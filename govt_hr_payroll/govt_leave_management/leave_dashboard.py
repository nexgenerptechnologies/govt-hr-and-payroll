# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, nowdate, getdate

@frappe.whitelist()
def get_employee_leave_dashboard(employee=None):
	"""
	Returns real-time leave dashboard metrics for an employee:
	- Available balance at credit
	- Taken / availed leave days
	- Statutory ceilings & buffer credit details
	- Color gradient themes & quick-apply links
	"""
	user = frappe.session.user

	# 1. Determine Target Employee
	if not employee:
		# Check if user matches user_id on Govt Employee
		try:
			emp_by_user = frappe.db.get_value("Govt Employee", {"user_id": user, "status": "Active"}, "employee_id")
			if emp_by_user:
				employee = emp_by_user
		except Exception:
			pass

		# If still not found, check if user matches employee_id or email
		if not employee:
			try:
				emp_by_id = frappe.db.get_value("Govt Employee", {"employee_id": user, "status": "Active"}, "employee_id")
				if emp_by_id:
					employee = emp_by_id
			except Exception:
				pass

		# Fallback to first active employee
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
	# Rule: Debits 2x HPL. Available = HPL balance / 2
	commuted_available = int(hpl_available // 2)
	commuted_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Commuted Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days"]
	)
	commuted_taken = sum([flt(a.total_days) for a in commuted_apps])

	# --- D. Casual Leave (CL) ---
	# Annual quota: 8 days
	cl_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Casual Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days", "from_date"]
	)
	cl_taken = sum([flt(a.total_days) for a in cl_apps if a.from_date and getdate(a.from_date).year == current_year])
	cl_available = max(0.0, 8.0 - cl_taken)

	# --- E. Restricted Holiday (RH) ---
	# Annual quota: 2 days
	rh_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Restricted Holiday", "status": "Sanctioned by Competent Authority"},
		fields=["total_days", "from_date"]
	)
	rh_taken = sum([flt(a.total_days) for a in rh_apps if a.from_date and getdate(a.from_date).year == current_year])
	rh_available = max(0.0, 2.0 - rh_taken)

	# --- F. Child Care Leave (CCL) ---
	# Lifetime ceiling: 730 days
	ccl_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Child Care Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days"]
	)
	ccl_taken = sum([flt(a.total_days) for a in ccl_apps])
	ccl_available = max(0.0, 730.0 - ccl_taken)

	# --- G. Maternity Leave (180 Days) ---
	mat_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Maternity Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days"]
	)
	mat_taken = sum([flt(a.total_days) for a in mat_apps])
	mat_available = max(0.0, 180.0 - mat_taken)

	# --- H. Paternity Leave (15 Days) ---
	pat_apps = frappe.get_all(
		"CCS Leave Application",
		filters={"employee": employee, "leave_type": "Paternity Leave", "status": "Sanctioned by Competent Authority"},
		fields=["total_days"]
	)
	pat_taken = sum([flt(a.total_days) for a in pat_apps])
	pat_available = max(0.0, 15.0 - pat_taken)

	cards = [
		{
			"leave_code": "EL",
			"leave_name": "Earned Leave (EL)",
			"leave_type": "Earned Leave",
			"available": el_available,
			"taken": el_taken,
			"max_ceiling": 300,
			"unit": "Days",
			"theme": "blue",
			"gradient": "linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%)",
			"accent_color": "#2563eb",
			"icon": "📘",
			"note": f"Buffer Credit: {el_buffer_available}d" if el_buffer_available > 0 else "Ceiling: 300d (15d Jan/Jul)",
			"can_apply": True
		},
		{
			"leave_code": "HPL",
			"leave_name": "Half Pay Leave (HPL)",
			"leave_type": "Half Pay Leave",
			"available": hpl_available,
			"taken": hpl_taken,
			"max_ceiling": 300,
			"unit": "Days",
			"theme": "emerald",
			"gradient": "linear-gradient(135deg, #065f46 0%, #059669 50%, #10b981 100%)",
			"accent_color": "#059669",
			"icon": "📗",
			"note": "10d Advance Credit Jan/Jul",
			"can_apply": True
		},
		{
			"leave_code": "COMMUTED",
			"leave_name": "Commuted Leave",
			"leave_type": "Commuted Leave",
			"available": commuted_available,
			"taken": commuted_taken,
			"max_ceiling": 150,
			"unit": "Days",
			"theme": "purple",
			"gradient": "linear-gradient(135deg, #581c87 0%, #7c3aed 50%, #8b5cf6 100%)",
			"accent_color": "#7c3aed",
			"icon": "🟣",
			"note": "Full Pay (Debits 2x HPL)",
			"can_apply": True
		},
		{
			"leave_code": "CL",
			"leave_name": "Casual Leave (CL)",
			"leave_type": "Casual Leave",
			"available": cl_available,
			"taken": cl_taken,
			"max_ceiling": 8,
			"unit": "Days",
			"theme": "amber",
			"gradient": "linear-gradient(135deg, #9a3412 0%, #ea580c 50%, #f59e0b 100%)",
			"accent_color": "#ea580c",
			"icon": "📙",
			"note": "Annual Quota: 8 Days",
			"can_apply": True
		},
		{
			"leave_code": "RH",
			"leave_name": "Restricted Holiday (RH)",
			"leave_type": "Restricted Holiday",
			"available": rh_available,
			"taken": rh_taken,
			"max_ceiling": 2,
			"unit": "Days",
			"theme": "teal",
			"gradient": "linear-gradient(135deg, #115e59 0%, #0d9488 50%, #14b8a6 100%)",
			"accent_color": "#0d9488",
			"icon": "🌴",
			"note": "Annual Quota: 2 Days",
			"can_apply": True
		},
		{
			"leave_code": "CCL",
			"leave_name": "Child Care Leave (CCL)",
			"leave_type": "Child Care Leave",
			"available": ccl_available,
			"taken": ccl_taken,
			"max_ceiling": 730,
			"unit": "Days",
			"theme": "pink",
			"gradient": "linear-gradient(135deg, #9d174d 0%, #db2777 50%, #ec4899 100%)",
			"accent_color": "#db2777",
			"icon": "👶",
			"note": "Lifetime Cap: 730d (<18 yrs)",
			"can_apply": emp_doc.gender in ["Female", "Other"]
		}
	]

	# Add gender specific card
	if emp_doc.gender in ["Female", "Other"]:
		cards.append({
			"leave_code": "MAT",
			"leave_name": "Maternity Leave",
			"leave_type": "Maternity Leave",
			"available": mat_available,
			"taken": mat_taken,
			"max_ceiling": 180,
			"unit": "Days",
			"theme": "indigo",
			"gradient": "linear-gradient(135deg, #312e81 0%, #4f46e5 50%, #6366f1 100%)",
			"accent_color": "#4f46e5",
			"icon": "🤱",
			"note": "180 Days (Full Pay)",
			"can_apply": True
		})
	else:
		cards.append({
			"leave_code": "PAT",
			"leave_name": "Paternity Leave",
			"leave_type": "Paternity Leave",
			"available": pat_available,
			"taken": pat_taken,
			"max_ceiling": 15,
			"unit": "Days",
			"theme": "indigo",
			"gradient": "linear-gradient(135deg, #312e81 0%, #4f46e5 50%, #6366f1 100%)",
			"accent_color": "#4f46e5",
			"icon": "👨‍👧",
			"note": "15 Days (Confinement)",
			"can_apply": True
		})

	return {
		"employee": {
			"employee_id": emp_doc.employee_id,
			"employee_name": emp_doc.employee_name,
			"designation": emp_doc.designation,
			"office_unit": emp_doc.office_unit,
			"gender": emp_doc.gender
		},
		"all_employees": all_employees,
		"leave_cards": cards
	}
