# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from frappe.utils import flt

class CGHSMedicalClaim(Document):
	def validate(self):
		self.calculate_claim()

	def calculate_claim(self):
		tot = flt(self.opd_amount) + flt(self.test_investigations_amount) + flt(self.indoor_treatment_amount)
		self.total_amount_claimed = tot
		adv = flt(self.medical_advance_taken)
		self.net_amount_claimed = max(0.0, tot - adv)

		if not self.sanctioned_amount or self.sanctioned_amount == 0:
			self.sanctioned_amount = self.net_amount_claimed
