// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Govt Income Tax Statement", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Recalculate Tax"), function() {
				frm.save();
			});
		}
	},
	fetch_salary_btn(frm) {
		frappe.call({
			doc: frm.doc,
			method: "populate_12_months",
			freeze: true,
			freeze_message: __("Populating 12-Month March to February salary ledger..."),
			callback: function() {
				frm.refresh_fields();
			}
		});
	},
	tax_regime(frm) { frm.save(); },
	annual_rent_paid(frm) { frm.save(); }
});
