# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe

def after_install():
	setup_cpc_pay_levels()
	setup_payroll_settings()

def after_migrate():
	setup_cpc_pay_levels()
	setup_payroll_settings()

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
