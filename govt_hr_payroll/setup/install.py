# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import os
import json
import frappe
from frappe.utils import flt, today

def after_install():
	setup_roles()
	setup_page_workspace_permissions()
	setup_workflow_states()
	setup_workflow_actions()
	setup_workflows()
	setup_cpc_pay_levels()
	setup_payroll_settings()
	setup_default_leave_types()
	setup_workspaces()
	setup_custom_blocks()
	setup_sidebars()
	assign_nitin_roles()

def after_migrate():
	setup_roles()
	setup_page_workspace_permissions()
	setup_workflow_states()
	setup_workflow_actions()
	setup_workflows()
	setup_cpc_pay_levels()
	setup_payroll_settings()
	setup_default_leave_types()
	setup_workspaces()
	setup_custom_blocks()
	setup_sidebars()
	assign_nitin_roles()

def setup_page_workspace_permissions():
	"""
	Grants Read access to standard 'Page', 'Workspace' and 'CCS Leave Ledger Entry' doctypes for Govt HR roles
	so restricted desk users don't encounter 'No permission for Page' error.
	"""
	roles = ["System Manager", "Desk User", "Govt HR Admin", "Dealing Assistant", "Section Officer", "Drawing and Disbursing Officer", "Govt Employee"]
	for doctype in ["Page", "Workspace", "CCS Leave Ledger Entry"]:
		for role in roles:
			try:
				if not frappe.db.exists("Custom DocPerm", {"parent": doctype, "role": role, "permlevel": 0}):
					p = frappe.new_doc("Custom DocPerm")
					p.parent = doctype
					p.parenttype = "DocType"
					p.parentfield = "permissions"
					p.role = role
					p.permlevel = 0
					p.read = 1
					p.flags.ignore_permissions = True
					p.insert()
			except Exception as e:
				frappe.log_error(f"Error setting {doctype} permission for {role}: {e}")
	frappe.db.commit()

def assign_nitin_roles():
	"""
	Automatically grants User 'Nitin' full operational access to the 
	Government HR & Payroll system, while stripping unrelated ERP/stock/accounts roles.
	"""
	try:
		users = frappe.get_all(
			"User",
			filters=[["name", "like", "%nitin%"]],
			fields=["name"]
		)
		if not users:
			users = frappe.get_all(
				"User",
				filters=[["first_name", "like", "%nitin%"]],
				fields=["name"]
			)
		if not users:
			users = frappe.get_all(
				"User",
				filters=[["email", "like", "%nitin%"]],
				fields=["name"]
			)

		for u in users:
			user_doc = frappe.get_doc("User", u.name)
			existing_roles = {r.role for r in user_doc.roles}

			# Ensure primary Government HR roles and Workspace Manager
			target_roles = [
				"System Manager",
				"Desk User",
				"Govt HR Admin",
				"Dealing Assistant",
				"Section Officer",
				"Drawing and Disbursing Officer",
				"Workspace Manager"
			]
			for tr in target_roles:
				if tr not in existing_roles:
					user_doc.append("roles", {"role": tr})

			# Strip other ERP module roles to isolate access to Govt HR & Payroll only
			unwanted_roles = [
				"Accounts User", "Accounts Manager", "Stock User", "Stock Manager",
				"Purchase User", "Purchase Manager", "Sales User", "Sales Manager",
				"Manufacturing User", "Manufacturing Manager", "Projects User"
			]
			user_doc.roles = [r for r in user_doc.roles if r.role not in unwanted_roles]
			user_doc.block_modules = []

			user_doc.flags.ignore_permissions = True
			user_doc.save()

		frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error auto-assigning Govt HR roles to Nitin: {e}")

def setup_roles():
	roles = [
		{"role_name": "Govt Employee", "desk_access": 1},
		{"role_name": "Dealing Assistant", "desk_access": 1},
		{"role_name": "Section Officer", "desk_access": 1},
		{"role_name": "Drawing and Disbursing Officer", "desk_access": 1},
		{"role_name": "Pay and Accounts Officer", "desk_access": 1},
		{"role_name": "Govt HR Admin", "desk_access": 1}
	]
	for r in roles:
		try:
			if not frappe.db.exists("Role", r["role_name"]):
				doc = frappe.new_doc("Role")
				doc.role_name = r["role_name"]
				doc.desk_access = r.get("desk_access", 1)
				doc.flags.ignore_permissions = True
				doc.insert()
		except Exception as e:
			frappe.log_error(f"Error creating role {r['role_name']}: {e}")
	frappe.db.commit()

