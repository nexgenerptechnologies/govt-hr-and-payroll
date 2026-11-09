// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("CEA Claim", {
	refresh(frm) {
	}
});

frappe.ui.form.on("CEA Claim Child Item", {
	tuition_fee(frm, cdt, cdn) { frm.save(); },
	books_notebooks_fee(frm, cdt, cdn) { frm.save(); },
	uniform_fee(frm, cdt, cdn) { frm.save(); },
	hostel_subsidy_claimed(frm, cdt, cdn) { frm.save(); }
});
