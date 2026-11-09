# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from govt_hr_payroll.govt_payroll.doctype.govt_pay_bill.govt_pay_bill import GovtPayBill

class SupplementaryPayBill(Document):
	def validate(self):
		# Re-use calculation logic from GovtPayBill
		GovtPayBill.calculate_bill(self)
