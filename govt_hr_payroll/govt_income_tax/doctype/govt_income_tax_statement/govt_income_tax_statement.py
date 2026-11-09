# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, cint

class GovtIncomeTaxStatement(Document):
	def validate(self):
		self.calculate_statement()

	@frappe.whitelist()
	def populate_12_months(self):
		month_names = [
			"Mar", "Apr", "May", "Jun", "Jul", "Aug",
			"Sep", "Oct", "Nov", "Dec", "Jan", "Feb"
		]
		
		# If items are already populated, keep existing unless empty
		if not self.monthly_salary_items:
			self.monthly_salary_items = []
			for m in month_names:
				row = self.append("monthly_salary_items", {})
				row.month_name = m

		# Auto-pull defaults from employee
		if self.employee:
			emp = frappe.get_doc("Govt Employee", self.employee)
			bp = flt(emp.basic_pay)
			settings = frappe.get_single("Govt Payroll Settings")
			da_rate = flt(settings.current_da_rate or 50.0)
			da = round(bp * (da_rate / 100.0))
			tpt = flt(emp.tpt_allowance or 7200)
			cghs = flt(emp.cghs_monthly_deduction or 1000)
			cgegis = flt(emp.cgegis_monthly_deduction or 120)
			govt_nps = round((bp + da) * 0.14) if emp.pension_scheme == "NPS" else 0.0
			emp_nps = round((bp + da) * 0.10) if emp.pension_scheme == "NPS" else 0.0
			gpf = flt(emp.gpf_monthly_subscription) if emp.pension_scheme == "GPF" else 0.0

			for item in self.monthly_salary_items:
				if not item.pay_in_band or item.pay_in_band == 0:
					item.pay_in_band = bp
					item.da_amount = da
					item.tpt_allowance = tpt
					item.cghs_deduction = cghs
					item.cgegis_deduction = cgegis
					item.govt_nps_contribution = govt_nps
					item.gpf_nps_employee = emp_nps if emp.pension_scheme == "NPS" else gpf

		self.calculate_statement()

	def calculate_statement(self):
		tot_gross = 0.0
		tot_tds = 0.0
		tot_gpf = 0.0
		tot_cghs = 0.0
		tot_cgegis = 0.0
		tot_govt_nps = 0.0
		tot_hba_p = 0.0

		for item in self.monthly_salary_items:
			bp = flt(item.pay_in_band)
			da = flt(item.da_amount)
			hra = flt(item.hra_amount)
			cash = flt(item.cash_allowance)
			tpt = flt(item.tpt_allowance)
			govt_nps = flt(item.govt_nps_contribution)
			arr = flt(item.arrears_bonus_ota)

			item.total_monthly_gross = bp + da + hra + cash + tpt + govt_nps + arr
			tot_gross += item.total_monthly_gross

			tot_tds += (flt(item.tax_paid) + flt(item.cess_paid))
			tot_gpf += flt(item.gpf_nps_employee)
			tot_cghs += flt(item.cghs_deduction)
			tot_cgegis += flt(item.cgegis_deduction)
			tot_govt_nps += govt_nps
			tot_hba_p += flt(item.hba_principal)

		self.total_gross_salary = tot_gross
		self.tax_deducted_at_source = tot_tds

		# Auto-populate Chapter VI-A fields from 12-month ledger
		if not self.sec_80c_gpf:
			self.sec_80c_gpf = tot_gpf
		if not self.sec_80c_cgegis:
			self.sec_80c_cgegis = tot_cgegis
		if not self.sec_80c_hba_principal:
			self.sec_80c_hba_principal = tot_hba_p
		self.sec_80ccd_2_govt_nps = tot_govt_nps
		if not self.sec_80d_mediclaim_cghs:
			self.sec_80d_mediclaim_cghs = tot_cghs

		# Standard deduction: ₹75,000 for New Regime, ₹50,000 for Old Regime
		is_new_regime = "New" in (self.tax_regime or "New")
		self.standard_deduction = 75000.0 if is_new_regime else 50000.0

		# HRA Exemption u/s 10 (applicable only under Old Regime)
		if not is_new_regime and self.hra_rebate_claimed and self.annual_rent_paid:
			# Exemption calculation
			rent_excess = max(0.0, flt(self.annual_rent_paid) - (0.10 * tot_gross))
			self.hra_exemption_u_s_10 = min(rent_excess, 0.50 * tot_gross)
		else:
			self.hra_exemption_u_s_10 = 0.0

		self.income_under_salaries = max(0.0, self.total_gross_salary - self.hra_exemption_u_s_10)

		# Gross Total Income
		house_loss = flt(self.income_loss_house_property) if not is_new_regime else 0.0
		self.gross_total_income = max(
			0.0,
			self.income_under_salaries - self.standard_deduction + house_loss + flt(self.income_other_sources)
		)

		# Chapter VI-A Deductions
		c_total = (
			flt(self.sec_80c_gpf)
			+ flt(self.sec_80c_cgegis)
			+ flt(self.sec_80c_hba_principal)
			+ flt(self.sec_80c_cea)
			+ flt(self.sec_80c_ppf_nsc)
			+ flt(self.sec_80c_lic)
		)
		self.sec_80c_total_claimed = c_total
		self.sec_80c_admissible = min(150000.0, c_total) if not is_new_regime else 0.0

		if is_new_regime:
			# Only 80CCD(2) Govt NPS contribution is allowed under New Regime
			self.total_chapter_vi_a = flt(self.sec_80ccd_2_govt_nps)
		else:
			self.total_chapter_vi_a = (
				self.sec_80c_admissible
				+ min(50000.0, flt(self.sec_80ccd_1b_nps))
				+ flt(self.sec_80ccd_2_govt_nps)
				+ min(50000.0, flt(self.sec_80d_mediclaim_cghs))
				+ flt(self.sec_80g_donations)
			)

		# Net Taxable Income (rounded to nearest 10)
		raw_taxable = max(0.0, self.gross_total_income - self.total_chapter_vi_a)
		self.net_taxable_income = round(raw_taxable / 10.0) * 10

		# Calculate Tax on Slabs (New Tax Regime as per Folder 2 document):
		# Upto 4,00,000 : Nil
		# 4,00,001 to 8,00,000 : 5%
		# 8,00,001 to 12,00,000 : 10%
		# 12,00,001 to 16,00,000 : 15%
		# 16,00,001 to 20,00,000 : 20%
		# 20,00,001 to 24,00,000 : 25%
		# Above 24,00,000 : 30%
		tax = 0.0
		ti = self.net_taxable_income

		if is_new_regime:
			if ti > 2400000:
				tax += (ti - 2400000) * 0.30
				ti = 2400000
			if ti > 2000000:
				tax += (ti - 2000000) * 0.25
				ti = 2000000
			if ti > 1600000:
				tax += (ti - 1600000) * 0.20
				ti = 1600000
			if ti > 1200000:
				tax += (ti - 1200000) * 0.15
				ti = 1200000
			if ti > 800000:
				tax += (ti - 800000) * 0.10
				ti = 800000
			if ti > 400000:
				tax += (ti - 400000) * 0.05
		else:
			# Old Tax Regime
			if ti > 1000000:
				tax += (ti - 1000000) * 0.30
				ti = 1000000
			if ti > 500000:
				tax += (ti - 500000) * 0.20
				ti = 500000
			if ti > 250000:
				tax += (ti - 250000) * 0.05

		self.tax_on_income = round(tax)

		# 87A Rebate (if taxable income <= 7 Lakhs under New Regime)
		if is_new_regime and self.net_taxable_income <= 700000:
			self.rebate_u_s_87a = self.tax_on_income
		else:
			self.rebate_u_s_87a = 0.0

		self.net_tax_payable = max(0.0, self.tax_on_income - self.rebate_u_s_87a)
		self.educational_cess = round(self.net_tax_payable * 0.04)
		self.total_tax_and_cess = self.net_tax_payable + self.educational_cess
		self.tax_balance_payable_or_refundable = self.total_tax_and_cess - self.tax_deducted_at_source
