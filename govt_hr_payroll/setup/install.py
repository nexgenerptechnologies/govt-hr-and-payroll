# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import os
import json
import frappe
from frappe.utils import flt, today

def after_install():
	setup_cpc_pay_levels()
	setup_payroll_settings()
	setup_default_leave_types()
	setup_workspaces()

def after_migrate():
	setup_cpc_pay_levels()
	setup_payroll_settings()
	setup_default_leave_types()
	setup_workspaces()

def setup_workspaces():
	workspace_files = [
		"govt_payroll/workspace/govt_hr_and_payroll/govt_hr_and_payroll.json",
		"govt_payroll/workspace/govt_payroll/govt_payroll.json",
		"govt_income_tax/workspace/govt_income_tax/govt_income_tax.json",
		"govt_leave_management/workspace/govt_leave_management/govt_leave_management.json",
		"govt_claims/workspace/govt_claims/govt_claims.json",
		"govt_tour_ta_da/workspace/govt_tour_ta_da/govt_tour_ta_da.json",
		"govt_masters/workspace/govt_masters/govt_masters.json"
	]
	app_path = frappe.get_app_path("govt_hr_payroll")
	for rel_file in workspace_files:
		full_path = os.path.join(app_path, rel_file)
		if not os.path.exists(full_path):
			continue
		try:
			with open(full_path, "r", encoding="utf-8") as f:
				data = json.load(f)
			ws_name = data.get("name")
			if not ws_name:
				continue
			
			if frappe.db.exists("Workspace", ws_name):
				doc = frappe.get_doc("Workspace", ws_name)
			else:
				doc = frappe.new_doc("Workspace")
				doc.name = ws_name
			
			doc.label = data.get("label", ws_name)
			doc.title = data.get("title", ws_name)
			doc.module = data.get("module")
			doc.category = data.get("category", "Modules")
			doc.icon = data.get("icon", "folder")
			doc.indicator_color = data.get("indicator_color", "blue")
			doc.is_standard = 1
			doc.public = 1
			doc.sequence_id = data.get("sequence_id", 1.0)
			doc.content = data.get("content", "[]")
			
			# Reset and reload shortcuts and links cleanly
			doc.set("shortcuts", [])
			for sc in data.get("shortcuts", []):
				doc.append("shortcuts", sc)
			
			doc.set("links", [])
			for lk in data.get("links", []):
				doc.append("links", lk)
			
			doc.flags.ignore_permissions = True
			doc.flags.ignore_mandatory = True
			doc.save()
		except Exception as e:
			frappe.log_error(f"Error loading workspace {rel_file}: {e}")
	
	frappe.db.commit()

def setup_payroll_settings():
	try:
		if not frappe.db.exists("Govt Payroll Settings", "Govt Payroll Settings"):
			settings = frappe.new_doc("Govt Payroll Settings")
			settings.current_financial_year = "2026-2027"
			settings.current_da_rate = 50.0
			settings.nps_emp_rate = 10.0
			settings.nps_govt_rate = 14.0
			settings.standard_edu_cess = 4.0
			settings.hra_x_rate = 30.0
			settings.hra_y_rate = 20.0
			settings.hra_z_rate = 10.0
			settings.flags.ignore_permissions = True
			settings.flags.ignore_mandatory = True
			settings.insert()
			frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error initializing Govt Payroll Settings: {e}")

def setup_cpc_pay_levels():
	levels_data = [
		("Level-1", 1800, 18000, 40),
		("Level-2", 1900, 19900, 40),
		("Level-3", 2000, 21700, 40),
		("Level-4", 2400, 25500, 40),
		("Level-5", 2800, 29200, 40),
		("Level-6", 4200, 35400, 40),
		("Level-7", 4600, 44900, 40),
		("Level-8", 4800, 47600, 40),
		("Level-9", 5400, 53100, 40),
		("Level-10", 5400, 56100, 40),
		("Level-11", 6600, 67700, 39),
		("Level-12", 7600, 78800, 34),
		("Level-13", 8700, 123100, 20),
		("Level-13A", 8900, 131100, 18),
		("Level-14", 10000, 144200, 15),
		("Level-15", 0, 182200, 8),
		("Level-16", 0, 205400, 4),
		("Level-17", 0, 225000, 1),
		("Level-18", 0, 250000, 1)
	]

	for lvl_name, gp, start_pay, num_cells in levels_data:
		try:
			if not frappe.db.exists("CPC Pay Level", lvl_name):
				doc = frappe.new_doc("CPC Pay Level")
				doc.pay_level = lvl_name
				doc.grade_pay = gp
				doc.entry_pay = start_pay
				
				current_pay = start_pay
				for cell_idx in range(1, num_cells + 1):
					doc.append("cells", {
						"cell_no": cell_idx,
						"basic_pay": current_pay
					})
					inc = round(current_pay * 0.03 / 100) * 100
					current_pay += inc

				doc.maximum_pay = doc.cells[-1].basic_pay
				doc.flags.ignore_permissions = True
				doc.flags.ignore_mandatory = True
				doc.insert()
		except Exception as e:
			frappe.log_error(f"Error creating pay level {lvl_name}: {e}")

	frappe.db.commit()

