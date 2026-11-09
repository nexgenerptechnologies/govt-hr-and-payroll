// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("CCS Leave Application", {
	refresh(frm) {
	},
	from_date(frm) {
		frm.trigger("calculate_days");
	},
	to_date(frm) {
		frm.trigger("calculate_days");
	},
	calculate_days(frm) {
		if (frm.doc.from_date && frm.doc.to_date) {
			let days = frappe.datetime.get_diff(frm.doc.to_date, frm.doc.from_date) + 1;
			frm.set_value("total_days", days > 0 ? days : 0);
		}
	},
	permission_to_leave_station(frm) {
		if (frm.doc.permission_to_leave_station && !frm.doc.station_leave_address) {
			frappe.msgprint(__("Please enter your station leave address during the leave period."));
		}
	}
});
