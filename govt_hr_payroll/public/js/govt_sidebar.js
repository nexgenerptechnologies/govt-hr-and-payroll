// Copyright (c) 2026, NexGen ERP Technologies and contributors
// Provides colorful sidebar navigation and e-HRMS style colored leave cards on Desk

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

	// SVG Icons Library matching e-HRMS
	const svgIcons = {
		calendar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>`,
		clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`,
		book: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>`,
		medical_cross: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>`,
		family: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
		star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>`,
		maternity: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="7" r="4"></circle><path d="M6 21v-2a6 6 0 0 1 12 0v2"></path><circle cx="17" cy="14" r="2.5"></circle></svg>`,
		paternity: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><line x1="19" y1="8" x2="19" y2="14"></line><line x1="22" y1="11" x2="16" y2="11"></line></svg>`,
		academic: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>`,
		hospital: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>`
	};

	// 1. ENHANCE SIDEBAR (COLORING & EXPANSION)
	function enhanceGovtSidebar() {
		const sidebarEl = document.querySelector(".desk-sidebar .sidebar-items, .desk-sidebar, nav.desk-sidebar, .layout-side-section");
		if (!sidebarEl) return;

		// Tag all sidebar items with their module color classes
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
			} else if (text.includes("tour") || text.includes("ta/da") || text.includes("ta & da")) {
				el.classList.add("govt-sidebar-tour");
			} else if (text.includes("master") || text.includes("employee") || text.includes("setting") || text.includes("cpc")) {
				el.classList.add("govt-sidebar-master");
			}
		});

		// Only inject if items are missing
		if (sidebarEl.querySelector(".govt-full-sidebar-injected")) return;
		const hasPayBill = sidebarEl.querySelector('a[href*="govt-pay-bill"], a[href*="Govt%20Pay%20Bill"]');
		if (hasPayBill) return;

		const container = document.createElement("div");
		container.className = "govt-full-sidebar-injected standard-sidebar-section";
		container.style.marginTop = "12px";
		container.style.paddingTop = "8px";
		container.style.borderTop = "1px solid var(--border-color, #e2e8f0)";

		let html = '<div class="sidebar-section-header mb-1"><span>🏛️ STATUTORY MODULES</span></div>';

		govtMenuModules.forEach(function (m) {
			html += `<a class="sidebar-item ${m.class}" href="/desk/${m.route}" onclick="event.preventDefault(); frappe.set_route('${m.route}');">
				<span class="sidebar-item-icon">${frappe.utils.icon ? frappe.utils.icon(m.icon, "sm") : "📁"}</span>
				<span class="sidebar-item-label">${m.label}</span>
			</a>`;
		});

		html += '<div class="sidebar-section-header mt-3 mb-1"><span>📄 STATUTORY DOCTYPES</span></div>';

		govtMenuDocTypes.forEach(function (d) {
			html += `<a class="sidebar-item ${d.class}" href="/desk/List/${d.doctype}" onclick="event.preventDefault(); frappe.set_route('List', '${d.doctype}');">
				<span class="sidebar-item-icon">${frappe.utils.icon ? frappe.utils.icon(d.icon, "sm") : "📄"}</span>
				<span class="sidebar-item-label">${d.label}</span>
			</a>`;
		});

		container.innerHTML = html;
		sidebarEl.appendChild(container);
	}

	// 2. RENDER e-HRMS STYLE COLORED CARDS ON WORKSPACE / DESK (EXACT IMAGE 3 ARCHITECTURE)
	let currentDashboardEmployee = null;
	let isFetchingDashboard = false;

	function loadLeaveDashboard(targetEmp) {
		const curRoute = frappe.get_route_str ? frappe.get_route_str() : "";
		// Do not show on doc list or form view
		if (curRoute.includes("List/") || curRoute.includes("Form/") || curRoute.includes("printview")) {
			const existing = document.getElementById("govt-ehrms-dashboard-section");
			if (existing) existing.remove();
			return;
		}

		const layoutMain = document.querySelector(".layout-main-section, .workspace-page, .page-container .page-content");
		if (!layoutMain) return;

		// Prevent duplicate simultaneous calls
		if (isFetchingDashboard) return;
		isFetchingDashboard = true;

		frappe.call({
			method: "govt_hr_payroll.govt_leave_management.leave_dashboard.get_employee_leave_dashboard",
			args: { employee: targetEmp || currentDashboardEmployee },
			callback: function (r) {
				isFetchingDashboard = false;
				if (!r || !r.message || !r.message.leave_cards) return;

				const data = r.message;
				currentDashboardEmployee = data.employee ? data.employee.employee_id : null;

				let oldEl = document.getElementById("govt-ehrms-dashboard-section");
				if (oldEl) oldEl.remove();

				const wrap = document.createElement("div");
				wrap.id = "govt-ehrms-dashboard-section";
				wrap.className = "govt-ehrms-dashboard-wrapper";

				// Employee selector options
				let optionsHtml = "";
				if (data.all_employees && data.all_employees.length > 0) {
					data.all_employees.forEach(function (e) {
						const selected = (data.employee && data.employee.employee_id === e.employee_id) ? "selected" : "";
						optionsHtml += `<option value="${e.employee_id}" ${selected}>${e.employee_id} - ${e.employee_name} (${e.designation || 'Staff'})</option>`;
					});
				}

				let empTitle = data.employee ? `${data.employee.employee_name} (${data.employee.designation || 'Staff'})` : "Government Official";

				// Top Bar
				let topBarHtml = `
					<div class="govt-ehrms-top-bar">
						<div class="govt-ehrms-title-group">
							<span class="govt-ehrms-title">
								<span>🏛️ Central Civil Services (CCS) Leave & Entitlement Portal</span>
							</span>
							<span class="govt-ehrms-emp-pill">👤 ${empTitle}</span>
						</div>
						<div class="govt-ehrms-controls">
							<label style="font-size:12px;font-weight:600;color:#64748b;margin:0;">Official:</label>
							<select class="govt-ehrms-select" id="govt-ehrms-emp-select">
								${optionsHtml}
							</select>
							<button class="btn btn-xs btn-default" id="govt-ehrms-refresh-btn" style="border-radius:6px;font-weight:600;padding:5px 10px;">🔄 Refresh</button>
							<button class="btn btn-xs btn-primary" onclick="frappe.new_doc('CCS Leave Application', {employee: '${currentDashboardEmployee || ''}'});" style="border-radius:6px;font-weight:600;padding:5px 12px;background:#2563eb;color:#fff;">➕ Apply Leave</button>
						</div>
					</div>
				`;

				// Exact Image 3 Card Architecture
				let cardsHtml = '<div class="govt-ehrms-cards-container">';
				data.leave_cards.forEach(function (c) {
					const cardColor = c.color || "#e11d48";
					const iconSvg = svgIcons[c.icon_type] || svgIcons.calendar;

					let clickHandler = "";
					if (c.is_claim && c.doctype) {
						clickHandler = `frappe.set_route('List', '${c.doctype}');`;
					} else {
						clickHandler = `frappe.new_doc('CCS Leave Application', {employee: '${currentDashboardEmployee || ''}', leave_type: '${c.leave_type}'});`;
					}

					cardsHtml += `
						<div class="govt-ehrms-card" style="border: 2px solid ${cardColor};" onclick="${clickHandler}">
							<div class="govt-ehrms-card-circle" style="background-color: ${cardColor};">
								${iconSvg}
							</div>
							<div class="govt-ehrms-card-title">${c.title}</div>
							<div class="govt-ehrms-card-number">${c.value}</div>
							<div class="govt-ehrms-card-caption">${c.sub_text}</div>
						</div>
					`;
				});
				cardsHtml += '</div>';

				wrap.innerHTML = topBarHtml + cardsHtml;

				// Attach at the very top of .layout-main-section
				const target = document.querySelector(".layout-main-section, .workspace-page");
				if (target) {
					target.insertBefore(wrap, target.firstChild);
				}

				// Dropdown change listener
				const sel = document.getElementById("govt-ehrms-emp-select");
				if (sel) {
					sel.addEventListener("change", function () {
						loadLeaveDashboard(this.value);
					});
				}
				const refBtn = document.getElementById("govt-ehrms-refresh-btn");
				if (refBtn) {
					refBtn.addEventListener("click", function () {
						loadLeaveDashboard(sel ? sel.value : null);
					});
				}
			},
			error: function () {
				isFetchingDashboard = false;
			}
		});
	}

	$(document).ready(function () {
		setTimeout(enhanceGovtSidebar, 500);
		setTimeout(loadLeaveDashboard, 700);

		$(document).on("page-change", function () {
			setTimeout(enhanceGovtSidebar, 300);
			setTimeout(loadLeaveDashboard, 500);
		});

		// Ensure persistent rendering if workspace re-renders
		setInterval(function () {
			enhanceGovtSidebar();
			const curRoute = frappe.get_route_str ? frappe.get_route_str() : "";
			if (!curRoute.includes("List/") && !curRoute.includes("Form/")) {
				if (!document.getElementById("govt-ehrms-dashboard-section")) {
					loadLeaveDashboard();
				}
			}
		}, 3000);
	});
})();
