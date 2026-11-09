# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CPCPayLevel(Document):
	def validate(self):
		if self.cells:
			self.entry_pay = self.cells[0].basic_pay
			self.maximum_pay = self.cells[-1].basic_pay
