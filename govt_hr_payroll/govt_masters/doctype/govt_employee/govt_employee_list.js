// Copyright (c) 2026, NexGen ERP Technologies and contributors
// For license information, please see license.txt

frappe.listview_settings['Govt Employee'] = {
	onload: function (listview) {
		listview.page.add_inner_button(__('Sync HQ ATVP Staff (12)'), function () {
			frappe.call({
				method: 'govt_hr_payroll.setup.install.sync_initial_employees',
				freeze: true,
				freeze_message: __('Syncing 12 Official HQ ATVP Employees & Users...'),
				callback: function (r) {
					frappe.show_alert({
						message: __('✅ 12 Official HQ ATVP Employees, Hierarchy & Accounts synced!'),
						indicator: 'green'
					}, 7);
					listview.refresh();
				}
			});
		}, __('Actions'));
	}
};
