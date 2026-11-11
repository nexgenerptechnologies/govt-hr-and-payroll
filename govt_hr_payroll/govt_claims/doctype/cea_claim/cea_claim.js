// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("CEA Claim", {
	refresh(frm) {
	},
	no_of_children(frm) {
		if (frm.doc.no_of_children > 3) {
			frappe.msgprint(__("Number of Surviving Children Claimed cannot be more than 3."));
			frm.set_value("no_of_children", 3);
		}
	},
	validate(frm) {
		if (frm.doc.no_of_children > 3) {
			frappe.throw(__("Number of Surviving Children Claimed cannot be more than 3."));
		}
		if (frm.doc.children && frm.doc.children.length > 3) {
			frappe.throw(__("Cannot claim CEA for more than 3 children in a single claim. Found {0} children.").replace("{0}", frm.doc.children.length));
		}
	}
});

frappe.ui.form.on("CEA Claim Child Item", {
	children_add(frm) {
		if (frm.doc.children && frm.doc.children.length > 3) {
			frappe.msgprint(__("Maximum 3 children are allowed in a single CEA claim."));
			frm.doc.children.pop();
			frm.refresh_field("children");
		}
	},
	tuition_fee(frm, cdt, cdn) { frm.save(); },
	books_notebooks_fee(frm, cdt, cdn) { frm.save(); },
	uniform_fee(frm, cdt, cdn) { frm.save(); },
	hostel_subsidy_claimed(frm, cdt, cdn) { frm.save(); }
});
