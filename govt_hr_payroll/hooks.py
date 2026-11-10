app_name = "govt_hr_payroll"
app_title = "Government HR & Payroll"
app_publisher = "NexGen ERP Technologies"
app_description = "Comprehensive 7th CPC Government HR and Payroll System for Frappe Framework v16"
app_email = "support@nexgenerptechnologies.com"
app_license = "mit"

# Installation and migration hooks for automated master setup
after_install = "govt_hr_payroll.setup.install.after_install"
after_migrate = "govt_hr_payroll.setup.install.after_migrate"

# Include client-side desk enhancement
app_include_js = "/assets/govt_hr_payroll/js/govt_sidebar.js"

# Frappe v16 Apps Launcher Screen
add_to_apps_screen = [
	{
		"name": "govt_hr_payroll",
		"logo": "/assets/govt_hr_payroll/images/govt_logo.svg",
		"title": "Government HR & Payroll",
		"route": "/desk/govt-masters",
		"sequence_id": 1
	}
]
