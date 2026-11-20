# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, getdate, flt, nowdate

class CCSLeaveApplication(Document):
	def validate(self):
		self.calculate_total_days()
		self.validate_gender_admissibility()
		self.validate_ccs_rules()
		self.validate_leave_balance()
		self.validate_prefix_suffix()
		self.set_current_balance()

	def validate_prefix_suffix(self):
		# Validate Prefix dates under CCS Leave Rules (Rule 22)
		if getattr(self, "prefix_from_date", None) and getattr(self, "prefix_to_date", None):
			if getdate(self.prefix_from_date) > getdate(self.prefix_to_date):
				frappe.throw(_("Prefix Holiday To Date cannot be earlier than Prefix Holiday From Date."), title=_("Invalid Prefix Dates"))
			if self.from_date and getdate(self.prefix_to_date) >= getdate(self.from_date):
				frappe.throw(_("Prefix Holiday To Date must precede the Leave From Date ({0}).").format(self.from_date), title=_("Invalid Prefix Dates"))

		# Validate Suffix dates under CCS Leave Rules (Rule 22)
		if getattr(self, "suffix_from_date", None) and getattr(self, "suffix_to_date", None):
			if getdate(self.suffix_from_date) > getdate(self.suffix_to_date):
				frappe.throw(_("Suffix Holiday To Date cannot be earlier than Suffix Holiday From Date."), title=_("Invalid Suffix Dates"))
			if self.to_date and getdate(self.suffix_from_date) <= getdate(self.to_date):
				frappe.throw(_("Suffix Holiday From Date must succeed the Leave To Date ({0}).").format(self.to_date), title=_("Invalid Suffix Dates"))

	def calculate_total_days(self):
		# Support for Half Day Leave (0.5 days)
		if getattr(self, "half_day", False) or flt(getattr(self, "total_days", 0)) == 0.5:
			if getattr(self, "half_day_date", None):
				self.from_date = self.half_day_date
				self.to_date = self.half_day_date
			elif self.from_date:
				self.to_date = self.from_date
			self.total_days = 0.5
			return

		if self.from_date and self.to_date:
			if getdate(self.from_date) > getdate(self.to_date):
				frappe.throw(_("To Date cannot be before From Date."))
			self.total_days = date_diff(self.to_date, self.from_date) + 1
			if self.total_days <= 0:
				frappe.throw(_("Total leave days must be at least 1 day."))

	def validate_gender_admissibility(self):
		if not self.employee or not self.leave_type:
			return

		gender = frappe.db.get_value("Govt Employee", self.employee, "gender")
		leave_type_doc = frappe.get_doc("CCS Leave Type", self.leave_type)
		leave_code = (leave_type_doc.leave_code or "").upper()
		leave_name = (self.leave_type or "").lower()

		# Rule 43: Maternity Leave - STRICTLY FEMALE ONLY
		if leave_code == "MAT" or "maternity" in leave_name:
			if gender != "Female":
				frappe.throw(
					_("Under Central Civil Services (Leave) Rules, 1972 (Rule 43), Maternity Leave is strictly admissible ONLY to Female Government servants. Employee {0} ({1}) is registered as '{2}' and cannot apply for Maternity Leave.").format(
						self.employee, self.employee_name or "", gender or "Unknown"
					),
					title=_("Gender Restriction Violation - Rule 43")
				)

		# Rule 43-A: Paternity Leave - STRICTLY MALE ONLY
		if leave_code == "PAT" or "paternity" in leave_name:
			if gender != "Male":
				frappe.throw(
					_("Under Central Civil Services (Leave) Rules, 1972 (Rule 43-A), Paternity Leave is strictly admissible ONLY to Male Government servants during confinement of wife. Employee {0} ({1}) is registered as '{2}' and cannot apply for Paternity Leave.").format(
						self.employee, self.employee_name or "", gender or "Unknown"
					),
					title=_("Gender Restriction Violation - Rule 43-A")
				)

		# Rule 43-C: Child Care Leave (CCL) - Female & Single Male only
		if leave_code == "CCL" or "child care" in leave_name:
			if gender == "Male":
				marital_status = None
				try:
					if frappe.db.has_column("Govt Employee", "marital_status"):
						marital_status = frappe.db.get_value("Govt Employee", self.employee, "marital_status")
				except Exception:
					pass

				if marital_status and marital_status.lower() == "married":
					frappe.throw(
						_("Under CCS Leave Rules (Rule 43-C) & DoPT guidelines, Child Care Leave is admissible to Female Government servants and Single Male employees (unmarried, widower, or legally divorced). Married male employees are not eligible for Child Care Leave."),
						title=_("CCL Admissibility Restriction - Rule 43-C")
					)
				elif not marital_status or marital_status.lower() not in ["unmarried", "widower", "divorced"]:
					frappe.throw(
						_("Under CCS Leave Rules (Rule 43-C), Child Care Leave is admissible only to Female employees and Single Male employees (unmarried, widower, or legally divorced). Employee '{0}' is registered as Male with Marital Status '{1}'. Please update employee Marital Status in Employee Master to confirm Single Male eligibility.").format(
							self.employee_name or self.employee, marital_status or "Not Specified"
						),
						title=_("Single Male Status Verification Required")
					)

	def validate_ccs_rules(self):
		leave_type_doc = frappe.get_doc("CCS Leave Type", self.leave_type)
		leave_code = (leave_type_doc.leave_code or "").upper()
		leave_name = (self.leave_type or "").lower()
		current_year = getdate(self.from_date or nowdate()).year

		# Rule 12: Absolute maximum continuous period of any leave is 5 years (1,825 days)
		if self.total_days > 1825:
			frappe.throw(
				_("Under CCS Leave Rule 12, no Government servant shall be granted leave of any kind for a continuous period exceeding five years (1,825 days)."),
				title=_("Rule 12 Continuous Absence Limit Exceeded")
			)

		# Rule 32: Extraordinary Leave (EOL) - Max 365 days (1 year) single spell
		if leave_code == "EOL" or "extraordinary" in leave_name or "extra ordinary" in leave_name:
			if self.total_days > 365:
				frappe.throw(
					_("Under Central Civil Services (Leave) Rules, 1972 (Rule 32), Extraordinary Leave (EOL) cannot exceed 365 days (1 year) in a single spell. You applied for {0} days. Absence beyond 1 year requires prior approval of the Cadre Controlling Authority / Ministry.").format(self.total_days),
					title=_("EOL Spell Ceiling Exceeded - Rule 32")
				)
			if not self.reason_for_leave:
				frappe.throw(
					_("Under CCS Rule 32, a specific written reason / justification is mandatory when applying for Extraordinary Leave (EOL)."),
					title=_("Reason Mandatory for EOL")
				)
			if self.total_days > 90 and not self.medical_certificate_attached:
				frappe.msgprint(
					_("Notice: Under CCS Rule 32, Extraordinary Leave exceeding 90 days generally requires a Registered Medical Practitioner certificate or approval for certified higher studies."),
					indicator="orange",
					title=_("Medical Certificate Recommended")
				)

		# Rule 26: Earned Leave (EL) can be availed up to 180 days at a time
		if leave_code == "EL" or "earned" in leave_name:
			if self.total_days > 180:
				frappe.throw(
					_("Under CCS Leave Rule 26, Earned Leave (EL) cannot be availed for more than 180 days in a single spell within India. Applied: {0} days.").format(self.total_days),
					title=_("Max Continuous EL Spell Exceeded")
				)

		# Rule 43: Maternity Leave - Max 180 days
		if leave_code == "MAT" or "maternity" in leave_name:
			if self.total_days > 180:
				frappe.throw(
					_("Under CCS Leave Rule 43, Maternity Leave cannot exceed 180 days for a single confinement. Applied: {0} days.").format(self.total_days),
					title=_("Maternity Leave Limit Exceeded")
				)
			if not self.medical_certificate_attached:
				frappe.throw(
					_("Under CCS Rule 43, a valid Medical Certificate / Confinement Proof is mandatory for Maternity Leave."),
					title=_("Medical Certificate Required")
				)

		# Rule 43-A: Paternity Leave - Max 15 days
		if leave_code == "PAT" or "paternity" in leave_name:
			if self.total_days > 15:
				frappe.throw(
					_("Under CCS Leave Rule 43-A, Paternity Leave cannot exceed 15 days in a single spell. Applied: {0} days.").format(self.total_days),
					title=_("Paternity Leave Limit Exceeded")
				)

		# Rule 43-C: Child Care Leave (CCL) - Min 5 days, Max 730 days lifetime, Max 3 spells per year
		if leave_code == "CCL" or "child care" in leave_name:
			if self.total_days < 5:
				frappe.throw(
					_("Under CCS Leave Rule 43-C, Child Care Leave (CCL) cannot be granted for less than 5 days at a time. Applied: {0} days.").format(self.total_days),
					title=_("Minimum Spell Violation")
				)

			# Check annual spell limit (max 3 spells in a calendar year)
			ccl_apps = frappe.get_all(
				"CCS Leave Application",
				filters={
					"employee": self.employee,
					"leave_type": self.leave_type,
					"status": ["in", ["Sanctioned by Competent Authority", "Applied", "Recommended by RO", "Verified by Dealing Clerk"]],
					"name": ["!=", self.name or ""]
				},
				fields=["from_date", "total_days"]
			)
			spells_this_year = sum(1 for a in ccl_apps if a.from_date and getdate(a.from_date).year == current_year)
			if spells_this_year >= 3:
				frappe.throw(
					_("Under CCS Leave Rule 43-C, Child Care Leave cannot be availed for more than 3 spells in a calendar year. You have already availed/applied for {0} spells in {1}.").format(
						spells_this_year, current_year
					),
					title=_("CCL Annual Spell Limit (Max 3 Spells)")
				)

			# Check cumulative 730 days lifetime ceiling
			total_ccl_taken = sum(flt(a.total_days) for a in ccl_apps)
			if (total_ccl_taken + self.total_days) > 730.0:
				frappe.throw(
					_("Under CCS Leave Rule 43-C, Child Care Leave exceeds the lifetime ceiling of 730 days. Already availed: {0} days, Currently applied: {1} days (Total: {2} days > 730 days maximum).").format(
						total_ccl_taken, self.total_days, total_ccl_taken + self.total_days
					),
					title=_("CCL Lifetime Ceiling Exceeded")
				)

		# Casual Leave (CL) - Annual quota of 8 days
		if leave_code == "CL" or "casual" in leave_name:
			if self.total_days > 8:
				frappe.throw(
					_("Casual Leave (CL) cannot exceed 8 days in total. Applied: {0} days.").format(self.total_days),
					title=_("CL Annual Quota Exceeded")
				)

			cl_apps = frappe.get_all(
				"CCS Leave Application",
				filters={
					"employee": self.employee,
					"leave_type": self.leave_type,
					"status": ["in", ["Sanctioned by Competent Authority", "Applied", "Recommended by RO", "Verified by Dealing Clerk"]],
					"name": ["!=", self.name or ""]
				},
				fields=["from_date", "total_days"]
			)
			cl_taken_year = sum(flt(a.total_days) for a in cl_apps if a.from_date and getdate(a.from_date).year == current_year)
			if (cl_taken_year + self.total_days) > 8.0:
				frappe.throw(
					_("Casual Leave (CL) quota of 8 days per calendar year exceeded. Already availed/applied in {0}: {1} days. Currently applied: {2} days (Total: {3} days > 8 days max quota).").format(
						current_year, cl_taken_year, self.total_days, cl_taken_year + self.total_days
					),
					title=_("CL Annual Quota Exceeded")
				)

		# Restricted Holiday (RH) - Annual quota of 2 days
		if leave_code == "RH" or "restricted" in leave_name:
			if self.total_days > 2:
				frappe.throw(
					_("Restricted Holiday (RH) cannot exceed 2 days in a calendar year. Applied: {0} days.").format(self.total_days),
					title=_("RH Annual Quota Exceeded")
				)

			rh_apps = frappe.get_all(
				"CCS Leave Application",
				filters={
					"employee": self.employee,
					"leave_type": self.leave_type,
					"status": ["in", ["Sanctioned by Competent Authority", "Applied", "Recommended by RO", "Verified by Dealing Clerk"]],
					"name": ["!=", self.name or ""]
				},
				fields=["from_date", "total_days"]
			)
			rh_taken_year = sum(flt(a.total_days) for a in rh_apps if a.from_date and getdate(a.from_date).year == current_year)
			if (rh_taken_year + self.total_days) > 2.0:
				frappe.throw(
					_("Restricted Holiday (RH) quota of 2 days per calendar year exceeded. Already availed/applied in {0}: {1} days. Currently applied: {2} days (Total: {3} days > 2 days max quota).").format(
						current_year, rh_taken_year, self.total_days, rh_taken_year + self.total_days
					),
					title=_("RH Annual Quota Exceeded")
				)

		# Rule 30: Commuted Leave requires medical certificate
		if leave_type_doc.is_commuted or leave_type_doc.requires_medical_certificate or leave_code == "COMMUTED":
			if not self.medical_certificate_attached:
				frappe.throw(
					_("Under CCS Leave Rule 30, a valid Medical Certificate from a Registered Medical Practitioner is mandatory for Commuted / Medical Leave."),
					title=_("Medical Certificate Mandatory")
				)

	def validate_leave_balance(self):
		leave_type_doc = frappe.get_doc("CCS Leave Type", self.leave_type)
		leave_code = (leave_type_doc.leave_code or "").upper()
		leave_name = (self.leave_type or "").lower()

		# For Commuted Leave: check Half Pay Leave (HPL) balance (needs 2x days)
		if leave_type_doc.is_commuted or leave_code == "COMMUTED":
			hpl_bal = get_leave_balance(self.employee, "Half Pay Leave")
			required_hpl = self.total_days * 2
			if required_hpl > hpl_bal:
				frappe.throw(
					_("Insufficient Half Pay Leave (HPL) balance to commute. Commuted Leave of {0} days requires {1} days of HPL (debits 2x), but your available HPL balance is only {2} days. Under CCS Rule 30, you cannot take more commuted leave than your HPL balance permits.").format(
						self.total_days, required_hpl, hpl_bal
					),
					title=_("Insufficient HPL Balance for Commutation")
				)
			return

		# For Earned Leave: check standard balance + 300-day buffer balance
		if leave_code == "EL" or "earned" in leave_name:
			std_bal = get_leave_balance(self.employee, "Earned Leave")
			buf_bal = get_buffer_balance(self.employee, "Earned Leave")
			total_avail = std_bal + buf_bal
			if self.total_days > total_avail:
				frappe.throw(
					_("Insufficient Earned Leave balance for {0}. You are applying for {1} days, but available balance is only {2} days (Standard: {3}d, Buffer: {4}d). Under CCS Leave Rules, leave exceeding available balance cannot be sanctioned without prior Competent Authority approval for Extra Ordinary Leave (EOL).").format(
						self.employee_name or self.employee, self.total_days, total_avail, std_bal, buf_bal
					),
					title=_("Insufficient Earned Leave Balance")
				)
			return

		# For Half Pay Leave
		if leave_code == "HPL" or "half pay" in leave_name:
			hpl_bal = get_leave_balance(self.employee, "Half Pay Leave")
			if self.total_days > hpl_bal:
				frappe.throw(
					_("Insufficient Half Pay Leave (HPL) balance for {0}. You are applying for {1} days, but available HPL balance is only {2} days.").format(
						self.employee_name or self.employee, self.total_days, hpl_bal
					),
					title=_("Insufficient Half Pay Leave Balance")
				)
			return

		# For other ledger-based leave types (excluding quota-based leaves and EOL which are without pay)
		if leave_code not in ["CL", "RH", "EOL", "MAT", "PAT", "CCL"]:
			bal = get_leave_balance(self.employee, self.leave_type)
			if bal is not None and self.total_days > bal:
				frappe.throw(
					_("Insufficient leave balance for {0}. Applied: {1} days, Available: {2} days.").format(
						self.leave_type, self.total_days, bal
					),
					title=_("Insufficient Leave Balance")
				)

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

@frappe.whitelist()
def get_leave_balance(employee, leave_type):
	entries = frappe.get_all(
		"CCS Leave Ledger Entry",
		filters={"employee": employee, "leave_type": leave_type},
		fields=["credit_days", "debit_days"],
		ignore_permissions=True
	)
	total_credit = sum([flt(e.credit_days) for e in entries])
	total_debit = sum([flt(e.debit_days) for e in entries])
	return max(0.0, total_credit - total_debit)

@frappe.whitelist()
def get_buffer_balance(employee, leave_type):
	entries = frappe.get_all(
		"CCS Leave Ledger Entry",
		filters={"employee": employee, "leave_type": leave_type},
		fields=["buffer_credit_days", "buffer_debit_days"],
		ignore_permissions=True
	)
	total_buffer_credit = sum([flt(e.buffer_credit_days) for e in entries])
	total_buffer_debit = sum([flt(e.buffer_debit_days) for e in entries])
	return max(0.0, total_buffer_credit - total_buffer_debit)
