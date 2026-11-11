// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tour Movement Order", {
	refresh(frm) {
	},
	validate(frm) {
		if (frm.doc.places_to_visit && frm.doc.places_to_visit.length > 10) {
			frappe.throw(__("Maximum 10 places of visit are allowed in a single Tour Movement Order."));
		}
	}
});

frappe.ui.form.on("Tour Destination Item", {
	places_to_visit_add(frm) {
		if (frm.doc.places_to_visit && frm.doc.places_to_visit.length > 10) {
			frappe.msgprint(__("Maximum 10 places of visit are allowed in a single Tour Movement Order."));
			frm.doc.places_to_visit.pop();
			frm.refresh_field("places_to_visit");
		}
	},
	station_name(frm, cdt, cdn) {
		sync_stations(frm);
	},
	places_to_visit_remove(frm) {
		sync_stations(frm);
	}
});

function sync_stations(frm) {
	if (frm.doc.places_to_visit && frm.doc.places_to_visit.length > 0) {
		const stations = frm.doc.places_to_visit
			.map(row => (row.station_name || "").trim())
			.filter(name => name.length > 0);
		if (stations.length > 0) {
			frm.set_value("station_to", stations.join(", "));
		}
	}
}
