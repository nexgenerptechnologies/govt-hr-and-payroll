# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from govt_hr_payroll.setup.install import (
	setup_roles,
	setup_page_workspace_permissions,
	setup_workflow_states,
	setup_workflow_actions,
	setup_workflows,
	assign_nitin_roles,
	setup_initial_employees
)

def execute():
	"""
	Migration patch to ensure all 4 workflows (CCS Leave, CEA Claim, Tour TA/DA, Govt Pay Bill)
	strictly adhere to the official Indian Government process flowcharts provided by the client:
	- CCS Leave: Recommended by Reporting Officer (not Section Officer), Scrutinized by Dealing Assistant, Sanctioned by Competent Authority.
	- CEA Claim: Submitted by Individual, Verified by Dealing Clerk, Countersigned by DDO.
	- Tour TA/DA: Submitted by Claimant, Scrutinized by Office, Countersigned by Controlling Officer, Sanctioned by DDO / PCDA.
	- Govt Pay Bill: Drafted by Dealing Assistant, Verified by Section Officer, Sanctioned by DDO.
	"""
	setup_roles()
	setup_page_workspace_permissions()
	setup_workflow_states()
	setup_workflow_actions()
	setup_workflows()
	assign_nitin_roles()
	setup_initial_employees()
