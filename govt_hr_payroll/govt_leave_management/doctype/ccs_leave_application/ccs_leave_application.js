// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("CCS Leave Application", {
	setup(frm) {
		frm.set_query("leave_type", function () {
			if (!frm.doc.employee) return {};
			return {
				filters: function() {
					let filters = {};
					return filters;
				}
			};
		});
	},

	refresh(frm) {
		frm.trigger("filter_leave_types");
	},

	employee(frm) {
		if (frm.doc.employee) {
			frappe.db.get_value("Govt Employee", frm.doc.employee, ["gender", "employee_name", "designation", "office_unit"], function (r) {
				if (r) {
					frm.doc.__emp_gender = r.gender;
					frm.trigger("filter_leave_types");
				}
			});
		}
	},

	filter_leave_types(frm) {
		if (!frm.doc.employee) return;
		frappe.db.get_value("Govt Employee", frm.doc.employee, "gender", function (r) {
			if (!r || !r.gender) return;
			const gender = r.gender;
			frm.set_query("leave_type", function () {
				let not_in_list = [];
				if (gender === "Male") {
					not_in_list.push("Maternity Leave");
				} else if (gender === "Female") {
					not_in_list.push("Paternity Leave");
				}
				if (not_in_list.length > 0) {
					return {
						filters: [
							["CCS Leave Type", "leave_type_name", "not in", not_in_list]
						]
					};
				}
				return {};
			});
		});
	},

	leave_type(frm) {
		if (frm.doc.employee && frm.doc.leave_type) {
			frappe.call({
				method: "govt_hr_payroll.govt_leave_management.doctype.ccs_leave_application.ccs_leave_application.get_leave_balance",
				args: {
					employee: frm.doc.employee,
					leave_type: frm.doc.leave_type
				},
				callback: function (r) {
					if (r.message !== undefined) {
						frm.set_value("current_balance", r.message);
					}
				}
			});
		}
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
