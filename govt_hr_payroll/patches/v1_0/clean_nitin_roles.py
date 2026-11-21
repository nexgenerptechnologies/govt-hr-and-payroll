# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from govt_hr_payroll.setup.install import assign_nitin_roles

def execute():
	"""
	Migration patch to clean user Nitin's roles and permissions,
	stripping all unrelated business, loan, school, and marketing roles,
	leaving only clean Government HR & Payroll operational roles.
	"""
	assign_nitin_roles()
