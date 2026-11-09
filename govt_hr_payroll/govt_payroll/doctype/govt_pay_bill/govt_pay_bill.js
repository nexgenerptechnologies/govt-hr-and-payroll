// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Govt Pay Bill", {
	refresh(frm) {
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__("Fetch Active Employees"), function() {
				frm.trigger("fetch_employees");
			});
			frm.add_custom_button(__("Recalculate Totals"), function() {
				frm.save();
			});
		}
	},

	get_employees_btn(frm) {
		frm.trigger("fetch_employees");
	},

	calculate_bill_btn(frm) {
		frm.save();
	},

	fetch_employees(frm) {
		if (!frm.doc.office_unit) {
			frappe.msgprint(__("Please select an Office / Unit first."));
			return;
		}

		frappe.call({
			doc: frm.doc,
			method: "fetch_active_employees",
			freeze: true,
			freeze_message: __("Fetching active government employees and calculating statutory components..."),
			callback: function(r) {
				if (r.message) {
					frappe.show_alert({
						message: __("{0} employee(s) fetched and calculated successfully.", [r.message.count]),
						indicator: "green"
					});
					frm.refresh_fields();
				}
			}
		});
	}
});

frappe.ui.form.on("Govt Pay Bill Item", {
	basic_pay(frm, cdt, cdn) {
		frm.trigger("recalc_row", cdt, cdn);
	},
	pension_deduction(frm, cdt, cdn) {
		frm.trigger("recalc_row", cdt, cdn);
	},
	da_rate(frm, cdt, cdn) {
		frm.trigger("recalc_row", cdt, cdn);
	},
	hra_rate(frm, cdt, cdn) {
		frm.trigger("recalc_row", cdt, cdn);
	},
	license_fee(frm, cdt, cdn) {
		frm.trigger("recalc_row", cdt, cdn);
	},
	tpt_allowance(frm, cdt, cdn) {
		frm.trigger("recalc_row", cdt, cdn);
	},
	income_tax(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		row.edu_cess = Math.round((row.income_tax || 0) * 0.04);
		frm.refresh_field("items");
	}
});