def setup_workflow_states():
	states = [
		{"workflow_state_name": "Draft", "style": "Primary"},
		{"workflow_state_name": "Under Verification", "style": "Warning"},
		{"workflow_state_name": "Recommended for Sanction", "style": "Info"},
		{"workflow_state_name": "Sanctioned & Passed", "style": "Success"},
		{"workflow_state_name": "Returned to Maker", "style": "Danger"},
		{"workflow_state_name": "Applied", "style": "Primary"},
		{"workflow_state_name": "Scrutinized", "style": "Warning"},
		{"workflow_state_name": "Recommended", "style": "Info"},
		{"workflow_state_name": "Sanctioned", "style": "Success"},
		{"workflow_state_name": "Rejected", "style": "Danger"},
		{"workflow_state_name": "Claim Drafted", "style": "Primary"},
		{"workflow_state_name": "Scrutinized by Office", "style": "Warning"},
		{"workflow_state_name": "Recommended by SO", "style": "Info"},
		{"workflow_state_name": "Sanctioned for Payment", "style": "Success"},
		{"workflow_state_name": "Returned for Rectification", "style": "Danger"}
	]
	for s in states:
		try:
			if not frappe.db.exists("Workflow State", s["workflow_state_name"]):
				doc = frappe.new_doc("Workflow State")
				doc.workflow_state_name = s["workflow_state_name"]
				doc.style = s.get("style", "Primary")
				doc.flags.ignore_permissions = True
				doc.insert()
		except Exception as e:
			frappe.log_error(f"Error creating workflow state {s['workflow_state_name']}: {e}")
	frappe.db.commit()

def setup_workflow_actions():
	actions = [
		"Submit for Verification",
		"Verify & Recommend",
		"Return with Queries",
		"Re-submit for Verification",
		"Sanction & Finalize",
		"Return to SO",
		"Forward for Scrutiny",
		"Recommend Leave",
		"Return to Employee",
		"Sanction Leave",
		"Reject Leave",
		"Submit Claim",
		"Verify Claim",
		"Sanction Claim",
		"Reject Claim",
		"Submit Tour Bill",
		"Audit Tour Claims",
		"Sanction Travel Bill"
	]
	for a in actions:
		try:
			if not frappe.db.exists("Workflow Action Master", a):
				doc = frappe.new_doc("Workflow Action Master")
				doc.workflow_action_name = a
				doc.flags.ignore_permissions = True
				doc.insert()
		except Exception as e:
			frappe.log_error(f"Error creating workflow action {a}: {e}")
	frappe.db.commit()

