// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Govt Employee", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.add_custom_button(__("Create / View Monthly Pay Bill"), function() {
				frappe.set_route("List", "Govt Pay Bill");
			}, __("Payroll"));
		}
	},

	first_name(frm) {
		frm.trigger("set_full_name");
	},
	last_name(frm) {
		frm.trigger("set_full_name");
	},
	set_full_name(frm) {
		let name = [frm.doc.first_name, frm.doc.last_name].filter(Boolean).join(" ");
		frm.set_value("employee_name", name);
	},

	pay_matrix_level(frm) {
		if (frm.doc.pay_matrix_level) {
			frappe.db.get_value("CPC Pay Level", frm.doc.pay_matrix_level, ["entry_pay", "grade_pay"], function(r) {
				if (r && r.entry_pay) {
					frm.set_value("basic_pay", r.entry_pay);
					frm.trigger("calc_annual_gross");
				}
			});
		}
	},

	cell_no(frm) {
		if (frm.doc.pay_matrix_level && frm.doc.cell_no) {
			frappe.db.get_value("CPC Pay Cell", {
				parent: frm.doc.pay_matrix_level,
				cell_no: frm.doc.cell_no
			}, "basic_pay", function(r) {
				if (r && r.basic_pay) {
					frm.set_value("basic_pay", r.basic_pay);
					frm.trigger("calc_annual_gross");
				}
			});
		}
	},

	cgegis_group(frm) {
		const cgegis_map = {
			"Group A": 120,
			"Group B": 60,
			"Group C": 30,
			"Group D": 15
		};
		if (frm.doc.cgegis_group && cgegis_map[frm.doc.cgegis_group]) {
			frm.set_value("cgegis_monthly_deduction", cgegis_map[frm.doc.cgegis_group]);
		}
	},

	basic_pay(frm) {
		frm.trigger("calc_annual_gross");
	},
	annual_regular_gross(frm) {
		frm.trigger("calc_total_tax_gross");
	},
	leave_encashment_taxable(frm) {
		frm.trigger("calc_total_tax_gross");
	},
	arrears_taxable(frm) {
		frm.trigger("calc_total_tax_gross");
	},
	bonus_taxable(frm) {
		frm.trigger("calc_total_tax_gross");
	},
	cea_received_taxable(frm) {
		frm.trigger("calc_total_tax_gross");
	},
	other_taxable_earnings(frm) {
		frm.trigger("calc_total_tax_gross");
	},

	calc_annual_gross(frm) {
		let bp = flt(frm.doc.basic_pay);
		if (bp > 0 && (!frm.doc.annual_regular_gross || frm.doc.annual_regular_gross === 0)) {
			let da = Math.round(bp * 0.53);
			let tpt = flt(frm.doc.tpt_allowance || 7200);
			let da_tpt = Math.round(tpt * 0.53);
			frm.set_value("annual_regular_gross", (bp + da + tpt + da_tpt) * 12);
		}
		frm.trigger("calc_total_tax_gross");
	},

	calc_total_tax_gross(frm) {
		let total = flt(frm.doc.annual_regular_gross)
			+ flt(frm.doc.leave_encashment_taxable)
			+ flt(frm.doc.arrears_taxable)
			+ flt(frm.doc.bonus_taxable)
			+ flt(frm.doc.cea_received_taxable)
			+ flt(frm.doc.other_taxable_earnings);
		frm.set_value("total_annual_gross_salary", total);
	},

	govt_quarters_availed(frm) {
		if (frm.doc.govt_quarters_availed) {
			frappe.msgprint(__("Government Quarters selected: HRA will be ₹0 on Pay Bill."));
		}
	}
});

frappe.ui.form.on("Govt Employee Hostel Item", {
	child_type(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		if (row.child_type === "Disabled / Divyang Child") {
			frappe.model.set_value(cdt, cdn, "amount", 202500);
		} else {
			frappe.model.set_value(cdt, cdn, "amount", 101250);
		}
	}
});
