# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

class CEAClaim(Document):
	def validate(self):
		self.validate_children_limit()
		self.calculate_claim_totals()

	def validate_children_limit(self):
		if len(self.children) > 2 and self.no_of_children <= 2:
			frappe.msgprint(_("Central Govt CEA rules normally restrict claims to the two oldest surviving children."))

	def calculate_claim_totals(self):
		tot_claimed = 0.0
		tot_admissible = 0.0

		# 7th CPC Statutory limits (DA >= 50% raises limit by 25%: ₹2,812.50/pm = ₹33,750/year per child)
		ANNUAL_CEA_CEILING = 33750.0
		ANNUAL_HOSTEL_CEILING = 101250.0

		for item in self.children:
			child_exp = flt(item.tuition_fee) + flt(item.books_notebooks_fee) + flt(item.uniform_fee)
			hostel_exp = flt(item.hostel_subsidy_claimed)
			item.total_claimed_child = child_exp + hostel_exp
			tot_claimed += item.total_claimed_child

			# Admissible cap per child
			adm_cea = min(child_exp, ANNUAL_CEA_CEILING)
			adm_hostel = min(hostel_exp, ANNUAL_HOSTEL_CEILING)
			tot_admissible += (adm_cea + adm_hostel)

		self.total_amount_claimed = tot_claimed
		self.total_amount_admissible = tot_admissible

		if not self.total_amount_sanctioned or self.total_amount_sanctioned == 0:
			self.total_amount_sanctioned = tot_admissible