def setup_workflows():
	workflows_def = [
		{
			"workflow_name": "Govt Pay Bill Approval Matrix",
			"document_type": "Govt Pay Bill",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"states": [
				{"state": "Draft", "doc_status": "0", "allow_edit": "Dealing Assistant"},
				{"state": "Under Verification", "doc_status": "0", "allow_edit": "Section Officer"},
				{"state": "Recommended for Sanction", "doc_status": "0", "allow_edit": "Drawing and Disbursing Officer"},
				{"state": "Sanctioned & Passed", "doc_status": "1", "allow_edit": "Drawing and Disbursing Officer"},
				{"state": "Returned to Maker", "doc_status": "0", "allow_edit": "Dealing Assistant"}
			],
			"transitions": [
				{"state": "Draft", "action": "Submit for Verification", "next_state": "Under Verification", "allowed": "Dealing Assistant"},
				{"state": "Under Verification", "action": "Verify & Recommend", "next_state": "Recommended for Sanction", "allowed": "Section Officer"},
				{"state": "Under Verification", "action": "Return with Queries", "next_state": "Returned to Maker", "allowed": "Section Officer"},
				{"state": "Returned to Maker", "action": "Re-submit for Verification", "next_state": "Under Verification", "allowed": "Dealing Assistant"},
				{"state": "Recommended for Sanction", "action": "Sanction & Finalize", "next_state": "Sanctioned & Passed", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Recommended for Sanction", "action": "Return to SO", "next_state": "Under Verification", "allowed": "Drawing and Disbursing Officer"}
			]
		},
		{
			"workflow_name": "CCS Leave Sanction Matrix",
			"document_type": "CCS Leave Application",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"states": [
				{"state": "Applied", "doc_status": "0", "allow_edit": "Govt Employee"},
				{"state": "Scrutinized", "doc_status": "0", "allow_edit": "Dealing Assistant"},
				{"state": "Recommended", "doc_status": "0", "allow_edit": "Section Officer"},
				{"state": "Sanctioned", "doc_status": "1", "allow_edit": "Drawing and Disbursing Officer"},
				{"state": "Rejected", "doc_status": "0", "allow_edit": "Drawing and Disbursing Officer"}
			],
			"transitions": [
				{"state": "Applied", "action": "Forward for Scrutiny", "next_state": "Scrutinized", "allowed": "Govt Employee"},
				{"state": "Scrutinized", "action": "Recommend Leave", "next_state": "Recommended", "allowed": "Dealing Assistant"},
				{"state": "Scrutinized", "action": "Return to Employee", "next_state": "Applied", "allowed": "Dealing Assistant"},
				{"state": "Recommended", "action": "Sanction Leave", "next_state": "Sanctioned", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Recommended", "action": "Reject Leave", "next_state": "Rejected", "allowed": "Drawing and Disbursing Officer"}
			]
		},
		{
			"workflow_name": "CEA Claim Sanction Matrix",
			"document_type": "CEA Claim",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"states": [
				{"state": "Claim Drafted", "doc_status": "0", "allow_edit": "Govt Employee"},
				{"state": "Scrutinized by Office", "doc_status": "0", "allow_edit": "Dealing Assistant"},
				{"state": "Recommended by SO", "doc_status": "0", "allow_edit": "Section Officer"},
				{"state": "Sanctioned for Payment", "doc_status": "1", "allow_edit": "Drawing and Disbursing Officer"},
				{"state": "Returned for Rectification", "doc_status": "0", "allow_edit": "Dealing Assistant"}
			],
			"transitions": [
				{"state": "Claim Drafted", "action": "Submit Claim", "next_state": "Scrutinized by Office", "allowed": "Govt Employee"},
				{"state": "Scrutinized by Office", "action": "Verify Claim", "next_state": "Recommended by SO", "allowed": "Dealing Assistant"},
				{"state": "Scrutinized by Office", "action": "Return to Employee", "next_state": "Claim Drafted", "allowed": "Dealing Assistant"},
				{"state": "Recommended by SO", "action": "Sanction Claim", "next_state": "Sanctioned for Payment", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Recommended by SO", "action": "Return with Queries", "next_state": "Returned for Rectification", "allowed": "Drawing and Disbursing Officer"}
			]
		},
		{
			"workflow_name": "Tour TADA Sanction Matrix",
			"document_type": "TADA Final Claim",
			"workflow_state_field": "workflow_state",
			"is_active": 1,
			"states": [
				{"state": "Claim Drafted", "doc_status": "0", "allow_edit": "Govt Employee"},
				{"state": "Scrutinized by Office", "doc_status": "0", "allow_edit": "Dealing Assistant"},
				{"state": "Recommended by SO", "doc_status": "0", "allow_edit": "Section Officer"},
				{"state": "Sanctioned for Payment", "doc_status": "1", "allow_edit": "Drawing and Disbursing Officer"},
				{"state": "Returned for Rectification", "doc_status": "0", "allow_edit": "Dealing Assistant"}
			],
			"transitions": [
				{"state": "Claim Drafted", "action": "Submit Tour Bill", "next_state": "Scrutinized by Office", "allowed": "Govt Employee"},
				{"state": "Scrutinized by Office", "action": "Audit Tour Claims", "next_state": "Recommended by SO", "allowed": "Dealing Assistant"},
				{"state": "Recommended by SO", "action": "Sanction Travel Bill", "next_state": "Sanctioned for Payment", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Recommended by SO", "action": "Return with Queries", "next_state": "Returned for Rectification", "allowed": "Drawing and Disbursing Officer"}
			]
		}
	]

	for wf in workflows_def:
		try:
			name = wf["workflow_name"]
			if frappe.db.exists("Workflow", name):
				doc = frappe.get_doc("Workflow", name)
			else:
				doc = frappe.new_doc("Workflow")
				doc.workflow_name = name

			doc.document_type = wf["document_type"]
			doc.workflow_state_field = wf.get("workflow_state_field", "workflow_state")
			doc.is_active = 1
			doc.send_email_alert = 0

			doc.set("states", [])
			for s in wf["states"]:
				doc.append("states", s)

			doc.set("transitions", [])
			for t in wf["transitions"]:
				doc.append("transitions", t)

			doc.flags.ignore_permissions = True
			doc.flags.ignore_mandatory = True
			doc.save()
		except Exception as e:
			frappe.log_error(f"Error setting up workflow {wf['workflow_name']}: {e}")

	frappe.db.commit()

def setup_sidebars():
	items_data = [
		{"type": "Link", "link_type": "Workspace", "link_to": "Govt Masters", "label": "Home", "icon": "home"},
		{"type": "Section Break", "link_type": "", "link_to": "", "label": "Modules", "icon": ""},
		{"type": "Link", "link_type": "Workspace", "link_to": "Govt Payroll", "label": "Payroll", "icon": "payroll"},
		{"type": "Link", "link_type": "Workspace", "link_to": "Govt Income Tax", "label": "Income Tax", "icon": "calculator"},
		{"type": "Link", "link_type": "Workspace", "link_to": "Govt Leave Management", "label": "Leave Management", "icon": "calendar"},
		{"type": "Link", "link_type": "Workspace", "link_to": "Govt Claims", "label": "Claims & Reimbursements", "icon": "heart"},
		{"type": "Link", "link_type": "Workspace", "link_to": "Govt Tour TA DA", "label": "Tour TA & DA", "icon": "navigation"},
		{"type": "Link", "link_type": "Workspace", "link_to": "Govt Masters", "label": "Masters & Settings", "icon": "users"},
		{"type": "Section Break", "link_type": "", "link_to": "", "label": "Statutory DocTypes", "icon": ""},
		{"type": "Link", "link_type": "DocType", "link_to": "Govt Pay Bill", "label": "Pay Bill (Monthly Payroll)", "icon": "file-text"},
		{"type": "Link", "link_type": "DocType", "link_to": "Supplementary Pay Bill", "label": "Supplementary Pay Bill", "icon": "file-plus"},
		{"type": "Link", "link_type": "DocType", "link_to": "Due Drawn Arrear", "label": "Due-Drawn Arrears", "icon": "trending-up"},
		{"type": "Link", "link_type": "DocType", "link_to": "Govt Income Tax Statement", "label": "Income Tax Statement", "icon": "calculator"},
		{"type": "Link", "link_type": "DocType", "link_to": "CCS Leave Application", "label": "Leave Application", "icon": "calendar"},
		{"type": "Link", "link_type": "DocType", "link_to": "DO Part Two Order", "label": "DO Part II Order", "icon": "award"},
		{"type": "Link", "link_type": "DocType", "link_to": "CCS Leave Ledger Entry", "label": "Leave Ledger", "icon": "book"},
		{"type": "Link", "link_type": "DocType", "link_to": "CEA Claim", "label": "CEA Claim", "icon": "heart"},
		{"type": "Link", "link_type": "DocType", "link_to": "CGHS Medical Claim", "label": "Medical Claim (MRC-S)", "icon": "activity"},
		{"type": "Link", "link_type": "DocType", "link_to": "Tour Movement Order", "label": "Tour Movement Order", "icon": "navigation"},
		{"type": "Link", "link_type": "DocType", "link_to": "TADA Final Claim", "label": "TA/DA Claim", "icon": "dollar-sign"},
		{"type": "Link", "link_type": "DocType", "link_to": "Govt Employee", "label": "Employee Master", "icon": "users"},
		{"type": "Link", "link_type": "DocType", "link_to": "CPC Pay Level", "label": "CPC Pay Level (1-18)", "icon": "layers"},
		{"type": "Link", "link_type": "DocType", "link_to": "Govt Office Unit", "label": "Office Unit (DDO/PAO)", "icon": "home"},
		{"type": "Link", "link_type": "DocType", "link_to": "Govt Payroll Settings", "label": "Payroll Settings", "icon": "settings"}
	]

	target_names = [
		("Govt Masters", "Masters & Settings"),
		("Govt Payroll", "Payroll"),
		("Govt Income Tax", "Income Tax"),
		("Govt Leave Management", "Leave Management"),
		("Govt Claims", "Claims & Reimbursements"),
		("Govt Tour TA DA", "Tour TA & DA"),
		("Govt HR & Payroll", "HR & Payroll"),
		("Masters & Settings", "Masters & Settings"),
		("HR & Payroll", "HR & Payroll")
	]

	try:
		# 1. Update Frappe v16 'Sidebar' DocType if present
		if frappe.db.exists("DocType", "Sidebar"):
			for sb_name, sb_title in target_names:
				try:
					if frappe.db.exists("Sidebar", sb_name):
						sb_doc = frappe.get_doc("Sidebar", sb_name)
					else:
						sb_doc = frappe.new_doc("Sidebar")
						sb_doc.name = sb_name

					sb_doc.title = sb_title
					sb_doc.module = sb_name if frappe.db.exists("Module Def", sb_name) else "Govt Masters"
					sb_doc.app = "govt_hr_payroll"
					sb_doc.standard = 1
					sb_doc.is_standard = 1

					sb_doc.set("items", [])
					for idx, itm in enumerate(items_data, 1):
						sb_doc.append("items", {
							"idx": idx,
							"label": itm.get("label"),
							"type": itm.get("type", "DocType"),
							"link_type": itm.get("link_type", "DocType"),
							"link_to": itm.get("link_to", ""),
							"icon": itm.get("icon", "file-text"),
							"hidden": 0
						})

					sb_doc.flags.ignore_permissions = True
					sb_doc.flags.ignore_mandatory = True
					sb_doc.save()
				except Exception as e:
					frappe.log_error(f"Error updating Sidebar {sb_name}: {e}")

			# Remove user-customized override sidebars so standard sidebar takes precedence
			try:
				frappe.db.delete("Sidebar", {"standard": 0})
			except Exception:
				pass

		# 2. Update 'Workspace Sidebar' DocType if present
		if frappe.db.exists("DocType", "Workspace Sidebar"):
			for sb_name, sb_title in target_names:
				try:
					if frappe.db.exists("Workspace Sidebar", sb_name):
						sb_doc = frappe.get_doc("Workspace Sidebar", sb_name)
					else:
						sb_doc = frappe.new_doc("Workspace Sidebar")
						sb_doc.name = sb_name

					sb_doc.sidebar_name = sb_name
					sb_doc.title = sb_title
					sb_doc.module = sb_name if frappe.db.exists("Module Def", sb_name) else "Govt Masters"
					sb_doc.is_standard = 1

					sb_doc.set("items", [])
					for idx, itm in enumerate(items_data, 1):
						sb_doc.append("items", {
							"idx": idx,
							"label": itm.get("label"),
							"type": itm.get("type", "DocType"),
							"link_type": itm.get("link_type", "DocType"),
							"link_to": itm.get("link_to", ""),
							"icon": itm.get("icon", "file-text"),
							"hidden": 0
						})

					sb_doc.flags.ignore_permissions = True
					sb_doc.flags.ignore_mandatory = True
					sb_doc.save()
				except Exception as e:
					frappe.log_error(f"Error updating Workspace Sidebar {sb_name}: {e}")

		frappe.db.commit()
		frappe.clear_cache()
	except Exception as e:
		frappe.log_error(f"Error executing setup_sidebars: {e}")

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

			frappe.db.set_value("Workspace", ws_name, "label", doc.label)
			frappe.db.set_value("Workspace", ws_name, "title", doc.title)
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
			settings.ups_emp_rate = 10.0
			settings.ups_govt_rate = 10.0
			settings.standard_edu_cess = 4.0
			settings.hra_x_rate = 30.0
			settings.hra_y_rate = 20.0
			settings.hra_z_rate = 10.0
			settings.flags.ignore_permissions = True
			settings.flags.ignore_mandatory = True
			settings.insert()
			frappe.db.commit()
		else:
			# Update existing settings if UPS rates not set
			settings = frappe.get_doc("Govt Payroll Settings", "Govt Payroll Settings")
			if not hasattr(settings, "ups_emp_rate") or not settings.ups_emp_rate:
				frappe.db.set_value("Govt Payroll Settings", "Govt Payroll Settings", "ups_emp_rate", 10.0)
			if not hasattr(settings, "ups_govt_rate") or not settings.ups_govt_rate:
				frappe.db.set_value("Govt Payroll Settings", "Govt Payroll Settings", "ups_govt_rate", 10.0)
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
			"leave_type_name": "Casual Leave",
			"leave_code": "CL",
			"max_days_at_a_time": 8,
			"max_accumulation": 8,
			"is_commuted": 0,
			"requires_medical_certificate": 0,
			"description": "Annual quota 8 days. Sundays/holidays not counted."
		},
		{
			"leave_type_name": "Restricted Holiday",
			"leave_code": "RH",
			"max_days_at_a_time": 2,
			"max_accumulation": 2,
			"is_commuted": 0,
			"requires_medical_certificate": 0,
			"description": "Annual quota 2 days from notified list."
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

def setup_custom_blocks():
	"""
	Sets up the native Custom HTML Block 'Govt Leave Dashboard' in Frappe v16.
	"""
	try:
		if not frappe.db.exists("DocType", "Custom HTML Block"):
			return

		if not frappe.db.exists("Custom HTML Block", "Govt Leave Dashboard"):
			doc = frappe.new_doc("Custom HTML Block")
			doc.name = "Govt Leave Dashboard"
		else:
			doc = frappe.get_doc("Custom HTML Block", "Govt Leave Dashboard")

		doc.html = """<div class="govt-ehrms-dashboard-wrapper" id="govt-ehrms-dashboard-section">
	<div class="govt-ehrms-top-bar">
		<div class="govt-ehrms-title-group">
			<span class="govt-ehrms-title">🏛️ Central Civil Services (CCS) Leave & Entitlement Portal</span>
			<span class="govt-ehrms-emp-pill" id="govt-ehrms-emp-badge">👤 Loading Official...</span>
		</div>
		<div class="govt-ehrms-controls">
			<label style="font-size:12px;font-weight:600;color:#64748b;margin:0;">Official:</label>
			<select class="govt-ehrms-select" id="govt-ehrms-emp-select"></select>
			<button class="btn btn-xs btn-default" id="govt-ehrms-refresh-btn" style="border-radius:6px;font-weight:600;padding:5px 10px;">🔄 Refresh</button>
			<button class="btn btn-xs btn-primary" id="govt-ehrms-apply-btn" style="border-radius:6px;font-weight:600;padding:5px 12px;background:#2563eb;color:#fff;">➕ Apply Leave</button>
		</div>
	</div>
	<div class="govt-ehrms-cards-container" id="govt-ehrms-cards-grid"></div>
</div>"""

		doc.style = """.govt-ehrms-dashboard-wrapper { margin: 0 0 24px 0 !important; padding: 16px 20px 20px 20px !important; background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 14px !important; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important; display: block !important; width: 100% !important; box-sizing: border-box !important; }
.govt-ehrms-top-bar { display: flex !important; align-items: center !important; justify-content: space-between !important; flex-wrap: wrap !important; gap: 12px !important; margin-bottom: 16px !important; padding-bottom: 12px !important; border-bottom: 1px solid #f1f5f9 !important; }
.govt-ehrms-title-group { display: flex !important; align-items: center !important; gap: 12px !important; flex-wrap: wrap !important; }
.govt-ehrms-title { font-size: 15px !important; font-weight: 700 !important; color: #0f172a !important; display: flex !important; align-items: center !important; gap: 8px !important; }
.govt-ehrms-emp-pill { display: inline-flex !important; align-items: center !important; gap: 6px !important; padding: 4px 12px !important; background: #f8fafc !important; border: 1px solid #cbd5e1 !important; border-radius: 20px !important; font-size: 12px !important; font-weight: 600 !important; color: #1e3a8a !important; }
.govt-ehrms-controls { display: flex !important; align-items: center !important; gap: 8px !important; flex-wrap: wrap !important; }
.govt-ehrms-select { padding: 5px 12px !important; border-radius: 8px !important; border: 1px solid #cbd5e1 !important; background: #ffffff !important; font-size: 12px !important; font-weight: 600 !important; color: #334155 !important; cursor: pointer !important; }
.govt-ehrms-cards-container { display: grid !important; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)) !important; gap: 14px !important; width: 100% !important; }
.govt-ehrms-card { background: #ffffff !important; border-radius: 12px !important; padding: 18px 12px 14px 12px !important; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; text-align: center !important; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important; transition: transform 0.16s ease, box-shadow 0.16s ease !important; cursor: pointer !important; min-height: 155px !important; box-sizing: border-box !important; }
.govt-ehrms-card:hover { transform: translateY(-3px) !important; box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08) !important; }
.govt-ehrms-card-circle { width: 46px !important; height: 46px !important; border-radius: 50% !important; display: flex !important; align-items: center !important; justify-content: center !important; color: #ffffff !important; margin-bottom: 10px !important; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12) !important; flex-shrink: 0 !important; }
.govt-ehrms-card-title { font-size: 12.5px !important; font-weight: 500 !important; color: #475569 !important; margin-bottom: 5px !important; line-height: 1.25 !important; text-align: center !important; min-height: 32px !important; display: flex !important; align-items: center !important; justify-content: center !important; }
.govt-ehrms-card-number { font-size: 24px !important; font-weight: 800 !important; color: #0f172a !important; margin-bottom: 5px !important; letter-spacing: -0.5px !important; line-height: 1.1 !important; }
.govt-ehrms-card-caption { font-size: 10.5px !important; font-weight: 600 !important; color: #64748b !important; background: #f1f5f9 !important; padding: 3px 8px !important; border-radius: 12px !important; max-width: 95% !important; overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; display: inline-block !important; }"""

		doc.script = """(function(root) {
	if (!root) return;
	const grid = root.querySelector('#govt-ehrms-cards-grid');
	const badge = root.querySelector('#govt-ehrms-emp-badge');
	const select = root.querySelector('#govt-ehrms-emp-select');
	const refBtn = root.querySelector('#govt-ehrms-refresh-btn');
	const applyBtn = root.querySelector('#govt-ehrms-apply-btn');

	let selectedEmp = null;

	const svgs = {
		calendar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>`,
		clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`,
		book: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>`,
		medical_cross: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>`,
		family: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
		star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>`,
		academic: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>`,
		hospital: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>`
	};

	function loadData(emp) {
		frappe.call({
			method: 'govt_hr_payroll.govt_leave_management.leave_dashboard.get_employee_leave_dashboard',
			args: { employee: emp || selectedEmp },
			callback: function(r) {
				if (!r || !r.message) return;
				const data = r.message;
				selectedEmp = data.employee ? data.employee.employee_id : null;

				if (badge && data.employee) {
					badge.textContent = '👤 ' + data.employee.employee_name + ' (' + (data.employee.designation || 'Staff') + ')';
				}

				if (select && data.all_employees && select.options.length === 0) {
					data.all_employees.forEach(function(e) {
						const opt = document.createElement('option');
						opt.value = e.employee_id;
						opt.textContent = e.employee_id + ' - ' + e.employee_name + ' (' + (e.designation || 'Staff') + ')';
						if (selectedEmp === e.employee_id) opt.selected = true;
						select.appendChild(opt);
					});
				}

				if (grid && data.leave_cards) {
					let html = '';
					data.leave_cards.forEach(function(c) {
						const color = c.color || '#0ea5e9';
						const svg = svgs[c.icon_type] || svgs.calendar;
						html += `
							<div class="govt-ehrms-card" data-leave="${c.leave_type || ''}" data-doctype="${c.doctype || ''}" style="border: 2px solid ${color};">
								<div class="govt-ehrms-card-circle" style="background-color: ${color};">
									${svg}
								</div>
								<div class="govt-ehrms-card-title">${c.title}</div>
								<div class="govt-ehrms-card-number">${c.value}</div>
								<div class="govt-ehrms-card-caption">${c.sub_text}</div>
							</div>
						`;
					});
					grid.innerHTML = html;

					grid.querySelectorAll('.govt-ehrms-card').forEach(function(card) {
						card.addEventListener('click', function() {
							const leaveType = this.getAttribute('data-leave');
							const docType = this.getAttribute('data-doctype');
							if (docType) {
								frappe.set_route('List', docType);
							} else if (leaveType) {
								frappe.new_doc('CCS Leave Application', {
									employee: selectedEmp || '',
									leave_type: leaveType
								});
							} else {
								frappe.set_route('List', 'CCS Leave Application');
							}
						});
					});
				}
			}
		});
	}

	if (select) {
		select.addEventListener('change', function() {
			loadData(this.value);
		});
	}
	if (refBtn) {
		refBtn.addEventListener('click', function() {
			loadData(select ? select.value : null);
		});
	}
	if (applyBtn) {
		applyBtn.addEventListener('click', function() {
			frappe.new_doc('CCS Leave Application', { employee: selectedEmp || '' });
		});
	}

	loadData();
})(root_element);"""

		doc.private = 0
		doc.flags.ignore_permissions = True
		doc.save()
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error creating Custom HTML Block Govt Leave Dashboard: {e}")
