// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("CCS Leave Application", {
	refresh(frm) {
		frm.trigger("toggle_half_day_fields");
		frm.trigger("add_half_day_button");
	},

	add_half_day_button(frm) {
		// Custom Action Button to apply 0.5 Day Leave easily
		frm.add_custom_button(__("Apply Half Day (0.5d)"), function () {
			frappe.prompt([
				{
					fieldname: "leave_date",
					fieldtype: "Date",
					label: __("Half Day Leave Date"),
					reqd: 1,
					default: frm.doc.from_date || frappe.datetime.get_today()
				},
				{
					fieldname: "session",
					fieldtype: "Select",
					label: __("Session"),
					options: "First Half (Morning Session)\nSecond Half (Afternoon Session)",
					default: "First Half (Morning Session)",
					reqd: 1
				}
			], function (vals) {
				frm.set_value("half_day", 1);
				frm.set_value("half_day_date", vals.leave_date);
				frm.set_value("half_day_session", vals.session.includes("First") ? "First Half" : "Second Half");
				frm.set_value("from_date", vals.leave_date);
				frm.set_value("to_date", vals.leave_date);
				frm.set_value("total_days", 0.5);
				frappe.show_alert({
					message: __("Half Day Leave applied: 0.5 Day on {0} ({1})").format(vals.leave_date, vals.session),
					indicator: "green"
				}, 6);
			}, __("Apply Half Day Leave (0.5 Day)"), __("Set 0.5 Day"));
		}, __("Actions"));
	},

	employee(frm) {
		if (frm.doc.employee) {
			frappe.db.get_value("Govt Employee", frm.doc.employee, ["gender", "employee_name", "designation", "office_unit", "reports_to", "leave_approver"], function (r) {
				if (r) {
					frm.doc.__emp_gender = r.gender;
					if (r.employee_name) frm.set_value("employee_name", r.employee_name);
					if (r.designation) frm.set_value("designation", r.designation);
					if (r.office_unit) frm.set_value("office_unit", r.office_unit);
					if (r.reports_to) frm.set_value("reports_to", r.reports_to);
					if (r.leave_approver) frm.set_value("leave_approver", r.leave_approver);
					if (frm.doc.leave_type) {
						frm.trigger("leave_type");
					}
				}
			});
		}
	},

	half_day(frm) {
		frm.trigger("toggle_half_day_fields");
		if (frm.doc.half_day) {
			const date = frm.doc.half_day_date || frm.doc.from_date || frappe.datetime.get_today();
			frm.set_value("half_day_date", date);
			frm.set_value("from_date", date);
			frm.set_value("to_date", date);
			frm.set_value("total_days", 0.5);
		} else {
			frm.trigger("calculate_days");
		}
	},

	half_day_date(frm) {
		if (frm.doc.half_day && frm.doc.half_day_date) {
			frm.set_value("from_date", frm.doc.half_day_date);
			frm.set_value("to_date", frm.doc.half_day_date);
			frm.set_value("total_days", 0.5);
		}
	},

	toggle_half_day_fields(frm) {
		const is_hd = frm.doc.half_day ? true : false;
		if (frm.fields_dict.half_day_date) {
			frm.toggle_display(["half_day_date", "half_day_session"], is_hd);
			frm.toggle_reqd("half_day_date", is_hd);
		}
	},

	leave_type(frm) {
		if (!frm.doc.leave_type) return;

		// Clarification on Half Pay Leave (HPL) vs Half Day Leave
		if (frm.doc.leave_type === "Half Pay Leave") {
			frappe.show_alert({
				message: __("ℹ️ Note: 'Half Pay Leave' (HPL) is statutory leave with half salary for a FULL day (1 full day absence = 1 day count). If you want half-day absence (0.5 day), click 'Actions' -> 'Apply Half Day (0.5d)'."),
				indicator: "blue"
			}, 7);
		}

		// Friendly Rule Guidance on Gender
		if (frm.doc.employee) {
			frappe.db.get_value("Govt Employee", frm.doc.employee, "gender", function (r) {
				const gender = r ? r.gender : frm.doc.__emp_gender;
				const lt = frm.doc.leave_type;

				if (lt === "Maternity Leave" && gender === "Male") {
					frappe.msgprint({
						title: __("Statutory Rule Notice (CCS Rule 43)"),
						indicator: "orange",
						message: __("<b>Maternity Leave</b> is admissible strictly to <b>Female Government servants</b>.<br><br>The selected employee (<b>{0}</b>) is registered as <b>Male</b>. To apply for Maternity Leave, please select a female employee.").format(frm.doc.employee_name || frm.doc.employee)
					});
				} else if (lt === "Paternity Leave" && gender === "Female") {
					frappe.msgprint({
						title: __("Statutory Rule Notice (CCS Rule 43-A)"),
						indicator: "orange",
						message: __("<b>Paternity Leave</b> is admissible strictly to <b>Male Government servants</b>.<br><br>The selected employee (<b>{0}</b>) is registered as <b>Female</b>.").format(frm.doc.employee_name || frm.doc.employee)
					});
				}
			});
		}

		// Auto-fetch balance
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
		if (frm.doc.half_day) {
			frm.set_value("half_day_date", frm.doc.from_date);
			frm.set_value("to_date", frm.doc.from_date);
			frm.set_value("total_days", 0.5);
		} else {
			frm.trigger("calculate_days");
		}
	},

	to_date(frm) {
		if (!frm.doc.half_day) {
			frm.trigger("calculate_days");
		}
	},

	calculate_days(frm) {
		if (frm.doc.half_day || frm.doc.total_days === 0.5) {
			frm.set_value("total_days", 0.5);
			return;
		}
		if (frm.doc.from_date && frm.doc.to_date) {
			let days = frappe.datetime.get_diff(frm.doc.to_date, frm.doc.from_date) + 1;
			frm.set_value("total_days", days > 0 ? days : 0);
		}
	},

	permission_to_leave_station(frm) {
		if (frm.doc.permission_to_leave_station && !frm.doc.station_leave_address) {
			frappe.msgprint(__("Please enter your station leave address during the leave period."));
		}
	},

	prefix_holidays(frm) {
		if (!frm.doc.prefix_holidays || frm.doc.prefix_holidays === "Nil / None") {
			frm.set_value("prefix_from_date", null);
			frm.set_value("prefix_to_date", null);
		}
	},

	suffix_holidays(frm) {
		if (!frm.doc.suffix_holidays || frm.doc.suffix_holidays === "Nil / None") {
			frm.set_value("suffix_from_date", null);
			frm.set_value("suffix_to_date", null);
		}
	}
});
