// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Due Drawn Arrear", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Recalculate Arrears"), function() {
				frm.save();
			});
		}
	},
	recalculate_btn(frm) {
		frm.save();
	}
});

frappe.ui.form.on("Due Drawn Arrear Item", {
	due_basic_pay(frm, cdt, cdn) { frm.save(); },
	due_da_rate(frm, cdt, cdn) { frm.save(); },
	due_hra_rate(frm, cdt, cdn) { frm.save(); },
	due_tpt_allowance(frm, cdt, cdn) { frm.save(); },
	drawn_basic_pay(frm, cdt, cdn) { frm.save(); },
	drawn_da_rate(frm, cdt, cdn) { frm.save(); },
	drawn_hra_rate(frm, cdt, cdn) { frm.save(); },
	drawn_tpt_allowance(frm, cdt, cdn) { frm.save(); }
});
