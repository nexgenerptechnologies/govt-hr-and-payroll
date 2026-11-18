# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, nowdate, getdate

@frappe.whitelist()
def get_employee_leave_dashboard(employee=None):
	"""
	Returns real-time leave dashboard metrics for an employee formatted
	exactly as per the e-HRMS colored card specification:
	- Solid colored circular icon top
	- Centered title
	- Large bold number
	- Colored outer border
	- Available and taken breakdown
	"""
	user = frappe.session.user

	# 1. Determine Target Employee
	if not employee:
		try:
			emp_by_user = frappe.db.get_value("Govt Employee", {"user_id": user, "status": "Active"}, "employee_id")
			if emp_by_user:
				employee = emp_by_user
		except Exception:
			pass

		if not employee:
			try:
				emp_by_id = frappe.db.get_value("Govt Employee", {"employee_id": user, "status": "Active"}, "employee_id")
				if emp_by_id:
					employee = emp_by_id
			except Exception:
				pass

		if not employee:
			first_emp = frappe.get_all("Govt Employee", filters={"status": "Active"}, fields=["employee_id"], limit=1)
			if first_emp:
				employee = first_emp[0].employee_id

	all_employees = frappe.get_all(
		"Govt Employee",
		filters={"status": "Active"},
		fields=["employee_id", "employee_name", "designation", "office_unit"],
		order_by="employee_id asc"
	)

	if not employee:
		return {
			"employee": None,
			"all_employees": all_employees,
			"leave_cards": []
		}

	emp_doc = frappe.get_doc("Govt Employee", employee)
	current_year = getdate(nowdate()).year

	# 2. Fetch all leave ledger entries for this employee
	ledger_entries = frappe.get_all(
		"CCS Leave Ledger Entry",
		filters={"employee": employee},
		fields=["leave_type", "credit_days", "debit_days", "buffer_credit_days", "buffer_debit_days", "posting_date"]
	)

	# 3. Calculate for each statutory leave type
	# --- A. Earned Leave (EL) ---
	el_credits = sum([flt(e.credit_days) for e in ledger_entries if e.leave_type == "Earned Leave"])
	el_debits = sum([flt(e.debit_days) for e in ledger_entries if e.leave_type == "Earned Leave"])
	el_buffer_credits = sum([flt(e.buffer_credit_days) for e in ledger_entries if e.leave_type == "Earned Leave"])
	el_buffer_debits = sum([flt(e.buffer_debit_days) for e in ledger_entries if e.leave_type == "Earned Leave"])
	el_available = max(0.0, el_credits - el_debits)
	el_buffer_available = max(0.0, el_buffer_credits - el_buffer_debits)
	el_taken = el_debits + el_buffer_debits

	# --- B. Half Pay Leave (HPL) ---
	hpl_credits = sum([flt(e.credit_days) for e in ledger_entries if e.leave_type == "Half Pay Leave"])
	hpl_debits = sum([flt(e.debit_days) for e in ledger_entries if e.leave_type == "Half Pay Leave"])
	hpl_available = max(0.0, hpl_credits - hpl_debits)
	hpl_taken = hpl_debits

	# --- C. Commuted Leave (Medical) ---
	commuted_available = int(hpl_available // 2)
	commuted_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Commuted Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days"]
	)
	commuted_taken = sum([flt(a.total_days) for a in commuted_apps])

	# --- D. Casual Leave (CL) ---
	cl_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Casual Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days", "from_date"]
	)
	cl_taken = sum([flt(a.total_days) for a in cl_apps if a.from_date and getdate(a.from_date).year == current_year])
	cl_available = max(0.0, 8.0 - cl_taken)

	# --- E. Restricted Holiday (RH) ---
	rh_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Restricted Holiday", "status": "Sanctioned by Competent Authority"},
		fields=["total_days", "from_date"]
	)
	rh_taken = sum([flt(a.total_days) for a in rh_apps if a.from_date and getdate(a.from_date).year == current_year])
	rh_available = max(0.0, 2.0 - rh_taken)

	# --- F. Child Care Leave (CCL) ---
	ccl_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Child Care Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days"]
	)
	ccl_taken = sum([flt(a.total_days) for a in ccl_apps])
	ccl_available = max(0.0, 730.0 - ccl_taken)

	# --- G. Maternity / Paternity Leave ---
	mat_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Maternity Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days"]
	)
	mat_taken = sum([flt(a.total_days) for a in mat_apps])
	mat_available = max(0.0, 180.0 - mat_taken)

	pat_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Paternity Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days"]
	)
	pat_taken = sum([flt(a.total_days) for a in pat_apps])
	pat_available = max(0.0, 15.0 - pat_taken)

	# --- H. Claims from Folder 5 (CEA & CGHS MRC-S) ---
	cea_records = frappe.get_all(
		"CEA Claim",
		filters={"employee": employee, "docstatus": ["!=", 2]},
		fields=["total_amount_sanctioned", "total_amount_claimed"]
	)
	total_cea = sum([flt(c.total_amount_sanctioned or c.total_amount_claimed) for c in cea_records])

	med_records = frappe.get_all(
		"CGHS Medical Claim",
		filters={"employee": employee, "docstatus": ["!=", 2]},
		fields=["amount_sanctioned", "total_claimed"]
	)
	total_med = sum([flt(m.amount_sanctioned or m.total_claimed) for m in med_records])

	# Total Leaves Applied
	total_leaves_applied_count = frappe.db.count("CCS Leave Application", {"employee": employee})

	# Format integer vs float cleanly
	def fmt(val):
		if val is None:
			return "0"
		return str(int(val)) if val == int(val) else f"{val:.1f}"

	# BUILD THE CARDS MATCHING IMAGE 3
	cards = [
		{
			"id": "el",
			"title": "Earned Leave (EL)",
			"leave_type": "Earned Leave",
			"value": fmt(el_available),
			"unit": "Days",
			"sub_text": f"Available | Taken: {fmt(el_taken)}d",
			"note": f"Buffer: {fmt(el_buffer_available)}d" if el_buffer_available > 0 else "Max: 300 Days",
			"color": "#e11d48",           # Pink (Image 3 Card 1 style)
			"icon_type": "calendar",
			"can_apply": True
		},
		{
			"id": "cl",
			"title": "Casual Leave (CL)",
			"leave_type": "Casual Leave",
			"value": fmt(cl_available),
			"unit": "Days",
			"sub_text": f"Available | Taken: {fmt(cl_taken)}d",
			"note": "Quota: 8 Days/Year",
			"color": "#0284c7",           # Sky Blue (Image 3 Card 2 style)
			"icon_type": "clock",
			"can_apply": True
		},
		{
			"id": "hpl",
			"title": "Half Pay Leave (HPL)",
			"leave_type": "Half Pay Leave",
			"value": fmt(hpl_available),
			"unit": "Days",
			"sub_text": f"Available | Taken: {fmt(hpl_taken)}d",
			"note": "10d Advance Jan/Jul",
			"color": "#ea580c",           # Sunset Orange (Image 3 Card 3 style)
			"icon_type": "book",
			"can_apply": True
		},
		{
			"id": "commuted",
			"title": "Commuted Leave",
			"leave_type": "Commuted Leave",
			"value": fmt(commuted_available),
			"unit": "Days",
			"sub_text": f"Available | Taken: {fmt(commuted_taken)}d",
			"note": "Full Pay (Debits 2x HPL)",
			"color": "#16a34a",           # Emerald Green (Image 3 Card 4 style)
			"icon_type": "medical_cross",
			"can_apply": True
		},
		{
			"id": "ccl",
			"title": "Child Care Leave (CCL)",
			"leave_type": "Child Care Leave",
			"value": fmt(ccl_available),
			"unit": "Days",
			"sub_text": f"Available | Taken: {fmt(ccl_taken)}d",
			"note": "Lifetime: 730 Days",
			"color": "#dc2626",           # Red/Crimson (Image 3 Card 5 style)
			"icon_type": "family",
			"can_apply": emp_doc.gender in ["Female", "Other"]
		},
		{
			"id": "rh",
			"title": "Restricted Holiday (RH)",
			"leave_type": "Restricted Holiday",
			"value": fmt(rh_available),
			"unit": "Days",
			"sub_text": f"Available | Taken: {fmt(rh_taken)}d",
			"note": "Quota: 2 Days/Year",
			"color": "#9333ea",           # Purple
			"icon_type": "star",
			"can_apply": True
		}
	]

	# Add Maternity / Paternity
	if emp_doc.gender in ["Female", "Other"]:
		cards.append({
			"id": "mat",
			"title": "Maternity Leave",
			"leave_type": "Maternity Leave",
			"value": fmt(mat_available),
			"unit": "Days",
			"sub_text": f"Entitlement | Taken: {fmt(mat_taken)}d",
			"note": "180 Days Full Pay",
			"color": "#7c3aed",
			"icon_type": "maternity",
			"can_apply": True
		})
	else:
		cards.append({
			"id": "pat",
			"title": "Paternity Leave",
			"leave_type": "Paternity Leave",
			"value": fmt(pat_available),
			"unit": "Days",
			"sub_text": f"Entitlement | Taken: {fmt(pat_taken)}d",
			"note": "15 Days Confinement",
			"color": "#4f46e5",
			"icon_type": "paternity",
			"can_apply": True
		})

	# Add Folder 5 Claims: CEA & Medical CGHS
	cards.append({
		"id": "cea",
		"title": "Child Education (CEA)",
		"leave_type": None,
		"value": f"₹{int(total_cea):,}" if total_cea > 0 else "₹0",
		"unit": "",
		"sub_text": "Sanctioned / Claimed",
		"note": "Max: ₹33,750/Child",
		"color": "#0d9488",              # Teal
		"icon_type": "academic",
		"is_claim": True,
		"doctype": "CEA Claim"
	})

	cards.append({
		"id": "cghs",
		"title": "Medical Claim (MRC-S)",
		"leave_type": None,
		"value": f"₹{int(total_med):,}" if total_med > 0 else "₹0",
		"unit": "",
		"sub_text": "Sanctioned / Claimed",
		"note": "CGHS Form MRC-S",
		"color": "#0284c7",              # Sky Blue
		"icon_type": "hospital",
		"is_claim": True,
		"doctype": "CGHS Medical Claim"
	})

	return {
		"employee": {
			"employee_id": emp_doc.employee_id,
			"employee_name": emp_doc.employee_name,
			"designation": emp_doc.designation,
			"office_unit": emp_doc.office_unit,
			"gender": emp_doc.gender,
			"total_leaves_applied": total_leaves_applied_count
		},
		"all_employees": all_employees,
		"leave_cards": cards
	}
