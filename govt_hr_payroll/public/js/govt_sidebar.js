// Copyright (c) 2026, NexGen ERP Technologies and contributors
// Provides colorful sidebar navigation and live CCS leave dashboard cards on Desk

(function () {
	"use strict";

	const govtMenuModules = [
		{ label: "Payroll", route: "workspaces/Govt Payroll", icon: "payroll", class: "govt-sidebar-payroll" },
		{ label: "Income Tax", route: "workspaces/Govt Income Tax", icon: "calculator", class: "govt-sidebar-tax" },
		{ label: "Leave Management", route: "workspaces/Govt Leave Management", icon: "calendar", class: "govt-sidebar-leave" },
		{ label: "Claims & Reimbursements", route: "workspaces/Govt Claims", icon: "heart", class: "govt-sidebar-claim" },
		{ label: "Tour TA & DA", route: "workspaces/Govt Tour TA DA", icon: "navigation", class: "govt-sidebar-tour" },
		{ label: "Masters & Settings", route: "workspaces/Govt Masters", icon: "users", class: "govt-sidebar-master" }
	];

	const govtMenuDocTypes = [
		{ label: "Pay Bill (Monthly Payroll)", doctype: "Govt Pay Bill", icon: "file-text", class: "govt-sidebar-payroll" },
		{ label: "Supplementary Pay Bill", doctype: "Supplementary Pay Bill", icon: "file-plus", class: "govt-sidebar-payroll" },
		{ label: "Due-Drawn Arrears", doctype: "Due Drawn Arrear", icon: "trending-up", class: "govt-sidebar-payroll" },
		{ label: "Income Tax Statement", doctype: "Govt Income Tax Statement", icon: "calculator", class: "govt-sidebar-tax" },
		{ label: "Leave Application", doctype: "CCS Leave Application", icon: "calendar", class: "govt-sidebar-leave" },
		{ label: "DO Part II Order", doctype: "DO Part Two Order", icon: "award", class: "govt-sidebar-leave" },
		{ label: "Leave Ledger", doctype: "CCS Leave Ledger Entry", icon: "book", class: "govt-sidebar-leave" },
		{ label: "CEA Claim", doctype: "CEA Claim", icon: "heart", class: "govt-sidebar-claim" },
		{ label: "Medical Claim (Form MRC-S)", doctype: "CGHS Medical Claim", icon: "activity", class: "govt-sidebar-claim" },
		{ label: "Tour Movement Order", doctype: "Tour Movement Order", icon: "navigation", class: "govt-sidebar-tour" },
		{ label: "TA/DA Final Claim", doctype: "TADA Final Claim", icon: "dollar-sign", class: "govt-sidebar-tour" },
		{ label: "Employee Master", doctype: "Govt Employee", icon: "users", class: "govt-sidebar-master" },
		{ label: "CPC Pay Level (1-18)", doctype: "CPC Pay Level", icon: "layers", class: "govt-sidebar-master" },
		{ label: "Office Unit (DDO/PAO)", doctype: "Govt Office Unit", icon: "home", class: "govt-sidebar-master" },
		{ label: "Payroll Settings", doctype: "Govt Payroll Settings", icon: "settings", class: "govt-sidebar-master" }
	];

	function isGovtContext() {
		const cur = frappe.get_route_str ? frappe.get_route_str().toLowerCase() : "";
		return (
			cur.includes("govt") ||
			cur.includes("cpc") ||
			cur.includes("ccs") ||
			cur.includes("due-drawn") ||
			cur.includes("cea") ||
			cur.includes("cghs") ||
			cur.includes("tada") ||
			cur.includes("do-part") ||
			cur.includes("payroll") ||
			cur.includes("masters") ||
			cur === "" ||
			cur === "desk"
		);
	}

	// 1. INJECT COLORED SIDEBAR
	function injectGovtSidebar() {
		const sidebarEl = document.querySelector(".desk-sidebar .sidebar-items, .desk-sidebar, nav.desk-sidebar, .layout-side-section");
		if (!sidebarEl) return;

		// Tag existing items with color classes if present
		document.querySelectorAll(".desk-sidebar a, .layout-side-section a").forEach(function (el) {
			const text = (el.innerText || "").toLowerCase();
			if (text.includes("payroll") || text.includes("pay bill") || text.includes("arrear")) {
				el.classList.add("govt-sidebar-payroll");
			} else if (text.includes("tax")) {
				el.classList.add("govt-sidebar-tax");
			} else if (text.includes("leave") || text.includes("do part")) {
				el.classList.add("govt-sidebar-leave");
			} else if (text.includes("claim") || text.includes("cea") || text.includes("medical")) {
				el.classList.add("govt-sidebar-claim");
			} else if (text.includes("tour") || text.includes("ta/da")) {
				el.classList.add("govt-sidebar-tour");
			} else if (text.includes("master") || text.includes("employee") || text.includes("setting")) {
				el.classList.add("govt-sidebar-master");
			}
		});

		if (sidebarEl.querySelector(".govt-full-sidebar-injected")) return;
		const hasPayBill = sidebarEl.querySelector('a[href*="govt-pay-bill"], a[href*="Govt%20Pay%20Bill"]');
		if (hasPayBill) return;

		const container = document.createElement("div");
		container.className = "govt-full-sidebar-injected standard-sidebar-section";
		container.style.marginTop = "12px";
		container.style.paddingTop = "8px";
		container.style.borderTop = "1px solid var(--border-color, #e2e8f0)";

		let html = '<div class="sidebar-section-header mb-1" style="font-weight:700;font-size:11px;text-transform:uppercase;color:#1e3a8a;padding:4px 8px;">Statutory Modules</div>';

		govtMenuModules.forEach(function (m) {
			html += `<a class="sidebar-item ${m.class}" href="/desk/${m.route}" onclick="event.preventDefault(); frappe.set_route('${m.route}');" style="display:flex;align-items:center;padding:6px 12px;text-decoration:none;border-radius:6px;font-size:13px;margin-bottom:2px;">
				<span class="sidebar-item-icon" style="margin-right:8px;">${frappe.utils.icon ? frappe.utils.icon(m.icon, "sm") : "📁"}</span>
				<span class="sidebar-item-label">${m.label}</span>
			</a>`;
		});

		html += '<div class="sidebar-section-header mt-3 mb-1" style="font-weight:700;font-size:11px;text-transform:uppercase;color:#1e3a8a;padding:4px 8px;">Statutory DocTypes</div>';

		govtMenuDocTypes.forEach(function (d) {
			html += `<a class="sidebar-item ${d.class}" href="/desk/List/${d.doctype}" onclick="event.preventDefault(); frappe.set_route('List', '${d.doctype}');" style="display:flex;align-items:center;padding:6px 12px;text-decoration:none;border-radius:6px;font-size:13px;margin-bottom:2px;">
				<span class="sidebar-item-icon" style="margin-right:8px;">${frappe.utils.icon ? frappe.utils.icon(d.icon, "sm") : "📄"}</span>
				<span class="sidebar-item-label">${d.label}</span>
			</a>`;
		});

		container.innerHTML = html;
		sidebarEl.appendChild(container);
	}

	// 2. RENDER COLORED LEAVE DASHBOARD CARDS ON DESK / WORKSPACE
	let currentDashboardEmployee = null;

	function loadLeaveDashboard(targetEmp) {
		const targetContainer = document.querySelector(".layout-main-section, .workspace-page, .desk-page, .page-container");
		if (!targetContainer) return;

		// Only inject on workspace / desk main pages
		const curRoute = frappe.get_route_str ? frappe.get_route_str() : "";
		if (curRoute.includes("List/") || curRoute.includes("Form/")) {
			const existing = document.getElementById("govt-leave-dashboard-section");
			if (existing) existing.remove();
			return;
		}

		if (document.getElementById("govt-leave-dashboard-section") && !targetEmp) return;

		frappe.call({
			method: "govt_hr_payroll.govt_leave_management.leave_dashboard.get_employee_leave_dashboard",
			args: { employee: targetEmp || currentDashboardEmployee },
			callback: function (r) {
				if (!r || !r.message || !r.message.leave_cards) return;

				const data = r.message;
				currentDashboardEmployee = data.employee ? data.employee.employee_id : null;

				let oldEl = document.getElementById("govt-leave-dashboard-section");
				if (oldEl) oldEl.remove();

				const wrap = document.createElement("div");
				wrap.id = "govt-leave-dashboard-section";
				wrap.className = "govt-leave-dashboard-wrapper";

				// Build Header & Employee Switcher
				let optionsHtml = "";
				if (data.all_employees && data.all_employees.length > 0) {
					data.all_employees.forEach(function (e) {
						const selected = (data.employee && data.employee.employee_id === e.employee_id) ? "selected" : "";
						optionsHtml += `<option value="${e.employee_id}" ${selected}>${e.employee_id} - ${e.employee_name} (${e.designation || 'Staff'})</option>`;
					});
				}

				let empName = data.employee ? `${data.employee.employee_name} (${data.employee.employee_id})` : "General";

				let headerHtml = `
					<div class="govt-leave-dashboard-header">
						<div class="govt-leave-header-title">
							<span>🏛️ Central Civil Services (CCS) Leave Account</span>
							<span class="govt-leave-emp-badge">👤 ${empName}</span>
						</div>
						<div style="display:flex;align-items:center;gap:10px;">
							<label style="font-size:12px;font-weight:600;color:#64748b;margin:0;">Select Official:</label>
							<select class="govt-leave-emp-select" id="govt-leave-emp-dropdown">
								${optionsHtml}
							</select>
							<button class="btn btn-xs btn-default" id="govt-leave-refresh-btn" style="border-radius:6px;font-weight:600;">🔄 Refresh</button>
						</div>
					</div>
				`;

				// Build Cards Grid
				let cardsHtml = '<div class="govt-leave-cards-grid">';
				data.leave_cards.forEach(function (c) {
					const avail = c.available !== undefined ? c.available : 0;
					const taken = c.taken !== undefined ? c.taken : 0;
					const ceil = c.max_ceiling || 0;
					const pct = ceil > 0 ? Math.min(100, Math.round((avail / ceil) * 100)) : 100;

					cardsHtml += `
						<div class="govt-leave-card" style="background:${c.gradient};">
							<div class="govt-leave-card-top">
								<div class="govt-leave-card-title">
									<span>${c.icon}</span>
									<span>${c.leave_name}</span>
								</div>
								<span class="govt-leave-card-badge">${c.note}</span>
							</div>

							<div class="govt-leave-card-metrics">
								<div class="govt-leave-available-lbl">Available Balance</div>
								<div class="govt-leave-available-val">${avail} <span style="font-size:14px;font-weight:500;">${c.unit}</span></div>
								<div class="govt-leave-progress-bg">
									<div class="govt-leave-progress-bar" style="width:${pct}%;"></div>
								</div>
								<div class="govt-leave-taken-val" style="margin-top:8px;">
									<span>Availed: <b>${taken} ${c.unit}</b></span>
									${ceil ? `<span style="opacity:0.8;">| Limit: ${ceil}d</span>` : ''}
								</div>
							</div>

							<div class="govt-leave-card-footer">
								<span style="font-size:11px;font-weight:600;opacity:0.9;">CCS Rules 1972</span>
								<button class="govt-leave-btn-apply" onclick="frappe.new_doc('CCS Leave Application', {employee: '${data.employee ? data.employee.employee_id : ''}', leave_type: '${c.leave_type}'});">
									➕ Apply ${c.leave_code}
								</button>
							</div>
						</div>
					`;
				});
				cardsHtml += '</div>';

				wrap.innerHTML = headerHtml + cardsHtml;

				// Insert at the very top of workspace page
				const mainContent = document.querySelector(".workspace-page, .layout-main-section, .page-container");
				if (mainContent) {
					mainContent.insertBefore(wrap, mainContent.firstChild);
				}

				// Bind Dropdown Change
				const sel = document.getElementById("govt-leave-emp-dropdown");
				if (sel) {
					sel.addEventListener("change", function () {
						loadLeaveDashboard(this.value);
					});
				}
				const refBtn = document.getElementById("govt-leave-refresh-btn");
				if (refBtn) {
					refBtn.addEventListener("click", function () {
						loadLeaveDashboard(sel ? sel.value : null);
					});
				}
			}
		});
	}

	$(document).ready(function () {
		setTimeout(injectGovtSidebar, 600);
		setTimeout(loadLeaveDashboard, 800);

		$(document).on("page-change", function () {
			setTimeout(injectGovtSidebar, 300);
			setTimeout(loadLeaveDashboard, 500);
		});

		setInterval(injectGovtSidebar, 2000);
	});
})();
