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
	setup_initial_employees()

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
	setup_initial_employees()

def setup_page_workspace_permissions():
	"""
	Grants Read access to standard 'Page', 'Workspace' and 'CCS Leave Ledger Entry' doctypes for Govt HR roles
	so restricted desk users don't encounter 'No permission for Page' error.
	"""
	roles = ["System Manager", "Desk User", "Govt HR Admin", "Dealing Assistant", "Section Officer", "Reporting Officer", "Competent Authority", "Controlling Officer", "Drawing and Disbursing Officer", "Govt Employee"]
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
				"Reporting Officer",
				"Competent Authority",
				"Controlling Officer",
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
		{"role_name": "Reporting Officer", "desk_access": 1},
		{"role_name": "Competent Authority", "desk_access": 1},
		{"role_name": "Controlling Officer", "desk_access": 1},
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
		{"workflow_state_name": "Recommended by RO", "style": "Info"},
		{"workflow_state_name": "Sanctioned", "style": "Success"},
		{"workflow_state_name": "Rejected", "style": "Danger"},
		{"workflow_state_name": "Returned to Employee", "style": "Danger"},
		{"workflow_state_name": "Claim Drafted", "style": "Primary"},
		{"workflow_state_name": "Scrutinized by Office", "style": "Warning"},
		{"workflow_state_name": "Countersigned by Controlling Officer", "style": "Info"},
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
		"Forward for Recommendation",
		"Recommend Leave",
		"Verify Leave Balance",
		"Return to Employee",
		"Sanction Leave",
		"Reject Leave",
		"Submit Claim",
		"Verify Claim",
		"Countersign & Sanction",
		"Sanction Claim",
		"Reject Claim",
		"Return to Individual",
		"Submit Tour Bill",
		"Audit Tour Claims",
		"Countersign Claim",
		"Sanction Travel Bill",
		"Return to Claimant",
		"Re-submit Leave",
		"Re-submit Claim",
		"Re-submit Tour Bill"
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
				{"state": "Recommended", "doc_status": "0", "allow_edit": "Reporting Officer"},
				{"state": "Sanctioned", "doc_status": "1", "allow_edit": "Competent Authority"},
				{"state": "Rejected", "doc_status": "0", "allow_edit": "Competent Authority"}
			],
			"transitions": [
				{"state": "Applied", "action": "Forward for Scrutiny", "next_state": "Scrutinized", "allowed": "Govt Employee"},
				{"state": "Applied", "action": "Recommend Leave", "next_state": "Recommended", "allowed": "Reporting Officer"},
				{"state": "Scrutinized", "action": "Recommend Leave", "next_state": "Recommended", "allowed": "Reporting Officer"},
				{"state": "Scrutinized", "action": "Verify Leave Balance", "next_state": "Recommended", "allowed": "Dealing Assistant"},
				{"state": "Scrutinized", "action": "Return to Employee", "next_state": "Applied", "allowed": "Dealing Assistant"},
				{"state": "Recommended", "action": "Sanction Leave", "next_state": "Sanctioned", "allowed": "Competent Authority"},
				{"state": "Recommended", "action": "Sanction Leave", "next_state": "Sanctioned", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Recommended", "action": "Reject Leave", "next_state": "Rejected", "allowed": "Competent Authority"},
				{"state": "Recommended", "action": "Reject Leave", "next_state": "Rejected", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Recommended", "action": "Return to Employee", "next_state": "Applied", "allowed": "Reporting Officer"}
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
				{"state": "Sanctioned for Payment", "doc_status": "1", "allow_edit": "Drawing and Disbursing Officer"},
				{"state": "Returned for Rectification", "doc_status": "0", "allow_edit": "Govt Employee"}
			],
			"transitions": [
				{"state": "Claim Drafted", "action": "Submit Claim", "next_state": "Scrutinized by Office", "allowed": "Govt Employee"},
				{"state": "Scrutinized by Office", "action": "Countersign & Sanction", "next_state": "Sanctioned for Payment", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Scrutinized by Office", "action": "Sanction Claim", "next_state": "Sanctioned for Payment", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Scrutinized by Office", "action": "Return to Individual", "next_state": "Returned for Rectification", "allowed": "Dealing Assistant"},
				{"state": "Scrutinized by Office", "action": "Return with Queries", "next_state": "Returned for Rectification", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Returned for Rectification", "action": "Re-submit Claim", "next_state": "Scrutinized by Office", "allowed": "Govt Employee"}
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
				{"state": "Countersigned by Controlling Officer", "doc_status": "0", "allow_edit": "Controlling Officer"},
				{"state": "Sanctioned for Payment", "doc_status": "1", "allow_edit": "Drawing and Disbursing Officer"},
				{"state": "Returned for Rectification", "doc_status": "0", "allow_edit": "Govt Employee"}
			],
			"transitions": [
				{"state": "Claim Drafted", "action": "Submit Tour Bill", "next_state": "Scrutinized by Office", "allowed": "Govt Employee"},
				{"state": "Scrutinized by Office", "action": "Audit Tour Claims", "next_state": "Countersigned by Controlling Officer", "allowed": "Dealing Assistant"},
				{"state": "Scrutinized by Office", "action": "Return to Claimant", "next_state": "Returned for Rectification", "allowed": "Dealing Assistant"},
				{"state": "Countersigned by Controlling Officer", "action": "Countersign Claim", "next_state": "Countersigned by Controlling Officer", "allowed": "Controlling Officer"},
				{"state": "Countersigned by Controlling Officer", "action": "Countersign Claim", "next_state": "Countersigned by Controlling Officer", "allowed": "Reporting Officer"},
				{"state": "Countersigned by Controlling Officer", "action": "Sanction Travel Bill", "next_state": "Sanctioned for Payment", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Countersigned by Controlling Officer", "action": "Return with Queries", "next_state": "Returned for Rectification", "allowed": "Controlling Officer"},
				{"state": "Countersigned by Controlling Officer", "action": "Return with Queries", "next_state": "Returned for Rectification", "allowed": "Drawing and Disbursing Officer"},
				{"state": "Returned for Rectification", "action": "Re-submit Tour Bill", "next_state": "Scrutinized by Office", "allowed": "Govt Employee"}
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

		doc.style = """/* Copyright (c) 2026, NexGen ERP Technologies and contributors */
/* Government HR & Payroll System - Vibrant Desk & Colorful Sidebar Theme */

/* ==========================================================================
   1. HIDE FRAPPE FLOW (NATIVE AI ASSISTANT IN FRAPPE v16)
   ========================================================================== */
.sidebar-flow,
[data-flow-toggle],
flow-launcher,
[data-sidebar-id="flow"],
.desk-sidebar [data-sidebar-id="flow"],
.layout-side-section [data-sidebar-id="flow"],
.sidebar-item[data-action="flow"],
.sidebar-item[data-flow-toggle],
.desk-sidebar [data-label="Flow"],
.desk-sidebar a[href*="flow"],
.sidebar-item:has(svg.es-icon-flow),
.standard-sidebar-item[data-title="Flow"],
.standard-sidebar-section [data-title="Flow"],
li:has(a[href*="/desk#Flow"]),
a[href*="/desk#Flow"] {
	display: none !important;
	visibility: hidden !important;
	opacity: 0 !important;
	pointer-events: none !important;
	height: 0 !important;
	width: 0 !important;
	margin: 0 !important;
	padding: 0 !important;
	overflow: hidden !important;
}

/* ==========================================================================
   2. MODERN COLORFUL SIDEBAR (EXECUTIVE VIBRANT GOVERNMENT DESIGN)
   ========================================================================== */
/* Sidebar Width 285px - Guarantees full label visibility with ZERO truncation */
.layout-side-section,
.desk-sidebar,
.standard-sidebar,
.body-sidebar,
[data-page-route] .layout-side-section,
.page-container .layout-side-section,
.standard-sidebar-section {
	width: 285px !important;
	min-width: 285px !important;
	max-width: 285px !important;
	flex: 0 0 285px !important;
}

/* Sidebar Item Container */
.standard-sidebar .standard-sidebar-item,
.desk-sidebar .standard-sidebar-item,
.layout-side-section .sidebar-item,
.layout-side-section .sidebar-item-container,
.layout-side-section .item-anchor,
.sidebar-item {
	display: flex !important;
	align-items: center !important;
	padding: 7px 10px !important;
	margin: 3px 6px !important;
	border-radius: 8px !important;
	text-decoration: none !important;
	font-weight: 500 !important;
	color: #334155 !important;
	transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
	border-left: 3px solid transparent !important;
	background: transparent !important;
}

.standard-sidebar .standard-sidebar-item:hover,
.desk-sidebar .standard-sidebar-item:hover,
.layout-side-section .sidebar-item:hover,
.sidebar-item:hover {
	background: #f8fafc !important;
	color: #0f172a !important;
	transform: translateX(3px) !important;
}

/* Active / Selected Item */
.standard-sidebar .standard-sidebar-item.selected,
.standard-sidebar .standard-sidebar-item.active,
.desk-sidebar .standard-sidebar-item.selected,
.layout-side-section .sidebar-item.selected,
.sidebar-item.active {
	background: #f1f5f9 !important;
	color: #0f172a !important;
	font-weight: 700 !important;
	border-left: 3.5px solid #2563eb !important;
}

/* Full Labels Without Truncation */
.standard-sidebar .standard-sidebar-item .sidebar-item-label,
.standard-sidebar-item .sidebar-item-label,
.desk-sidebar .sidebar-item-label,
.layout-side-section .sidebar-item-label,
.desk-sidebar .ellipsis,
.layout-side-section .ellipsis,
.standard-sidebar-section .ellipsis,
.sidebar-item-label {
	min-width: 0 !important;
	overflow: visible !important;
	white-space: normal !important;
	text-overflow: clip !important;
	word-break: keep-all !important;
	font-size: 13px !important;
	font-weight: 500 !important;
	color: #1e293b !important;
	line-height: 1.3 !important;
}

/* Sidebar Section Headers */
.desk-sidebar .sidebar-section-header,
.layout-side-section .sidebar-section-header,
.standard-sidebar-section .sidebar-section-header {
	font-size: 11px !important;
	font-weight: 700 !important;
	text-transform: uppercase !important;
	letter-spacing: 0.05em !important;
	color: #94a3b8 !important;
	padding: 12px 14px 6px 14px !important;
}

/* ==========================================================================
   3. VIBRANT COLORFUL MODULE ICON BADGES
   ========================================================================== */
.standard-sidebar .sidebar-item-icon,
.desk-sidebar .sidebar-item-icon,
.layout-side-section .sidebar-item-icon,
.sidebar-item-icon {
	width: 26px !important;
	height: 26px !important;
	min-width: 26px !important;
	border-radius: 7px !important;
	display: inline-flex !important;
	align-items: center !important;
	justify-content: center !important;
	margin-right: 10px !important;
	flex-shrink: 0 !important;
	transition: transform 0.18s ease, box-shadow 0.18s ease !important;
	box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}

.standard-sidebar .sidebar-item-icon svg,
.desk-sidebar .sidebar-item-icon svg,
.layout-side-section .sidebar-item-icon svg,
.sidebar-item-icon svg {
	width: 15px !important;
	height: 15px !important;
	stroke-width: 2 !important;
}

/* Module Specific Colors */
/* 1. Home / Master Desk */
a[href*="govt-masters" i] .sidebar-item-icon,
[data-sidebar-id*="home" i] .sidebar-item-icon,
a[href$="/desk"] .sidebar-item-icon {
	background: #eff6ff !important;
	color: #2563eb !important;
	border: 1px solid #bfdbfe !important;
}

/* 2. Payroll */
a[href*="payroll" i] .sidebar-item-icon,
[data-sidebar-id*="payroll" i] .sidebar-item-icon {
	background: #ecfdf5 !important;
	color: #059669 !important;
	border: 1px solid #a7f3d0 !important;
}

/* 3. Income Tax */
a[href*="tax" i] .sidebar-item-icon,
[data-sidebar-id*="tax" i] .sidebar-item-icon {
	background: #f5f3ff !important;
	color: #7c3aed !important;
	border: 1px solid #ddd6fe !important;
}

/* 4. Leave Management */
a[href*="leave" i] .sidebar-item-icon,
[data-sidebar-id*="leave" i] .sidebar-item-icon {
	background: #ffe4e6 !important;
	color: #e11d48 !important;
	border: 1px solid #fecdd3 !important;
}

/* 5. Claims & Reimbursements */
a[href*="claim" i] .sidebar-item-icon,
[data-sidebar-id*="claim" i] .sidebar-item-icon {
	background: #e0f2fe !important;
	color: #0284c7 !important;
	border: 1px solid #bae6fd !important;
}

/* 6. Tour TA & DA */
a[href*="tour" i] .sidebar-item-icon,
[data-sidebar-id*="tour" i] .sidebar-item-icon {
	background: #fef3c7 !important;
	color: #d97706 !important;
	border: 1px solid #fde68a !important;
}

/* 7. Pay Bill (Monthly Payroll) */
a[href*="pay-bill" i] .sidebar-item-icon,
a[href*="govt_pay_bill" i] .sidebar-item-icon {
	background: #f0fdf4 !important;
	color: #16a34a !important;
	border: 1px solid #bbf7d0 !important;
}

/* 8. Supplementary Pay Bill */
a[href*="supplementary" i] .sidebar-item-icon {
	background: #ccfbf1 !important;
	color: #0f766e !important;
	border: 1px solid #99f6e4 !important;
}

/* 9. Due-Drawn Arrears */
a[href*="due-drawn" i] .sidebar-item-icon,
a[href*="arrear" i] .sidebar-item-icon {
	background: #eff6ff !important;
	color: #3b82f6 !important;
	border: 1px solid #bfdbfe !important;
}

/* 10. DO Part II Order */
a[href*="do-part" i] .sidebar-item-icon {
	background: #fae8ff !important;
	color: #c026d3 !important;
	border: 1px solid #f5d0fe !important;
}

/* 11. Employee Master */
a[href*="employee" i] .sidebar-item-icon {
	background: #e0e7ff !important;
	color: #4338ca !important;
	border: 1px solid #c7d2fe !important;
}

/* ==========================================================================
   4. COMPACT HALF-SIZE e-HRMS LEAVE CARDS (100% VISIBLE WORDS)
   ========================================================================= */
.govt-ehrms-dashboard-wrapper {
	margin: 0 0 12px 0 !important;
	padding: 10px 12px 10px 12px !important;
	background: #ffffff !important;
	border: 1px solid #e2e8f0 !important;
	border-radius: 10px !important;
	box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
	display: block !important;
	clear: both !important;
	width: 100% !important;
	box-sizing: border-box !important;
}

/* Top Bar: Title + Selector */
.govt-ehrms-top-bar {
	display: flex !important;
	align-items: center !important;
	justify-content: space-between !important;
	flex-wrap: wrap !important;
	gap: 6px !important;
	margin-bottom: 8px !important;
	padding-bottom: 6px !important;
	border-bottom: 1px solid #f1f5f9 !important;
}

.govt-ehrms-title-group {
	display: flex !important;
	align-items: center !important;
	gap: 6px !important;
	flex-wrap: wrap !important;
}

.govt-ehrms-title {
	font-size: 12.5px !important;
	font-weight: 700 !important;
	color: #0f172a !important;
	display: flex !important;
	align-items: center !important;
	gap: 5px !important;
	letter-spacing: -0.2px !important;
}

.govt-ehrms-emp-pill {
	display: inline-flex !important;
	align-items: center !important;
	gap: 4px !important;
	padding: 2px 7px !important;
	background: #f8fafc !important;
	border: 1px solid #cbd5e1 !important;
	border-radius: 12px !important;
	font-size: 10.5px !important;
	font-weight: 600 !important;
	color: #1e3a8a !important;
}

.govt-ehrms-controls {
	display: flex !important;
	align-items: center !important;
	gap: 5px !important;
	flex-wrap: wrap !important;
}

.govt-ehrms-select {
	padding: 2px 6px !important;
	border-radius: 6px !important;
	border: 1px solid #cbd5e1 !important;
	background: #ffffff !important;
	font-size: 10.5px !important;
	font-weight: 600 !important;
	color: #334155 !important;
	cursor: pointer !important;
	height: 25px !important;
}

.govt-ehrms-cards-container {
	display: grid !important;
	grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)) !important;
	gap: 6px !important;
	width: 100% !important;
}

/* Individual Card (Half Size / 100% Visible Words) */
.govt-ehrms-card {
	background: #ffffff !important;
	border-radius: 8px !important;
	padding: 6px 3px 6px 3px !important;
	display: flex !important;
	flex-direction: column !important;
	align-items: center !important;
	justify-content: space-between !important;
	text-align: center !important;
	position: relative !important;
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
	transition: transform 0.14s ease, box-shadow 0.14s ease !important;
	cursor: pointer !important;
	min-height: 90px !important;
	max-height: none !important;
	box-sizing: border-box !important;
}

.govt-ehrms-card:hover {
	transform: translateY(-2px) !important;
	box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08) !important;
}

/* Top Centered Circular Icon Badge */
.govt-ehrms-card-circle,
.govt-ehrms-card-badge {
	width: 22px !important;
	height: 22px !important;
	border-radius: 50% !important;
	display: flex !important;
	align-items: center !important;
	justify-content: center !important;
	color: #ffffff !important;
	margin-bottom: 2px !important;
	box-shadow: 0 1px 2px rgba(0, 0, 0, 0.10) !important;
	flex-shrink: 0 !important;
}

.govt-ehrms-card-circle svg,
.govt-ehrms-card-badge svg {
	width: 12px !important;
	height: 12px !important;
}

/* Centered Card Title (Slightly Smaller Font so 100% Words are Visible) */
.govt-ehrms-card-title {
	font-size: 10px !important;
	font-weight: 600 !important;
	color: #334155 !important;
	margin-bottom: 2px !important;
	line-height: 1.15 !important;
	text-align: center !important;
	min-height: 26px !important;
	height: auto !important;
	display: flex !important;
	align-items: center !important;
	justify-content: center !important;
	overflow: visible !important;
	word-break: normal !important;
}

/* Metric Number */
.govt-ehrms-card-number,
.govt-ehrms-card-val {
	font-size: 15px !important;
	font-weight: 800 !important;
	color: #0f172a !important;
	margin-bottom: 2px !important;
	letter-spacing: -0.3px !important;
	line-height: 1.1 !important;
}

/* Caption / Status Pill (Clear Text Without Dots) */
.govt-ehrms-card-caption,
.govt-ehrms-card-sub {
	font-size: 8.5px !important;
	font-weight: 600 !important;
	color: #475569 !important;
	background: #f1f5f9 !important;
	padding: 1.5px 4px !important;
	border-radius: 6px !important;
	max-width: 98% !important;
	overflow: visible !important;
	text-overflow: clip !important;
	white-space: nowrap !important;
	display: inline-block !important;
}


/* ==========================================================================
   5. VIBRANT MODERN GRADIENT SIDEBAR ICON BADGES
   ========================================================================== */
.standard-sidebar .sidebar-item-icon,
.sidebar-item-container .sidebar-item-icon,
.desk-sidebar .sidebar-item-icon,
.sidebar-item-icon {
	width: 28px !important;
	height: 28px !important;
	min-width: 28px !important;
	border-radius: 8px !important;
	display: inline-flex !important;
	align-items: center !important;
	justify-content: center !important;
	margin-right: 10px !important;
	flex-shrink: 0 !important;
	transition: all 0.2s ease !important;
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.10) !important;
}

.standard-sidebar .sidebar-item-icon svg,
.sidebar-item-container .sidebar-item-icon svg,
.desk-sidebar .sidebar-item-icon svg,
.sidebar-item-icon svg {
	width: 15px !important;
	height: 15px !important;
	stroke: #ffffff !important;
	color: #ffffff !important;
	fill: none !important;
	stroke-width: 2 !important;
}

/* Home */
[item-name="Home"] .sidebar-item-icon,
[data-id="Home"] .sidebar-item-icon,
.govt-badge-home .sidebar-item-icon,
a[href$="/desk"] .sidebar-item-icon {
	background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
}

/* Payroll */
[item-name="Payroll"] .sidebar-item-icon,
[data-id="Payroll"] .sidebar-item-icon,
.govt-badge-payroll .sidebar-item-icon,
a[href*="payroll" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #10b981, #059669) !important;
}

/* Income Tax */
[item-name="Income Tax"] .sidebar-item-icon,
[data-id="Income Tax"] .sidebar-item-icon,
.govt-badge-tax .sidebar-item-icon,
a[href*="tax" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important;
}

/* Leave Management */
[item-name*="Leave" i] .sidebar-item-icon,
[data-id*="Leave" i] .sidebar-item-icon,
.govt-badge-leave .sidebar-item-icon,
a[href*="leave" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #f43f5e, #be123c) !important;
}

/* Claims & Reimbursements */
[item-name*="Claim" i] .sidebar-item-icon,
[data-id*="Claim" i] .sidebar-item-icon,
.govt-badge-claim .sidebar-item-icon,
a[href*="claim" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #06b6d4, #0e7490) !important;
}

/* Tour TA & DA */
[item-name*="Tour" i] .sidebar-item-icon,
[data-id*="Tour" i] .sidebar-item-icon,
.govt-badge-tour .sidebar-item-icon,
a[href*="tour" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #f59e0b, #b45309) !important;
}

/* Pay Bill (Monthly Payroll) */
[item-name*="Pay Bill" i] .sidebar-item-icon,
[data-id*="Pay Bill" i] .sidebar-item-icon,
.govt-badge-paybill .sidebar-item-icon,
a[href*="pay-bill" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #22c55e, #15803d) !important;
}

/* Supplementary Pay Bill */
[item-name*="Supplementary" i] .sidebar-item-icon,
[data-id*="Supplementary" i] .sidebar-item-icon,
.govt-badge-supp .sidebar-item-icon,
a[href*="supplementary" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #14b8a6, #0f766e) !important;
}

/* Due-Drawn Arrears */
[item-name*="Due-Drawn" i] .sidebar-item-icon,
[data-id*="Due-Drawn" i] .sidebar-item-icon,
.govt-badge-arrear .sidebar-item-icon,
a[href*="due-drawn" i] .sidebar-item-icon,
a[href*="arrear" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #6366f1, #4338ca) !important;
}

/* Income Tax Statement */
[item-name*="Income Tax Stat" i] .sidebar-item-icon,
[data-id*="Income Tax Stat" i] .sidebar-item-icon,
.govt-badge-taxstmt .sidebar-item-icon {
	background: linear-gradient(135deg, #a855f7, #7e22ce) !important;
}

/* DO Part II Order */
[item-name*="DO Part" i] .sidebar-item-icon,
[data-id*="DO Part" i] .sidebar-item-icon,
.govt-badge-dopart .sidebar-item-icon,
a[href*="do-part" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #ec4899, #be185d) !important;
}
"""

		doc.script = """(function(root) {
	if (!root) return;
	const grid = root.querySelector('#govt-ehrms-cards-grid');
	const badge = root.querySelector('#govt-ehrms-emp-badge');
	const select = root.querySelector('#govt-ehrms-emp-select');
	const refBtn = root.querySelector('#govt-ehrms-refresh-btn');
	const applyBtn = root.querySelector('#govt-ehrms-apply-btn');

	let selectedEmp = null;

	const svgs = {
		calendar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>`,
		clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`,
		book: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>`,
		medical_cross: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>`,
		family: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
		star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>`,
		academic: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>`,
		hospital: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px;"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>`
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


def setup_initial_employees():
	"""
	Seeds the official 12 employees of HQ ATVP with their complete demographic,
	joining, designation, hierarchy (Reporting Officer & Leave Sanctioning Authority),
	User login accounts (default password: Govt@1234), and initial leave ledger credits.
	"""
	try:
		# Ensure Office Unit 'HQ ATVP' exists
		if not frappe.db.exists("Govt Office Unit", "HQ ATVP"):
			ou = frappe.new_doc("Govt Office Unit")
			ou.office_unit_name = "HQ ATVP"
			ou.ministry_dept = "ATVP"
			ou.station_city = "Delhi"
			ou.city_classification = "X"
			ou.ddo_id = "DDO-ATVP-01"
			ou.flags.ignore_permissions = True
			ou.flags.ignore_mandatory = True
			ou.insert()
		else:
			ou = frappe.get_doc("Govt Office Unit", "HQ ATVP")
			ou.ministry_dept = "ATVP"
			ou.city_classification = "X"
			ou.flags.ignore_permissions = True
			ou.save()
		frappe.db.commit()
	except Exception as e:
		frappe.log_error(f"Error ensuring HQ ATVP office unit: {e}")

	employees_data = [
		{
			"employee_id": "B327591",
			"employee_name": "Sachin",
			"first_name": "Sachin",
			"gender": "Male",
			"marital_status": "Married",
			"dob": "1994-02-21",
			"doj": "2021-10-18",
			"doj_in_atvp": "2021-10-13",
			"designation": "DIR",
			"hometown": "Delhi",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-13",
			"basic_pay": 123100,
			"email": "sachin@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Govt HR Admin", "Drawing and Disbursing Officer", "Workspace Manager", "Competent Authority", "Controlling Officer", "Reporting Officer"],
			"reports_to": None,
			"leave_approver": None
		},
		{
			"employee_id": "B289635",
			"employee_name": "Ritik",
			"first_name": "Ritik",
			"gender": "Male",
			"marital_status": "Married",
			"dob": "1990-07-16",
			"doj": "2016-06-08",
			"doj_in_atvp": "2022-03-28",
			"designation": "PM",
			"hometown": "Pune",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-11",
			"basic_pay": 67700,
			"email": "ritik@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Section Officer", "Competent Authority", "Controlling Officer", "Reporting Officer"],
			"reports_to": "B327591", # Sachin (DIR)
			"leave_approver": "B327591" # Sachin (DIR)
		},
		{
			"employee_id": "B253674",
			"employee_name": "Ritu",
			"first_name": "Ritu",
			"gender": "Female",
			"marital_status": "Married",
			"dob": "1975-07-18",
			"doj": "2015-09-19",
			"doj_in_atvp": "2019-12-16",
			"designation": "DPM",
			"hometown": "Howrah",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-10",
			"basic_pay": 56100,
			"email": "ritu@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Section Officer", "Controlling Officer", "Reporting Officer"],
			"reports_to": "B289635", # Ritik (PM)
			"leave_approver": "B327591" # Sachin (DIR)
		},
		{
			"employee_id": "B256973",
			"employee_name": "Ravi",
			"first_name": "Ravi",
			"gender": "Male",
			"marital_status": "Married",
			"dob": "1978-02-08",
			"doj": "1999-02-16",
			"doj_in_atvp": "2020-10-05",
			"designation": "APM",
			"hometown": "Delhi",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-8",
			"basic_pay": 47600,
			"email": "ravi@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Section Officer", "Controlling Officer", "Reporting Officer", "Competent Authority"],
			"reports_to": "B253674", # Ritu (DPM)
			"leave_approver": "B289635" # Ritik (PM)
		},
		{
			"employee_id": "B256983",
			"employee_name": "Rampratap",
			"first_name": "Rampratap",
			"gender": "Male",
			"marital_status": "Married",
			"dob": "1968-03-08",
			"doj": "1993-12-25",
			"doj_in_atvp": "2021-03-05",
			"designation": "PA",
			"hometown": "Sirsa",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-7",
			"basic_pay": 44900,
			"email": "rampratap@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Dealing Assistant"],
			"reports_to": "B327591", # Attached to Sachin (DIR)
			"leave_approver": "B327591" # Sachin (DIR)
		},
		{
			"employee_id": "B583162",
			"employee_name": "Sonu",
			"first_name": "Sonu",
			"gender": "Male",
			"marital_status": "Married",
			"dob": "1985-01-15",
			"doj": "2011-04-22",
			"doj_in_atvp": "2022-04-01",
			"designation": "ASO",
			"hometown": "Jamalpur",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-7",
			"basic_pay": 44900,
			"email": "sonu@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Dealing Assistant", "Reporting Officer"],
			"reports_to": "B256973", # Ravi (APM)
			"leave_approver": "B289635" # Ritik (PM)
		},
		{
			"employee_id": "B576983",
			"employee_name": "Priya",
			"first_name": "Priya",
			"gender": "Female",
			"marital_status": "Married",
			"dob": "1994-10-12",
			"doj": "2021-12-26",
			"doj_in_atvp": "2021-12-21",
			"designation": "ASO",
			"hometown": "Delhi",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-7",
			"basic_pay": 44900,
			"email": "priya@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Dealing Assistant", "Reporting Officer"],
			"reports_to": "B256973", # Ravi (APM)
			"leave_approver": "B289635" # Ritik (PM)
		},
		{
			"employee_id": "B487962",
			"employee_name": "Harsh",
			"first_name": "Harsh",
			"gender": "Male",
			"marital_status": "Unmarried",
			"dob": "1997-02-09",
			"doj": "2023-04-16",
			"doj_in_atvp": "2023-04-13",
			"designation": "ASO",
			"hometown": "Delhi",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-7",
			"basic_pay": 44900,
			"email": "harsh@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Dealing Assistant", "Reporting Officer"],
			"reports_to": "B256973", # Ravi (APM)
			"leave_approver": "B289635" # Ritik (PM)
		},
		{
			"employee_id": "B238769",
			"employee_name": "Shivam",
			"first_name": "Shivam",
			"gender": "Male",
			"marital_status": "Unmarried",
			"dob": "1994-12-13",
			"doj": "2020-11-12",
			"doj_in_atvp": "2020-11-19",
			"designation": "ASO",
			"hometown": "Kerala",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-7",
			"basic_pay": 44900,
			"email": "shivam@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Dealing Assistant"],
			"reports_to": "B256973", # Ravi (APM)
			"leave_approver": "B289635" # Ritik (PM)
		},
		{
			"employee_id": "B672984",
			"employee_name": "Aniket",
			"first_name": "Aniket",
			"gender": "Male",
			"marital_status": "Married",
			"dob": "1988-08-12",
			"doj": "2011-03-18",
			"doj_in_atvp": "2022-01-08",
			"designation": "SSA",
			"hometown": "Patna",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-4",
			"basic_pay": 25500,
			"email": "aniket@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User", "Dealing Assistant"],
			"reports_to": "B583162", # Sonu (ASO)
			"leave_approver": "B256973" # Ravi (APM)
		},
		{
			"employee_id": "B458632",
			"employee_name": "Soniya",
			"first_name": "Soniya",
			"gender": "Female",
			"marital_status": "Married",
			"dob": "1984-12-20",
			"doj": "2011-01-14",
			"doj_in_atvp": "2021-10-14",
			"designation": "JSA",
			"hometown": "Rajsthan",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-2",
			"basic_pay": 19900,
			"email": "soniya@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User"],
			"reports_to": "B576983", # Priya (ASO)
			"leave_approver": "B256973" # Ravi (APM)
		},
		{
			"employee_id": "B238795",
			"employee_name": "Shivani",
			"first_name": "Shivani",
			"gender": "Female",
			"marital_status": "Unmarried",
			"dob": "1994-08-15",
			"doj": "2021-02-26",
			"doj_in_atvp": "2021-02-22",
			"designation": "MTS",
			"hometown": "Jaipur",
			"office_unit": "HQ ATVP",
			"pay_matrix_level": "Level-1",
			"basic_pay": 18000,
			"email": "shivani@atvp.gov.in",
			"roles": ["Govt Employee", "Desk User"],
			"reports_to": "B487962", # Harsh (ASO)
			"leave_approver": "B256973" # Ravi (APM)
		}
	]

	# 1. First Pass: Create Users and Employee Profiles
	for ed in employees_data:
		try:
			email = ed["email"]
			# Create User Account if not exists, or update roles if already exists
			if not frappe.db.exists("User", email):
				u = frappe.new_doc("User")
				u.email = email
				u.first_name = ed["first_name"]
				u.enabled = 1
				u.send_welcome_email = 0
				u.user_type = "System User"
				for role in ed["roles"]:
					u.append("roles", {"role": role})
				u.flags.ignore_permissions = True
				u.insert()
				# Set Default Password: Govt@1234
				try:
					from frappe.utils.password import update_password
					update_password(email, "Govt@1234")
				except Exception:
					pass
			else:
				u = frappe.get_doc("User", email)
				existing_roles = {r.role for r in u.roles}
				changed = False
				for role in ed["roles"]:
					if role not in existing_roles:
						u.append("roles", {"role": role})
						changed = True
				if changed:
					u.flags.ignore_permissions = True
					u.save()

			# Create or Update Govt Employee Record
			emp_id = ed["employee_id"]
			is_new = False
			if not frappe.db.exists("Govt Employee", emp_id):
				emp = frappe.new_doc("Govt Employee")
				emp.employee_id = emp_id
				is_new = True
			else:
				emp = frappe.get_doc("Govt Employee", emp_id)

			emp.employee_name = ed["employee_name"]
			emp.first_name = ed["first_name"]
			emp.user_id = email
			emp.gender = ed["gender"]
			emp.marital_status = ed["marital_status"]
			emp.dob = ed["dob"]
			emp.doj = ed["doj"]
			emp.doj_in_atvp = ed["doj_in_atvp"]
			emp.designation = ed["designation"]
			emp.office_unit = "HQ ATVP"
			emp.pay_matrix_level = ed["pay_matrix_level"]
			emp.basic_pay = ed["basic_pay"]
			emp.hometown = ed["hometown"]
			emp.status = "Active"
			emp.hra_city_class = "X (27% / 30%)"
			emp.tpt_city_type = "Higher TPTA Cities"
			emp.pension_scheme = "NPS (10% + 14%)"
			emp.flags.ignore_permissions = True
			emp.flags.ignore_mandatory = True
			if is_new:
				emp.insert()
			else:
				emp.save()
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Error creating employee {ed['employee_id']}: {e}")

	# 2. Second Pass: Link Hierarchy (reports_to & leave_approver) and seed initial leave ledger
	for ed in employees_data:
		try:
			emp_id = ed["employee_id"]
			if frappe.db.exists("Govt Employee", emp_id):
				emp = frappe.get_doc("Govt Employee", emp_id)
				if ed["reports_to"] and frappe.db.exists("Govt Employee", ed["reports_to"]):
					emp.reports_to = ed["reports_to"]
				if ed["leave_approver"] and frappe.db.exists("Govt Employee", ed["leave_approver"]):
					emp.leave_approver = ed["leave_approver"]
				emp.flags.ignore_permissions = True
				emp.save()

				# Setup initial leave balances if not already present
				initial_leaves = [
					("Earned Leave", 30.0),
					("Casual Leave", 8.0),
					("Half Pay Leave", 20.0),
					("Restricted Holiday", 2.0)
				]
				for lt, days in initial_leaves:
					if not frappe.db.exists("CCS Leave Ledger Entry", {"employee": emp_id, "leave_type": lt, "transaction_type": "Advance Credit"}):
						entry = frappe.new_doc("CCS Leave Ledger Entry")
						entry.employee = emp_id
						entry.leave_type = lt
						entry.posting_date = ed["doj_in_atvp"]
						entry.transaction_type = "Advance Credit"
						entry.credit_days = days
						entry.debit_days = 0.0
						entry.remarks = "Initial Opening Credit Balance for ATVP Service"
						entry.flags.ignore_permissions = True
						entry.insert()
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(f"Error updating hierarchy for {ed['employee_id']}: {e}")

@frappe.whitelist()
def sync_initial_employees():
	"""
	Whitelisted endpoint to allow Administrator / HR Admin to trigger
	the creation / synchronization of the 12 HQ ATVP employees directly from Frappe Desk.
	"""
	setup_initial_employees()
	emps = frappe.get_all("Govt Employee", fields=["employee_id", "employee_name", "designation", "office_unit"])
	return {
		"status": "success",
		"message": f"Successfully synced {len(emps)} employees in Employee Master!",
		"employees": emps
	}

@frappe.whitelist()
def sync_workflows():
	"""
	Whitelisted endpoint to re-apply the official government workflows
	(CCS Leave, CEA Claim, Tour TA/DA, Govt Pay Bill) matching user-provided flowcharts.
	"""
	setup_roles()
	setup_page_workspace_permissions()
	setup_workflow_states()
	setup_workflow_actions()
	setup_workflows()
	assign_nitin_roles()
	return {
		"status": "success",
		"message": "Official Government Workflows synchronized successfully as per provided documents!"
	}

