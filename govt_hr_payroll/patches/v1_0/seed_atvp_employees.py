# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from govt_hr_payroll.setup.install import setup_initial_employees

def execute():
	setup_initial_employees()
