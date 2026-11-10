// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Govt Employee", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Create / View Monthly Pay Bill"), function() {
				frappe.set_route("List", "Govt Pay Bill");
			}, __("Payroll"));
		}
	},
	first_name(frm) {
		frm.trigger("set_full_name");
	},
	last_name(frm) {
		frm.trigger("set_full_name");
	},
	set_full_name(frm) {
		let name = [frm.doc.first_name, frm.doc.last_name].filter(Boolean).join(" ");
		frm.set_value("employee_name", name);
	},
	govt_quarters_availed(frm) {
		if (frm.doc.govt_quarters_availed) {
			frappe.msgprint(__("Government Quarters selected: HRA will be ₹0 on Pay Bill."));
		}
	}
});
