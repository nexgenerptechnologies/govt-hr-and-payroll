// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Supplementary Pay Bill", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Recalculate Totals"), function() {
				frm.save();
			});
		}
	},
	calculate_bill_btn(frm) {
		frm.save();
	}
});
