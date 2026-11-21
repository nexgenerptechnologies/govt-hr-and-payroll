# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from govt_hr_payroll.setup.install import setup_page_workspace_permissions

def execute():
	"""
	Migration patch to guarantee read permissions on CCS Leave Type,
	CCS Leave Ledger Entry, and CCS Leave Application for Employee Master / Govt Employee roles.
	"""
	setup_page_workspace_permissions()
