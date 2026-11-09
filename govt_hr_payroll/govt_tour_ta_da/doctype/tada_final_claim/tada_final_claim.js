// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("TADA Final Claim", {
	refresh(frm) {
	}
});

frappe.ui.form.on("TADA Journey Item", {
	amount_claimed(frm, cdt, cdn) { frm.save(); }
});

frappe.ui.form.on("TADA Hotel Item", {
	daily_rate_claimed(frm, cdt, cdn) { frm.save(); },
	no_of_days(frm, cdt, cdn) { frm.save(); }
});

frappe.ui.form.on("TADA Food Item", {
	food_amount_claimed(frm, cdt, cdn) { frm.save(); },
	absence_hours(frm, cdt, cdn) { frm.save(); }
});