def setup_default_leave_types():
	types = [
		{
			"leave_type_name": "Earned Leave",
			"leave_code": "EL",
			"max_days_at_a_time": 180,
			"max_accumulation": 300,
			"is_commuted": 0,
			"requires_medical_certificate": 0,
			"description": "CCS Rule: 15 days advance credit on 01 Jan and 01 Jul. 300 days ceiling."
		},
		{
			"leave_type_name": "Half Pay Leave",
			"leave_code": "HPL",
			"max_days_at_a_time": 180,
			"max_accumulation": 300,
			"is_commuted": 0,
			"requires_medical_certificate": 0,
			"description": "CCS Rule: 10 days advance credit on 01 Jan and 01 Jul."
		},
		{
			"leave_type_name": "Commuted Leave",
			"leave_code": "COMMUTED",
			"max_days_at_a_time": 90,
			"max_accumulation": 150,
			"is_commuted": 1,
			"requires_medical_certificate": 1,
			"description": "Debits 2x from HPL balance. Mandatory medical certificate."
		},
		{
			"leave_type_name": "Maternity Leave",
			"leave_code": "MAT",
			"max_days_at_a_time": 180,
			"max_accumulation": 180,
			"is_commuted": 0,
			"requires_medical_certificate": 1,
			"description": "Admissible up to 180 days for female employees."
		},
		{
			"leave_type_name": "Paternity Leave",
			"leave_code": "PAT",
			"max_days_at_a_time": 15,
			"max_accumulation": 15,
			"is_commuted": 0,
			"requires_medical_certificate": 0,
			"description": "Admissible for 15 days during confinement of wife."
		},
		{
			"leave_type_name": "Child Care Leave",
			"leave_code": "CCL",
			"max_days_at_a_time": 180,
			"max_accumulation": 730,
			"is_commuted": 0,
			"requires_medical_certificate": 0,
			"description": "Admissible up to 730 days during entire service."
		},
		{
			"leave_type_name": "Extraordinary Leave",
			"leave_code": "EOL",
			"max_days_at_a_time": 365,
			"max_accumulation": 0,
			"is_commuted": 0,
			"requires_medical_certificate": 0,
			"description": "Without pay. 1/10th EL deducted for EOL availed."
		}
	]

	for lt in types:
		try:
			if not frappe.db.exists("CCS Leave Type", lt["leave_type_name"]):
				doc = frappe.new_doc("CCS Leave Type")
				doc.update(lt)
				doc.flags.ignore_permissions = True
				doc.flags.ignore_mandatory = True
				doc.insert()
		except Exception as e:
			frappe.log_error(f"Error creating leave type {lt['leave_type_name']}: {e}")

	frappe.db.commit()

@frappe.whitelist()
def credit_half_yearly_el_and_hpl():
	"""
	CCS Leave Rule 1 & 2:
	1. 15 days EL auto credited on 01 Jan and 01 Jul.
	2. Ceiling is 300 days. If balance at credit is between 286-300 days,
	   the advance 15 days is placed into buffer_credit_days to set off during the half year.
	3. 10 days HPL credited on 01 Jan and 01 Jul.
	"""
	active_employees = frappe.get_all("Govt Employee", filters={"status": "Active"}, fields=["employee_id", "employee_name"])
	count = 0

	for emp in active_employees:
		# 1. Earned Leave Credit
		el_entries = frappe.get_all(
			"CCS Leave Ledger Entry",
			filters={"employee": emp.employee_id, "leave_type": "Earned Leave"},
			fields=["credit_days", "debit_days"]
		)
		curr_el = sum([flt(e.credit_days) - flt(e.debit_days) for e in el_entries])

		std_credit = 0.0
		buffer_credit = 0.0

		if curr_el >= 300:
			buffer_credit = 15.0
		elif curr_el >= 285:
			std_credit = 300.0 - curr_el
			buffer_credit = 15.0 - std_credit
		else:
			std_credit = 15.0

		entry_el = frappe.new_doc("CCS Leave Ledger Entry")
		entry_el.employee = emp.employee_id
		entry_el.leave_type = "Earned Leave"
		entry_el.posting_date = today()
		entry_el.transaction_type = "Advance Credit (Jan/Jul)"
		entry_el.credit_days = std_credit
		entry_el.buffer_credit_days = buffer_credit
		entry_el.remarks = "Half-yearly advance credit under CCS Leave Rules"
		entry_el.flags.ignore_permissions = True
		entry_el.insert()

		# 2. Half Pay Leave Credit (10 days)
		entry_hpl = frappe.new_doc("CCS Leave Ledger Entry")
		entry_hpl.employee = emp.employee_id
		entry_hpl.leave_type = "Half Pay Leave"
		entry_hpl.posting_date = today()
		entry_hpl.transaction_type = "Advance Credit (Jan/Jul)"
		entry_hpl.credit_days = 10.0
		entry_hpl.remarks = "Half-yearly advance HPL credit under CCS Leave Rules"
		entry_hpl.flags.ignore_permissions = True
		entry_hpl.insert()

		count += 1

	frappe.db.commit()
	return {"credited_employees": count}
