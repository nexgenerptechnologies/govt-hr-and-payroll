# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from govt_hr_payroll.setup.install import sync_all_sidebars_and_roles

def execute():
	"""
	Migration patch to:
	1. Wipe module blocks for Nitin and all 12 employees.
	2. Synchronize all 12 ATVP employees' roles & permissions to match Indian Govt approval workflows.
	3. Synchronize all Workspace Sidebars (Home, Leave Management, Claims & Reimbursements, Tour TA & DA, Payroll, Income Tax).
	4. Reset user-customized workspace/sidebar overrides and clear cache.
	"""
	sync_all_sidebars_and_roles()
