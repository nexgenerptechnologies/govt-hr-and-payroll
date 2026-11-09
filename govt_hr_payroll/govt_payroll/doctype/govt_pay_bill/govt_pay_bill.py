# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint

class GovtPayBill(Document):
	def validate(self):
		self.calculate_bill()

	def calculate_bill(self):
		settings = frappe.get_single("Govt Payroll Settings")
		da_rate = flt(self.da_rate or settings.current_da_rate or 50.0)
		nps_emp_rate = flt(settings.nps_emp_rate or 10.0)
		nps_govt_rate = flt(settings.nps_govt_rate or 14.0)

		# Totals accumulators
		tot_bp = 0.0
		tot_da = 0.0
		tot_hra = 0.0
		tot_tpt = 0.0
		tot_da_tpt = 0.0
		tot_misc_earn = 0.0
		tot_gross = 0.0

		tot_nps_emp = 0.0
		tot_nps_govt = 0.0
		tot_nps_grand = 0.0
		tot_gpf = 0.0
		tot_cghs = 0.0
		tot_lf = 0.0
		tot_cgegis = 0.0
		tot_itax = 0.0
		tot_cess = 0.0
		tot_misc_ded = 0.0
		tot_deductions = 0.0
		tot_net = 0.0

		for item in self.items:
			# 1. Earnings Calculation
			bp = flt(item.basic_pay)
			pension_ded = flt(item.pension_deduction)
			eff_bp = max(0.0, bp - pension_ded)
			item.effective_basic_pay = eff_bp

			item.da_rate = da_rate
			item.da_amount = round(eff_bp * (da_rate / 100.0))

			# HRA calculation
			hra_rate = flt(item.hra_rate)
			if item.license_fee and item.license_fee > 0:
				item.hra_amount = 0.0
			else:
				item.hra_amount = round(eff_bp * (hra_rate / 100.0))

			tpt = flt(item.tpt_allowance)
			item.da_on_tpt = round(tpt * (da_rate / 100.0))

			da_tpt_arr = flt(item.da_tpt_arrear)
			misc_allow = flt(item.misc_allowance)

			item.gross_pay = eff_bp + item.da_amount + item.hra_amount + tpt + item.da_on_tpt + da_tpt_arr + misc_allow

			# 2. NPS Contributions
			pran_base = eff_bp + item.da_amount
			if item.pran_gpf_no and not item.gpf_subscription:
				item.pran_emp_contrib = round(pran_base * (nps_emp_rate / 100.0))
				item.pran_govt_contrib = round(pran_base * (nps_govt_rate / 100.0))
				item.pran_total_emp = item.pran_emp_contrib + flt(item.pran_emp_arrear)
				item.pran_total_govt = item.pran_govt_contrib + flt(item.pran_govt_arrear)
				item.pran_grand_total = item.pran_total_emp + item.pran_total_govt
			else:
				item.pran_emp_contrib = 0.0
				item.pran_govt_contrib = 0.0
				item.pran_total_emp = 0.0
				item.pran_total_govt = 0.0
				item.pran_grand_total = 0.0

			# 3. GPF Contributions
			item.gpf_total = flt(item.gpf_subscription) + flt(item.gpf_refund)

			# 4. Other Recoveries
			itax = flt(item.income_tax)
			item.edu_cess = round(itax * 0.04)

			item.total_deduction = (
				item.pran_total_emp
				+ item.gpf_total
				+ flt(item.cghs_amount)
				+ flt(item.license_fee)
				+ flt(item.cgegis_amount)
				+ itax
				+ item.edu_cess
				+ flt(item.misc_deduction)
			)

			item.net_pay = item.gross_pay - item.total_deduction

			# Accumulate totals
			tot_bp += eff_bp
			tot_da += item.da_amount
			tot_hra += item.hra_amount
			tot_tpt += tpt
			tot_da_tpt += item.da_on_tpt
			tot_misc_earn += (da_tpt_arr + misc_allow)
			tot_gross += item.gross_pay

			tot_nps_emp += item.pran_total_emp
			tot_nps_govt += item.pran_total_govt
			tot_nps_grand += item.pran_grand_total
			tot_gpf += item.gpf_total
			tot_cghs += flt(item.cghs_amount)
			tot_lf += flt(item.license_fee)
			tot_cgegis += flt(item.cgegis_amount)
			tot_itax += itax
			tot_cess += item.edu_cess
			tot_misc_ded += flt(item.misc_deduction)
			tot_deductions += item.total_deduction
			tot_net += item.net_pay

		# Write summary headers
		self.total_basic_pay = tot_bp
		self.total_da = tot_da
		self.total_hra = tot_hra
		self.total_tpt = tot_tpt
		self.total_da_on_tpt = tot_da_tpt
		self.total_misc_allowance = tot_misc_earn
		self.total_gross_pay = tot_gross

		self.total_pran_emp = tot_nps_emp
		self.total_pran_govt = tot_nps_govt
		self.total_pran_grand = tot_nps_grand
		self.total_gpf = tot_gpf
		self.total_cghs = tot_cghs
		self.total_license_fee = tot_lf
		self.total_cgegis = tot_cgegis
		self.total_income_tax = tot_itax
		self.total_edu_cess = tot_cess
		self.total_misc_deduction = tot_misc_ded
		self.total_deductions = tot_deductions
		self.total_net_pay = tot_net

	@frappe.whitelist()
	def fetch_active_employees(self):
		if not self.office_unit:
			frappe.throw(_("Please select an Office / Unit first."))

		settings = frappe.get_single("Govt Payroll Settings")
		da_rate = flt(self.da_rate or settings.current_da_rate or 50.0)

		# Fetch city classification of the unit
		unit_doc = frappe.get_doc("Govt Office Unit", self.office_unit)
		city_class = unit_doc.city_classification or "X"
		hra_percent = {
			"X": flt(settings.hra_x_rate or 30.0),
			"Y": flt(settings.hra_y_rate or 20.0),
			"Z": flt(settings.hra_z_rate or 10.0)
		}.get(city_class, 30.0)

		employees = frappe.get_all(
			"Govt Employee",
			filters={"office_unit": self.office_unit, "status": "Active"},
			fields=["*"],
			order_by="employee_id asc"
		)

		self.items = []
		pc_counter = 1

		for emp in employees:
			item = self.append("items", {})
			item.pc_no = pc_counter
			pc_counter += 1

			item.employee = emp.employee_id
			item.employee_name = emp.employee_name
			item.designation = emp.designation
			item.pay_matrix_level = emp.pay_matrix_level
			item.dni = emp.dni
			item.pan = emp.pan
			item.dob = emp.dob

			# Pension scheme identifier
			if emp.pension_scheme == "NPS":
				item.pran_gpf_no = emp.pran_no
			elif emp.pension_scheme == "GPF":
				item.pran_gpf_no = emp.gpf_no
			else:
				item.pran_gpf_no = ""

			item.basic_pay = flt(emp.basic_pay)
			if emp.is_reemployed:
				item.pension_deduction = flt(emp.reemployed_pension_deduction)

			item.da_rate = da_rate
			item.hra_rate = hra_percent
			item.tpt_allowance = flt(emp.tpt_allowance or 7200)

			# Quarters & License Fee
			if emp.govt_quarters_availed:
				item.quarter_no = emp.quarter_no
				item.quarter_type = emp.quarter_type
				item.quarter_floor = emp.floor_no
				item.aan_no = emp.aan_no
				item.license_fee = flt(emp.license_fee)
				item.hra_amount = 0.0

			# GPF Subscription
			if emp.pension_scheme == "GPF":
				item.gpf_subscription = flt(emp.gpf_monthly_subscription)

			# Statutory deductions
			item.cghs_amount = flt(emp.cghs_monthly_deduction or 1000)
			item.cgegis_amount = flt(emp.cgegis_monthly_deduction or 120)
			item.income_tax = flt(emp.monthly_income_tax_tds or 0)

			# Bank Details
			item.bank_name = emp.bank_name
			item.bank_branch = emp.bank_branch
			item.bank_account_no = emp.account_no
			item.ifsc_code = emp.ifsc_code
			item.micr_code = emp.micr_code

		self.calculate_bill()
		return {"count": len(employees)}
