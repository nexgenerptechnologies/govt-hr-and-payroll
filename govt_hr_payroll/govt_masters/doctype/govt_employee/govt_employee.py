# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import calendar
import frappe
from frappe.model.document import Document
from frappe.utils import add_years, getdate, flt

class GovtEmployee(Document):
	def validate(self):
		self.set_full_name()
		self.calculate_dor()
		self.set_basic_pay_from_matrix()
		self.set_cgegis_deduction()
		self.calculate_annual_tax_gross()

	def set_full_name(self):
		parts = [self.first_name, self.last_name]
		self.employee_name = " ".join([p.strip() for p in parts if p])

	def calculate_dor(self):
		"""Central Govt retirement is last day of the month in which employee turns 60."""
		if self.dob and not self.dor:
			dob_date = getdate(self.dob)
			sixtieth_year = dob_date.year + 60
			month = dob_date.month
			last_day = calendar.monthrange(sixtieth_year, month)[1]
			self.dor = f"{sixtieth_year}-{month:02d}-{last_day:02d}"

	def set_basic_pay_from_matrix(self):
		"""Auto-populate Basic Pay from Pay Matrix Level (entry pay or cell pay)."""
		if self.pay_matrix_level:
			if self.cell_no:
				cell = frappe.db.get_value(
					"CPC Pay Cell",
					{"parent": self.pay_matrix_level, "cell_no": self.cell_no},
					"basic_pay"
				)
				if cell:
					self.basic_pay = flt(cell)
					return

			# If basic_pay is empty or 0, default to entry pay of the selected Pay Level
			if not self.basic_pay or self.basic_pay == 0:
				entry_pay = frappe.db.get_value("CPC Pay Level", self.pay_matrix_level, "entry_pay")
				if entry_pay:
					self.basic_pay = flt(entry_pay)

	def set_cgegis_deduction(self):
		"""Auto-populate monthly CGEGIS deduction according to Central Govt Group."""
		cgegis_map = {
			"Group A": 120.0,
			"Group B": 60.0,
			"Group C": 30.0,
			"Group D": 15.0
		}
		if self.cgegis_group in cgegis_map:
			if not self.cgegis_monthly_deduction or self.cgegis_monthly_deduction == 0 or self.has_value_changed("cgegis_group"):
				self.cgegis_monthly_deduction = cgegis_map[self.cgegis_group]

	def calculate_annual_tax_gross(self):
		"""Calculates total annual gross salary including arrears, leave encashment, bonus, and CEA."""
		bp = flt(self.basic_pay)
		if (not self.annual_regular_gross or self.annual_regular_gross == 0) and bp > 0:
			da = round(bp * 0.53)
			tpt = flt(self.tpt_allowance or 7200)
			da_tpt = round(tpt * 0.53)
			self.annual_regular_gross = (bp + da + tpt + da_tpt) * 12.0

		self.total_annual_gross_salary = (
			flt(self.annual_regular_gross)
			+ flt(self.leave_encashment_taxable)
			+ flt(self.arrears_taxable)
			+ flt(self.bonus_taxable)
			+ flt(self.cea_received_taxable)
			+ flt(self.other_taxable_earnings)
		)
