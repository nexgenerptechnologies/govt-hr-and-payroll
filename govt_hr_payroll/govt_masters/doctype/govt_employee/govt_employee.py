# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import calendar
import frappe
from frappe.model.document import Document
from frappe.utils import add_years, getdate

class GovtEmployee(Document):
	def validate(self):
		self.set_full_name()
		self.calculate_dor()
		self.set_basic_pay_from_matrix()

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
		"""Fetch basic pay from CPC Pay Level cell if cell_no provided and basic_pay is empty or 0."""
		if self.pay_matrix_level and self.cell_no and (not self.basic_pay or self.basic_pay == 0):
			cells = frappe.get_all(
				"CPC Pay Cell",
				filters={"parent": self.pay_matrix_level, "cell_no": self.cell_no},
				fields=["basic_pay"]
			)
			if cells:
				self.basic_pay = cells[0].basic_pay
