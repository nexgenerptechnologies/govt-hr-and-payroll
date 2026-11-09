# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, getdate, flt

class CCSLeaveApplication(Document):
	def validate(self):
		self.calculate_total_days()
		self.validate_ccs_rules()
		self.set_current_balance()

	def calculate_total_days(self):
		if self.from_date and self.to_date:
			if getdate(self.from_date) > getdate(self.to_date):
				frappe.throw(_("To Date cannot be before From Date."))
			self.total_days = date_diff(self.to_date, self.from_date) + 1

	def validate_ccs_rules(self):
		leave_type_doc = frappe.get_doc("CCS Leave Type", self.leave_type)

		# Rule 5: EL can be availed up to 180 days at a time
		if leave_type_doc.leave_code == "EL" and self.total_days > 180:
			frappe.throw(_("Under CCS Leave Rules, Earned Leave cannot be availed for more than 180 days at a time."))

		# Rule 6: Commuted leave requires medical certificate
		if leave_type_doc.is_commuted or leave_type_doc.requires_medical_certificate:
			if not self.medical_certificate_attached:
				frappe.throw(_("A valid Medical Certificate must be attached for Commuted / Medical Leave."))

	def set_current_balance(self):
		self.current_balance = get_leave_balance(self.employee, self.leave_type)

	def on_submit(self):
		if self.status != "Sanctioned by Competent Authority":
			self.status = "Sanctioned by Competent Authority"
			self.db_set("status", self.status)

		leave_type_doc = frappe.get_doc("CCS Leave Type", self.leave_type)

		# For Commuted Leave: debits 2x from Half Pay Leave (HPL)
		debit_qty = self.total_days * 2 if leave_type_doc.is_commuted else self.total_days
		effective_leave_type = "Half Pay Leave" if leave_type_doc.is_commuted else self.leave_type

		# Check 286-300 Day Buffer Set-off Rule for Earned Leave
		buffer_debit = 0.0
		standard_debit = debit_qty

		if leave_type_doc.leave_code == "EL":
			buffer_bal = get_buffer_balance(self.employee, self.leave_type)
			if buffer_bal > 0:
				buffer_debit = min(buffer_bal, debit_qty)
				standard_debit = debit_qty - buffer_debit

		# Create Leave Ledger Entry
		entry = frappe.new_doc("CCS Leave Ledger Entry")
		entry.employee = self.employee
		entry.leave_type = effective_leave_type
		entry.posting_date = self.from_date
		entry.transaction_type = "Leave Availed"
		entry.debit_days = standard_debit
		entry.buffer_debit_days = buffer_debit
		entry.reference_type = "CCS Leave Application"
		entry.reference_name = self.name
		entry.remarks = f"Leave availed from {self.from_date} to {self.to_date}"
		entry.flags.ignore_permissions = True
		entry.insert()

		# Auto-generate DO Part II Order draft
		self.create_do_part_two_order()

	def on_cancel(self):
		frappe.db.delete("CCS Leave Ledger Entry", {
			"reference_type": "CCS Leave Application",
			"reference_name": self.name
		})

	def create_do_part_two_order(self):
		existing = frappe.db.exists("DO Part Two Order", {"leave_application": self.name})
		if not existing:
			do_order = frappe.new_doc("DO Part Two Order")
			do_order.order_date = frappe.utils.today()
			do_order.office_unit = self.office_unit
			do_order.leave_application = self.name
			do_order.employee = self.employee
			do_order.sanction_text = (
				f"Sanction of the Competent Authority is hereby conveyed for the grant of "
				f"{self.total_days} days {self.leave_type} from {self.from_date} to {self.to_date} "
				f"to {self.employee_name}, {self.designation}."
			)
			do_order.flags.ignore_permissions = True
			do_order.insert()

def get_leave_balance(employee, leave_type):
	entries = frappe.get_all(
		"CCS Leave Ledger Entry",
		filters={"employee": employee, "leave_type": leave_type},
		fields=["credit_days", "debit_days"]
	)
	total_credit = sum([flt(e.credit_days) for e in entries])
	total_debit = sum([flt(e.debit_days) for e in entries])
	return max(0.0, total_credit - total_debit)

def get_buffer_balance(employee, leave_type):
	entries = frappe.get_all(
		"CCS Leave Ledger Entry",
		filters={"employee": employee, "leave_type": leave_type},
		fields=["buffer_credit_days", "buffer_debit_days"]
	)
	total_buffer_credit = sum([flt(e.buffer_credit_days) for e in entries])
	total_buffer_debit = sum([flt(e.buffer_debit_days) for e in entries])
	return max(0.0, total_buffer_credit - total_buffer_debit)
