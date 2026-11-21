// Copyright (c) 2026, NexGen ERP Technologies and contributors
// High-Performance e-HRMS Cards & Vibrant Desk Navigation Engine (Zero-Flicker, Fully Cached, Mutation-Driven)

(function () {
	"use strict";

	// 1. INJECT INLINE STYLESHEET (GUARANTEES IMMEDIATE APPLICATION ACROSS ALL VIEWS)
	function injectGovtStyles() {
		let styleEl = document.getElementById("govt-desk-custom-theme");
		if (!styleEl) {
			styleEl = document.createElement("style");
			styleEl.id = "govt-desk-custom-theme";
			document.head.appendChild(styleEl);
		}

		styleEl.textContent = `/* Copyright (c) 2026, NexGen ERP Technologies and contributors */
/* Government HR & Payroll System - Vibrant Desk & Colorful Sidebar Theme */

/* ==========================================================================
   1. HIDE FRAPPE FLOW (NATIVE AI ASSISTANT IN FRAPPE v16)
   ========================================================================== */
.sidebar-flow,
[data-flow-toggle],
flow-launcher,
[data-sidebar-id="flow"],
.desk-sidebar [data-sidebar-id="flow"],
.layout-side-section [data-sidebar-id="flow"],
.sidebar-item[data-action="flow"],
.sidebar-item[data-flow-toggle],
.desk-sidebar [data-label="Flow"],
.desk-sidebar a[href*="flow"],
.sidebar-item:has(svg.es-icon-flow),
.standard-sidebar-item[data-title="Flow"],
.standard-sidebar-section [data-title="Flow"],
li:has(a[href*="/desk#Flow"]),
a[href*="/desk#Flow"] {
	display: none !important;
	visibility: hidden !important;
	opacity: 0 !important;
	pointer-events: none !important;
	height: 0 !important;
	width: 0 !important;
	margin: 0 !important;
	padding: 0 !important;
	overflow: hidden !important;
}

/* ==========================================================================
   2. MODERN COLORFUL SIDEBAR (EXECUTIVE VIBRANT GOVERNMENT DESIGN)
   ========================================================================== */
/* Sidebar Width 285px - Guarantees full label visibility with ZERO truncation & ZERO SCROLLING */
.layout-side-section,
.desk-sidebar,
.standard-sidebar,
.body-sidebar,
[data-page-route] .layout-side-section,
.page-container .layout-side-section,
.standard-sidebar-section {
	width: 285px !important;
	min-width: 285px !important;
	max-width: 285px !important;
	flex: 0 0 285px !important;
	overflow: hidden !important;
	overflow-y: hidden !important;
}

/* Sidebar Item Container */
.standard-sidebar .standard-sidebar-item,
.desk-sidebar .standard-sidebar-item,
.layout-side-section .sidebar-item,
.layout-side-section .sidebar-item-container,
.layout-side-section .item-anchor,
.sidebar-item {
	display: flex !important;
	align-items: center !important;
	padding: 7px 10px !important;
	margin: 3px 6px !important;
	border-radius: 8px !important;
	text-decoration: none !important;
	font-weight: 500 !important;
	color: #334155 !important;
	transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1) !important;
	border-left: 3px solid transparent !important;
	background: transparent !important;
}

.standard-sidebar .standard-sidebar-item:hover,
.desk-sidebar .standard-sidebar-item:hover,
.layout-side-section .sidebar-item:hover,
.sidebar-item:hover {
	background: #f8fafc !important;
	color: #0f172a !important;
	transform: translateX(3px) !important;
}

/* Active / Selected Item */
.standard-sidebar .standard-sidebar-item.selected,
.standard-sidebar .standard-sidebar-item.active,
.desk-sidebar .standard-sidebar-item.selected,
.layout-side-section .sidebar-item.selected,
.sidebar-item.active {
	background: #f1f5f9 !important;
	color: #0f172a !important;
	font-weight: 700 !important;
	border-left: 3.5px solid #2563eb !important;
}

/* Full Labels Without Truncation */
.standard-sidebar .standard-sidebar-item .sidebar-item-label,
.standard-sidebar-item .sidebar-item-label,
.desk-sidebar .sidebar-item-label,
.layout-side-section .sidebar-item-label,
.desk-sidebar .ellipsis,
.layout-side-section .ellipsis,
.standard-sidebar-section .ellipsis,
.sidebar-item-label {
	min-width: 0 !important;
	overflow: visible !important;
	white-space: normal !important;
	text-overflow: clip !important;
	word-break: keep-all !important;
	font-size: 13px !important;
	font-weight: 500 !important;
	color: #1e293b !important;
	line-height: 1.3 !important;
}

/* Sidebar Section Headers */
.desk-sidebar .sidebar-section-header,
.layout-side-section .sidebar-section-header,
.standard-sidebar-section .sidebar-section-header {
	font-size: 11px !important;
	font-weight: 700 !important;
	text-transform: uppercase !important;
	letter-spacing: 0.05em !important;
	color: #94a3b8 !important;
	padding: 12px 14px 6px 14px !important;
}

/* ==========================================================================
   3. VIBRANT COLORFUL MODULE ICON BADGES
   ========================================================================== */
.standard-sidebar .sidebar-item-icon,
.desk-sidebar .sidebar-item-icon,
.layout-side-section .sidebar-item-icon,
.sidebar-item-icon {
	width: 26px !important;
	height: 26px !important;
	min-width: 26px !important;
	border-radius: 7px !important;
	display: inline-flex !important;
	align-items: center !important;
	justify-content: center !important;
	margin-right: 10px !important;
	flex-shrink: 0 !important;
	transition: transform 0.18s ease, box-shadow 0.18s ease !important;
	box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}

.standard-sidebar .sidebar-item-icon svg,
.desk-sidebar .sidebar-item-icon svg,
.layout-side-section .sidebar-item-icon svg,
.sidebar-item-icon svg {
	width: 15px !important;
	height: 15px !important;
	stroke-width: 2 !important;
}

/* Module Specific Colors */
/* 1. Home / Master Desk */
a[href*="govt-masters" i] .sidebar-item-icon,
[data-sidebar-id*="home" i] .sidebar-item-icon,
a[href$="/desk"] .sidebar-item-icon {
	background: #eff6ff !important;
	color: #2563eb !important;
	border: 1px solid #bfdbfe !important;
}

/* 2. Payroll */
a[href*="payroll" i] .sidebar-item-icon,
[data-sidebar-id*="payroll" i] .sidebar-item-icon {
	background: #ecfdf5 !important;
	color: #059669 !important;
	border: 1px solid #a7f3d0 !important;
}

/* 3. Income Tax */
a[href*="tax" i] .sidebar-item-icon,
[data-sidebar-id*="tax" i] .sidebar-item-icon {
	background: #f5f3ff !important;
	color: #7c3aed !important;
	border: 1px solid #ddd6fe !important;
}

/* 4. Leave Management */
a[href*="leave" i] .sidebar-item-icon,
[data-sidebar-id*="leave" i] .sidebar-item-icon {
	background: #ffe4e6 !important;
	color: #e11d48 !important;
	border: 1px solid #fecdd3 !important;
}

/* 5. Claims & Reimbursements */
a[href*="claim" i] .sidebar-item-icon,
[data-sidebar-id*="claim" i] .sidebar-item-icon {
	background: #e0f2fe !important;
	color: #0284c7 !important;
	border: 1px solid #bae6fd !important;
}

/* 6. Tour TA & DA */
a[href*="tour" i] .sidebar-item-icon,
[data-sidebar-id*="tour" i] .sidebar-item-icon {
	background: #fef3c7 !important;
	color: #d97706 !important;
	border: 1px solid #fde68a !important;
}

/* 7. Pay Bill (Monthly Payroll) */
a[href*="pay-bill" i] .sidebar-item-icon,
a[href*="govt_pay_bill" i] .sidebar-item-icon {
	background: #f0fdf4 !important;
	color: #16a34a !important;
	border: 1px solid #bbf7d0 !important;
}

/* 8. Supplementary Pay Bill */
a[href*="supplementary" i] .sidebar-item-icon {
	background: #ccfbf1 !important;
	color: #0f766e !important;
	border: 1px solid #99f6e4 !important;
}

/* 9. Due-Drawn Arrears */
a[href*="due-drawn" i] .sidebar-item-icon,
a[href*="arrear" i] .sidebar-item-icon {
	background: #eff6ff !important;
	color: #3b82f6 !important;
	border: 1px solid #bfdbfe !important;
}

/* 10. DO Part II Order */
a[href*="do-part" i] .sidebar-item-icon {
	background: #fae8ff !important;
	color: #c026d3 !important;
	border: 1px solid #f5d0fe !important;
}

/* 11. Employee Master */
a[href*="employee" i] .sidebar-item-icon {
	background: #e0e7ff !important;
	color: #4338ca !important;
	border: 1px solid #c7d2fe !important;
}

/* ==========================================================================
   4. COMPACT HALF-SIZE e-HRMS LEAVE CARDS (100% VISIBLE WORDS)
   ========================================================================= */
.govt-ehrms-dashboard-wrapper {
	margin: 0 0 12px 0 !important;
	padding: 10px 12px 10px 12px !important;
	background: #ffffff !important;
	border: 1px solid #e2e8f0 !important;
	border-radius: 10px !important;
	box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
	display: block !important;
	clear: both !important;
	width: 100% !important;
	box-sizing: border-box !important;
}

/* Top Bar: Title + Selector */
.govt-ehrms-top-bar {
	display: flex !important;
	align-items: center !important;
	justify-content: space-between !important;
	flex-wrap: wrap !important;
	gap: 6px !important;
	margin-bottom: 8px !important;
	padding-bottom: 6px !important;
	border-bottom: 1px solid #f1f5f9 !important;
}

.govt-ehrms-title-group {
	display: flex !important;
	align-items: center !important;
	gap: 6px !important;
	flex-wrap: wrap !important;
}

.govt-ehrms-title {
	font-size: 12.5px !important;
	font-weight: 700 !important;
	color: #0f172a !important;
	display: flex !important;
	align-items: center !important;
	gap: 5px !important;
	letter-spacing: -0.2px !important;
}

.govt-ehrms-emp-pill {
	display: inline-flex !important;
	align-items: center !important;
	gap: 4px !important;
	padding: 2px 7px !important;
	background: #f8fafc !important;
	border: 1px solid #cbd5e1 !important;
	border-radius: 12px !important;
	font-size: 10.5px !important;
	font-weight: 600 !important;
	color: #1e3a8a !important;
}

.govt-ehrms-controls {
	display: flex !important;
	align-items: center !important;
	gap: 5px !important;
	flex-wrap: wrap !important;
}

.govt-ehrms-select {
	padding: 2px 6px !important;
	border-radius: 6px !important;
	border: 1px solid #cbd5e1 !important;
	background: #ffffff !important;
	font-size: 10.5px !important;
	font-weight: 600 !important;
	color: #334155 !important;
	cursor: pointer !important;
	height: 25px !important;
}

.govt-ehrms-cards-container {
	display: grid !important;
	grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)) !important;
	gap: 6px !important;
	width: 100% !important;
}

/* Individual Card (Half Size / 100% Visible Words) */
.govt-ehrms-card {
	background: #ffffff !important;
	border-radius: 8px !important;
	padding: 6px 3px 6px 3px !important;
	display: flex !important;
	flex-direction: column !important;
	align-items: center !important;
	justify-content: space-between !important;
	text-align: center !important;
	position: relative !important;
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
	transition: transform 0.14s ease, box-shadow 0.14s ease !important;
	cursor: pointer !important;
	min-height: 90px !important;
	max-height: none !important;
	box-sizing: border-box !important;
}

.govt-ehrms-card:hover {
	transform: translateY(-2px) !important;
	box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08) !important;
}

/* Top Centered Circular Icon Badge */
.govt-ehrms-card-circle,
.govt-ehrms-card-badge {
	width: 22px !important;
	height: 22px !important;
	border-radius: 50% !important;
	display: flex !important;
	align-items: center !important;
	justify-content: center !important;
	color: #ffffff !important;
	margin-bottom: 2px !important;
	box-shadow: 0 1px 2px rgba(0, 0, 0, 0.10) !important;
	flex-shrink: 0 !important;
}

.govt-ehrms-card-circle svg,
.govt-ehrms-card-badge svg {
	width: 12px !important;
	height: 12px !important;
}

/* Centered Card Title (Slightly Smaller Font so 100% Words are Visible) */
.govt-ehrms-card-title {
	font-size: 10px !important;
	font-weight: 600 !important;
	color: #334155 !important;
	margin-bottom: 2px !important;
	line-height: 1.15 !important;
	text-align: center !important;
	min-height: 26px !important;
	height: auto !important;
	display: flex !important;
	align-items: center !important;
	justify-content: center !important;
	overflow: visible !important;
	word-break: normal !important;
}

/* Metric Number */
.govt-ehrms-card-number,
.govt-ehrms-card-val {
	font-size: 15px !important;
	font-weight: 800 !important;
	color: #0f172a !important;
	margin-bottom: 2px !important;
	letter-spacing: -0.3px !important;
	line-height: 1.1 !important;
}

/* Caption / Status Pill (Clear Text Without Dots) */
.govt-ehrms-card-caption,
.govt-ehrms-card-sub {
	font-size: 8.5px !important;
	font-weight: 600 !important;
	color: #475569 !important;
	background: #f1f5f9 !important;
	padding: 1.5px 4px !important;
	border-radius: 6px !important;
	max-width: 98% !important;
	overflow: visible !important;
	text-overflow: clip !important;
	white-space: nowrap !important;
	display: inline-block !important;
}


/* ==========================================================================
   5. VIBRANT MODERN GRADIENT SIDEBAR ICON BADGES
   ========================================================================== */
.standard-sidebar .sidebar-item-icon,
.sidebar-item-container .sidebar-item-icon,
.desk-sidebar .sidebar-item-icon,
.sidebar-item-icon {
	width: 28px !important;
	height: 28px !important;
	min-width: 28px !important;
	border-radius: 8px !important;
	display: inline-flex !important;
	align-items: center !important;
	justify-content: center !important;
	margin-right: 10px !important;
	flex-shrink: 0 !important;
	transition: all 0.2s ease !important;
	box-shadow: 0 1px 3px rgba(0, 0, 0, 0.10) !important;
}

.standard-sidebar .sidebar-item-icon svg,
.sidebar-item-container .sidebar-item-icon svg,
.desk-sidebar .sidebar-item-icon svg,
.sidebar-item-icon svg {
	width: 15px !important;
	height: 15px !important;
	stroke: #ffffff !important;
	color: #ffffff !important;
	fill: none !important;
	stroke-width: 2 !important;
}

/* Home */
[item-name="Home"] .sidebar-item-icon,
[data-id="Home"] .sidebar-item-icon,
.govt-badge-home .sidebar-item-icon,
a[href$="/desk"] .sidebar-item-icon {
	background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
}

/* Payroll */
[item-name="Payroll"] .sidebar-item-icon,
[data-id="Payroll"] .sidebar-item-icon,
.govt-badge-payroll .sidebar-item-icon,
a[href*="payroll" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #10b981, #059669) !important;
}

/* Income Tax */
[item-name="Income Tax"] .sidebar-item-icon,
[data-id="Income Tax"] .sidebar-item-icon,
.govt-badge-tax .sidebar-item-icon,
a[href*="tax" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important;
}

/* Leave Management */
[item-name*="Leave" i] .sidebar-item-icon,
[data-id*="Leave" i] .sidebar-item-icon,
.govt-badge-leave .sidebar-item-icon,
a[href*="leave" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #f43f5e, #be123c) !important;
}

/* Claims & Reimbursements */
[item-name*="Claim" i] .sidebar-item-icon,
[data-id*="Claim" i] .sidebar-item-icon,
.govt-badge-claim .sidebar-item-icon,
a[href*="claim" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #06b6d4, #0e7490) !important;
}

/* Tour TA & DA */
[item-name*="Tour" i] .sidebar-item-icon,
[data-id*="Tour" i] .sidebar-item-icon,
.govt-badge-tour .sidebar-item-icon,
a[href*="tour" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #f59e0b, #b45309) !important;
}

/* Pay Bill (Monthly Payroll) */
[item-name*="Pay Bill" i] .sidebar-item-icon,
[data-id*="Pay Bill" i] .sidebar-item-icon,
.govt-badge-paybill .sidebar-item-icon,
a[href*="pay-bill" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #22c55e, #15803d) !important;
}

/* Supplementary Pay Bill */
[item-name*="Supplementary" i] .sidebar-item-icon,
[data-id*="Supplementary" i] .sidebar-item-icon,
.govt-badge-supp .sidebar-item-icon,
a[href*="supplementary" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #14b8a6, #0f766e) !important;
}

/* Due-Drawn Arrears */
[item-name*="Due-Drawn" i] .sidebar-item-icon,
[data-id*="Due-Drawn" i] .sidebar-item-icon,
.govt-badge-arrear .sidebar-item-icon,
a[href*="due-drawn" i] .sidebar-item-icon,
a[href*="arrear" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #6366f1, #4338ca) !important;
}

/* Income Tax Statement */
[item-name*="Income Tax Stat" i] .sidebar-item-icon,
[data-id*="Income Tax Stat" i] .sidebar-item-icon,
.govt-badge-taxstmt .sidebar-item-icon {
	background: linear-gradient(135deg, #a855f7, #7e22ce) !important;
}

/* DO Part II Order */
[item-name*="DO Part" i] .sidebar-item-icon,
[data-id*="DO Part" i] .sidebar-item-icon,
.govt-badge-dopart .sidebar-item-icon,
a[href*="do-part" i] .sidebar-item-icon {
	background: linear-gradient(135deg, #ec4899, #be185d) !important;
}
`;
	}

	// 2. ENHANCE AND COLORIZE SIDEBAR (DYNAMIC VIBRANT BADGES, NO ELLIPSIS, NO FLOW, NO SCROLLBAR)
	function enhanceGovtSidebar() {
		injectGovtStyles();

		// Remove/hide Frappe Flow buttons
		const flowElements = document.querySelectorAll('.sidebar-flow, [data-flow-toggle], flow-launcher, [data-sidebar-id="flow"], .sidebar-item[data-action="flow"]');
		flowElements.forEach(function (el) {
			el.remove ? el.remove() : (el.style.display = "none");
		});

		const sidebarContainer = document.querySelector(".standard-sidebar-section, .desk-sidebar .standard-sidebar, .layout-side-section .standard-sidebar, .desk-sidebar, .layout-side-section");
		if (!sidebarContainer) return;

		const isStaff = frappe.session && frappe.session.user && frappe.session.user !== "Guest";
		const roles = (frappe.user_roles || []);
		const hasOfficerRole = roles.some(r => ["System Manager", "Workspace Manager", "Govt HR Admin", "Dealing Assistant", "Section Officer", "Drawing and Disbursing Officer", "Pay and Accounts Officer"].includes(r));

		// 1. Purge individual DocTypes to prevent an endlessly long, scrolling sidebar
		const clutterPatterns = [
			"pay bill (monthly", "supplementary pay", "due-drawn arrear", "income tax statement",
			"leave application", "do part ii", "leave ledger", "cea claim", "medical claim",
			"tour movement", "ta/da claim", "tada final", "employee master", "cpc pay level",
			"office unit", "payroll settings", "statutory doctypes", "modules"
		];

		sidebarContainer.querySelectorAll("a, .sidebar-item, .standard-sidebar-item, .sidebar-section-header, .sidebar-item-container").forEach(function(el) {
			const text = (el.innerText || el.getAttribute("item-name") || el.getAttribute("data-id") || "").toLowerCase().trim();
			const href = (el.getAttribute("href") || "").toLowerCase();

			if (text.includes("flow")) {
				el.remove ? el.remove() : (el.style.display = "none");
				return;
			}

			// If general employee (like Shivani), IMMEDIATELY PURGE Payroll and Income Tax
			if (!hasOfficerRole) {
				if (text === "payroll" || href.includes("payroll") || text === "income tax" || href.includes("tax") || text.includes("pay bill") || href.includes("pay_bill") || text.includes("arrear")) {
					el.remove ? el.remove() : (el.style.display = "none");
					return;
				}
			}

			// Purge individual DocTypes (they already exist inside Workspace cards/shortcuts)
			if (clutterPatterns.some(p => text === p || text.startsWith(p) || (href.includes(p) && !href.includes("workspace") && !href.includes("govt-claims") && !href.includes("govt-leave-management") && !href.includes("govt-tour-ta-da") && !href.includes("govt-payroll") && !href.includes("govt-income-tax") && !href.includes("govt-masters")))) {
				if (!text.includes("leave management") && !text.includes("claims & reimbursements") && !text.includes("tour ta & da") && text !== "payroll" && text !== "income tax" && text !== "home") {
					el.remove ? el.remove() : (el.style.display = "none");
					return;
				}
			}
		});

		// 2. Ensure only the exact role-permitted modules exist in the sidebar
		const currentText = Array.from(sidebarContainer.querySelectorAll("a, .sidebar-item, .standard-sidebar-item")).map(el => (el.innerText || "").toLowerCase()).join(" ");

		const expectedModules = [
			{ key: "home", label: "Home", href: "/desk/masters-and-settings/govt-masters", iconClass: "govt-badge-home", iconSvg: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>` },
			{ key: "leave", label: "Leave Management", href: "/desk/leave-management/govt-leave-management", iconClass: "govt-badge-leave", iconSvg: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>` },
			{ key: "claim", label: "Claims & Reimbursements", href: "/desk/claims-and-reimbursements/govt-claims", iconClass: "govt-badge-claim", iconSvg: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>` },
			{ key: "tour", label: "Tour TA & DA", href: "/desk/tour-ta-and-da/govt-tour-ta-da", iconClass: "govt-badge-tour", iconSvg: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg>` }
		];

		if (hasOfficerRole) {
			expectedModules.splice(1, 0, 
				{ key: "payroll", label: "Payroll", href: "/desk/payroll/govt-payroll", iconClass: "govt-badge-payroll", iconSvg: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>` },
				{ key: "tax", label: "Income Tax", href: "/desk/income-tax/govt-income-tax", iconClass: "govt-badge-tax", iconSvg: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><rect x="4" y="2" width="16" height="20" rx="2"></rect><line x1="8" y1="6" x2="16" y2="6"></line><line x1="16" y1="14" x2="16" y2="18"></line><line x1="8" y1="10" x2="8" y2="10.01"></line><line x1="12" y1="10" x2="12" y2="10.01"></line><line x1="16" y1="10" x2="16" y2="10.01"></line><line x1="8" y1="14" x2="8" y2="14.01"></line><line x1="12" y1="14" x2="12" y2="14.01"></line><line x1="8" y1="18" x2="8" y2="18.01"></line><line x1="12" y1="18" x2="12" y2="18.01"></line></svg>` }
			);
		}

		if (isStaff) {
			const targetList = sidebarContainer.querySelector(".standard-sidebar-section, .sidebar-items, ul") || sidebarContainer;
			expectedModules.forEach(function(mod) {
				if (!currentText.includes(mod.key)) {
					const item = document.createElement("a");
					item.className = "standard-sidebar-item sidebar-item " + mod.iconClass;
					item.href = mod.href;
					item.setAttribute("item-name", mod.label);
					item.setAttribute("data-id", mod.label);
					item.innerHTML = `<span class="sidebar-item-icon">${mod.iconSvg}</span><span class="sidebar-item-label">${mod.label}</span>`;
					item.addEventListener("click", function(e) {
						e.preventDefault();
						if (frappe.set_route) {
							const clean = mod.href.replace("/desk/", "").split("/");
							frappe.set_route(...clean);
						} else {
							window.location.href = mod.href;
						}
					});
					targetList.appendChild(item);
				}
			});
		}

		// 3. Re-apply colorful badges to all remaining items
		sidebarContainer.querySelectorAll(".sidebar-item-container, .standard-sidebar-item, a.sidebar-item").forEach(function (el) {
			const text = (el.innerText || el.getAttribute("item-name") || el.getAttribute("data-id") || "").toLowerCase();
			const href = (el.getAttribute("href") || "").toLowerCase();

			if (text.includes("home") || href.endsWith("/desk") || href.endsWith("/desk#")) {
				el.classList.add("govt-badge-home");
			} else if (text.includes("payroll") || href.includes("payroll")) {
				el.classList.add("govt-badge-payroll");
			} else if (text.includes("tax") || href.includes("tax")) {
				el.classList.add("govt-badge-tax");
			} else if (text.includes("leave") || href.includes("leave")) {
				el.classList.add("govt-badge-leave");
			} else if (text.includes("claim") || href.includes("claim") || text.includes("cea") || text.includes("medical")) {
				el.classList.add("govt-badge-claim");
			} else if (text.includes("tour") || href.includes("tour") || text.includes("ta/da") || text.includes("tada")) {
				el.classList.add("govt-badge-tour");
			}
		});
	}

	// 3. SVG ICONS LIBRARY (12px CRISP SIZE)
	const svgIcons = {
		calendar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>`,
		clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px;"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`,
		book: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>`,
		medical_cross: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px;"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>`,
		family: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px;"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
		star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>`,
		academic: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px;"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>`,
		hospital: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px;"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>`
	};

	// In-memory cache
	window._govt_leave_cache = window._govt_leave_cache || null;
	let currentDashboardEmployee = null;
	let isFetching = false;

	// 4. FIND ACTIVE VISIBLE WORKSPACE CONTAINER
	function getActiveWorkspaceMainSection() {
		const editorContainers = Array.from(document.querySelectorAll(".editor-js-container, .layout-main-section, .workspace-page")).filter(function (el) {
			return el.offsetParent !== null && !el.closest('[style*="display: none"]');
		});

		if (editorContainers.length > 0) return editorContainers[0];
		return document.querySelector(".layout-main-section");
	}

	// 5. MOUNT ONCE WITH ZERO FLICKER (NO INTERVAL POLLING)
	function mountOrUpdateDashboard() {
		injectGovtStyles();

		const curRoute = frappe.get_route_str ? frappe.get_route_str() : "";

		// If user is at root /desk (apps launcher), automatically route to the main workspace!
		if (!curRoute || curRoute === "apps" || curRoute === "desk") {
			if (frappe.set_route) {
				frappe.set_route("masters-and-settings", "govt-masters");
				return;
			}
		}

		// Do not show on List view, Form view, Printview, etc.
		if (curRoute.includes("List/") || curRoute.includes("Form/") || curRoute.includes("printview") || curRoute.includes("Report/")) {
			const existing = document.getElementById("govt-ehrms-dashboard-section");
			if (existing) existing.remove();
			return;
		}

		const activeMain = getActiveWorkspaceMainSection();
		if (!activeMain) return;

		let dashboardWrap = document.getElementById("govt-ehrms-dashboard-section");
		if (dashboardWrap && dashboardWrap.parentElement === activeMain) {
			return;
		}

		if (!dashboardWrap) {
			dashboardWrap = document.createElement("div");
			dashboardWrap.id = "govt-ehrms-dashboard-section";
			dashboardWrap.className = "govt-ehrms-dashboard-wrapper";
		}

		if (activeMain.firstChild !== dashboardWrap) {
			activeMain.insertBefore(dashboardWrap, activeMain.firstChild);
		}
	}

	// 6. INITIALIZE OBSERVER AND ATTACH EVENT HANDLERS (ZERO POLLING, LIGHTNING FAST)
	$(document).ready(function () {
		injectGovtStyles();
		enhanceGovtSidebar();
		mountOrUpdateDashboard();

		const observer = new MutationObserver(function () {
			enhanceGovtSidebar();
			mountOrUpdateDashboard();
		});

		observer.observe(document.body, { childList: true, subtree: true });

		if (frappe.router && frappe.router.on) {
			frappe.router.on("change", function () {
				injectGovtStyles();
				setTimeout(enhanceGovtSidebar, 50);
				setTimeout(mountOrUpdateDashboard, 100);
			});
		}

		$(document).on("page-change", function () {
			injectGovtStyles();
			setTimeout(enhanceGovtSidebar, 50);
			setTimeout(mountOrUpdateDashboard, 100);
		});

		// Block Ctrl+I for Flow globally
		document.addEventListener("keydown", function (e) {
			if ((e.ctrlKey || e.metaKey) && (e.key === "i" || e.key === "I")) {
				e.preventDefault();
				e.stopPropagation();
			}
		}, true);
	});
})();
