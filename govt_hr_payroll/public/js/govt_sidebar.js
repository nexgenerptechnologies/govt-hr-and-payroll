// Copyright (c) 2026, NexGen ERP Technologies and contributors
// Ensures complete statutory HR & Payroll navigation is always visible on Frappe Desk

(function () {
	"use strict";

	const govtMenuModules = [
		{ label: "Payroll", route: "workspaces/Govt Payroll", icon: "payroll" },
		{ label: "Income Tax", route: "workspaces/Govt Income Tax", icon: "calculator" },
		{ label: "Leave Management", route: "workspaces/Govt Leave Management", icon: "calendar" },
		{ label: "Claims & Reimbursements", route: "workspaces/Govt Claims", icon: "heart" },
		{ label: "Tour TA & DA", route: "workspaces/Govt Tour TA DA", icon: "navigation" },
		{ label: "Masters & Settings", route: "workspaces/Govt Masters", icon: "users" }
	];

	const govtMenuDocTypes = [
		{ label: "Pay Bill (Monthly Payroll)", doctype: "Govt Pay Bill", icon: "file-text" },
		{ label: "Supplementary Pay Bill", doctype: "Supplementary Pay Bill", icon: "file-plus" },
		{ label: "Due-Drawn Arrears", doctype: "Due Drawn Arrear", icon: "trending-up" },
		{ label: "Income Tax Statement", doctype: "Govt Income Tax Statement", icon: "calculator" },
		{ label: "Leave Application", doctype: "CCS Leave Application", icon: "calendar" },
		{ label: "DO Part II Order", doctype: "DO Part Two Order", icon: "award" },
		{ label: "Leave Ledger", doctype: "CCS Leave Ledger Entry", icon: "book" },
		{ label: "CEA Claim", doctype: "CEA Claim", icon: "heart" },
		{ label: "Medical Claim (Form MRC-S)", doctype: "CGHS Medical Claim", icon: "activity" },
		{ label: "Tour Movement Order", doctype: "Tour Movement Order", icon: "navigation" },
		{ label: "TA/DA Final Claim", doctype: "TADA Final Claim", icon: "dollar-sign" },
		{ label: "Employee Master", doctype: "Govt Employee", icon: "users" },
		{ label: "CPC Pay Level (1-18)", doctype: "CPC Pay Level", icon: "layers" },
		{ label: "Office Unit (DDO/PAO)", doctype: "Govt Office Unit", icon: "home" },
		{ label: "Payroll Settings", doctype: "Govt Payroll Settings", icon: "settings" }
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
			cur.includes("masters")
		);
	}

	function injectGovtSidebar() {
		if (!isGovtContext()) return;

		const sidebarEl = document.querySelector(".desk-sidebar .sidebar-items, .desk-sidebar, nav.desk-sidebar, .layout-side-section");
		if (!sidebarEl) return;

		// If full items already present, don't duplicate
		if (sidebarEl.querySelector(".govt-full-sidebar-injected")) return;

		// Check if Pay Bill is present in sidebar links
		const hasPayBill = sidebarEl.querySelector('a[href*="govt-pay-bill"], a[href*="Govt%20Pay%20Bill"]');
		if (hasPayBill) return;

		const container = document.createElement("div");
		container.className = "govt-full-sidebar-injected standard-sidebar-section";
		container.style.marginTop = "12px";
		container.style.paddingTop = "8px";
		container.style.borderTop = "1px solid var(--border-color, #e2e8f0)";

		let html = '<div class="sidebar-section-header mb-1" style="font-weight:600;font-size:11px;text-transform:uppercase;color:var(--text-muted);padding:4px 8px;">Statutory Modules</div>';

		govtMenuModules.forEach(function (m) {
			html += `<a class="sidebar-item" href="/desk/${m.route}" onclick="event.preventDefault(); frappe.set_route('${m.route}');" style="display:flex;align-items:center;padding:6px 12px;color:var(--text-color);text-decoration:none;border-radius:6px;font-size:13px;margin-bottom:2px;">
				<span class="sidebar-item-icon" style="margin-right:8px;opacity:0.8;">${frappe.utils.icon ? frappe.utils.icon(m.icon, "sm") : "📁"}</span>
				<span class="sidebar-item-label">${m.label}</span>
			</a>`;
		});

		html += '<div class="sidebar-section-header mt-3 mb-1" style="font-weight:600;font-size:11px;text-transform:uppercase;color:var(--text-muted);padding:4px 8px;">Statutory DocTypes</div>';

		govtMenuDocTypes.forEach(function (d) {
			html += `<a class="sidebar-item" href="/desk/List/${d.doctype}" onclick="event.preventDefault(); frappe.set_route('List', '${d.doctype}');" style="display:flex;align-items:center;padding:6px 12px;color:var(--text-color);text-decoration:none;border-radius:6px;font-size:13px;margin-bottom:2px;">
				<span class="sidebar-item-icon" style="margin-right:8px;opacity:0.8;">${frappe.utils.icon ? frappe.utils.icon(d.icon, "sm") : "📄"}</span>
				<span class="sidebar-item-label">${d.label}</span>
			</a>`;
		});

		container.innerHTML = html;
		sidebarEl.appendChild(container);
	}

	$(document).ready(function () {
		setTimeout(injectGovtSidebar, 600);
		$(document).on("page-change", function () {
			setTimeout(injectGovtSidebar, 300);
		});
		setInterval(injectGovtSidebar, 2000);
	});
})();
