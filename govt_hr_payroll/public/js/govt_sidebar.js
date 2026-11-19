// Copyright (c) 2026, NexGen ERP Technologies and contributors
// Provides high-precision e-HRMS cards and vibrant, expanded sidebar on Frappe Desk

(function () {
	"use strict";

	// 1. INJECT INLINE STYLESHEET TO GUARANTEE ZERO CACHE OR 404 ISSUES
	function injectGovtStyles() {
		if (document.getElementById("govt-desk-custom-theme")) return;

		const styleEl = document.createElement("style");
		styleEl.id = "govt-desk-custom-theme";
		styleEl.textContent = `
			/* Desk Sidebar Widening & No Truncation */
			.layout-side-section,
			.desk-sidebar,
			[data-page-route] .layout-side-section,
			.body-sidebar,
			.standard-sidebar-section {
				width: 270px !important;
				min-width: 270px !important;
				max-width: 270px !important;
				flex: 0 0 270px !important;
				background: #ffffff !important;
				border-right: 1px solid #e2e8f0 !important;
				padding-right: 6px !important;
			}
			.desk-sidebar .sidebar-items .sidebar-item,
			.layout-side-section .sidebar-item,
			.layout-side-section .sidebar-item-container,
			.layout-side-section .item-anchor,
			.desk-sidebar .standard-sidebar-item {
				display: flex !important;
				align-items: center !important;
				padding: 8px 12px !important;
				margin: 3px 6px !important;
				border-radius: 9px !important;
				text-decoration: none !important;
				color: #1e293b !important;
				font-weight: 500 !important;
				font-size: 13.5px !important;
				line-height: 1.35 !important;
				border-left: 3px solid transparent !important;
				transition: all 0.18s ease !important;
			}
			.desk-sidebar .sidebar-item-label,
			.layout-side-section .sidebar-item-label,
			.desk-sidebar .ellipsis,
			.layout-side-section .ellipsis,
			.desk-sidebar span.ellipsis,
			.layout-side-section span.ellipsis {
				white-space: normal !important;
				overflow: visible !important;
				text-overflow: clip !important;
				word-break: normal !important;
				font-weight: 500 !important;
				color: #1e293b !important;
				line-height: 1.3 !important;
			}
			.desk-sidebar .sidebar-item-icon,
			.layout-side-section .sidebar-item-icon,
			.sidebar-item-icon {
				width: 28px !important;
				height: 28px !important;
				min-width: 28px !important;
				border-radius: 8px !important;
				display: inline-flex !important;
				align-items: center !important;
				justify-content: center !important;
				margin-right: 11px !important;
				flex-shrink: 0 !important;
				box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
			}
			.desk-sidebar .sidebar-section-header,
			.layout-side-section .sidebar-section-header {
				font-size: 11px !important;
				font-weight: 700 !important;
				text-transform: uppercase !important;
				letter-spacing: 0.06em !important;
				color: #1e3a8a !important;
				padding: 10px 12px 4px 12px !important;
				margin-top: 8px !important;
				border-bottom: 1px solid #f1f5f9 !important;
			}

			/* Sidebar Module Colors */
			.govt-sidebar-payroll .sidebar-item-icon, a[href*="payroll" i] .sidebar-item-icon, a[href*="pay-bill" i] .sidebar-item-icon {
				background: #eff6ff !important; color: #2563eb !important; border: 1px solid #bfdbfe !important;
			}
			.govt-sidebar-tax .sidebar-item-icon, a[href*="tax" i] .sidebar-item-icon {
				background: #f0fdf4 !important; color: #16a34a !important; border: 1px solid #bbf7d0 !important;
			}
			.govt-sidebar-leave .sidebar-item-icon, a[href*="leave" i] .sidebar-item-icon {
				background: #fff1f2 !important; color: #e11d48 !important; border: 1px solid #fecdd3 !important;
			}
			.govt-sidebar-claim .sidebar-item-icon, a[href*="claim" i] .sidebar-item-icon, a[href*="cea" i] .sidebar-item-icon {
				background: #faf5ff !important; color: #9333ea !important; border: 1px solid #e9d5ff !important;
			}
			.govt-sidebar-tour .sidebar-item-icon, a[href*="tour" i] .sidebar-item-icon, a[href*="ta-da" i] .sidebar-item-icon {
				background: #fff7ed !important; color: #ea580c !important; border: 1px solid #fed7aa !important;
			}
			.govt-sidebar-master .sidebar-item-icon, a[href*="master" i] .sidebar-item-icon, a[href*="employee" i] .sidebar-item-icon {
				background: #f8fafc !important; color: #475569 !important; border: 1px solid #cbd5e1 !important;
			}

			/* e-HRMS Cards Architecture */
			.govt-ehrms-dashboard-wrapper {
				margin: 12px 0 24px 0 !important;
				padding: 16px 20px 20px 20px !important;
				background: #ffffff !important;
				border: 1px solid #e2e8f0 !important;
				border-radius: 14px !important;
				box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
				display: block !important;
				clear: both !important;
			}
			.govt-ehrms-top-bar {
				display: flex !important;
				align-items: center !important;
				justify-content: space-between !important;
				flex-wrap: wrap !important;
				gap: 12px !important;
				margin-bottom: 16px !important;
				padding-bottom: 12px !important;
				border-bottom: 1px solid #f1f5f9 !important;
			}
			.govt-ehrms-title-group {
				display: flex !important;
				align-items: center !important;
				gap: 12px !important;
				flex-wrap: wrap !important;
			}
			.govt-ehrms-title {
				font-size: 15px !important;
				font-weight: 700 !important;
				color: #0f172a !important;
				display: flex !important;
				align-items: center !important;
				gap: 8px !important;
			}
			.govt-ehrms-emp-pill {
				display: inline-flex !important;
				align-items: center !important;
				gap: 6px !important;
				padding: 4px 12px !important;
				background: #f8fafc !important;
				border: 1px solid #cbd5e1 !important;
				border-radius: 20px !important;
				font-size: 12px !important;
				font-weight: 600 !important;
				color: #1e3a8a !important;
			}
			.govt-ehrms-controls {
				display: flex !important;
				align-items: center !important;
				gap: 8px !important;
				flex-wrap: wrap !important;
			}
			.govt-ehrms-select {
				padding: 5px 12px !important;
				border-radius: 8px !important;
				border: 1px solid #cbd5e1 !important;
				background: #ffffff !important;
				font-size: 12px !important;
				font-weight: 600 !important;
				color: #334155 !important;
				cursor: pointer !important;
			}
			.govt-ehrms-cards-container {
				display: grid !important;
				grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)) !important;
				gap: 16px !important;
				width: 100% !important;
			}
			.govt-ehrms-card {
				background: #ffffff !important;
				border-radius: 12px !important;
				padding: 20px 14px 16px 14px !important;
				display: flex !important;
				flex-direction: column !important;
				align-items: center !important;
				justify-content: center !important;
				text-align: center !important;
				box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
				transition: transform 0.16s ease, box-shadow 0.16s ease !important;
				cursor: pointer !important;
				min-height: 160px !important;
			}
			.govt-ehrms-card:hover {
				transform: translateY(-3px) !important;
				box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08) !important;
			}
			.govt-ehrms-card-circle {
				width: 48px !important;
				height: 48px !important;
				border-radius: 50% !important;
				display: flex !important;
				align-items: center !important;
				justify-content: center !important;
				color: #ffffff !important;
				margin-bottom: 12px !important;
				box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12) !important;
				flex-shrink: 0 !important;
			}
			.govt-ehrms-card-circle svg {
				width: 22px !important;
				height: 22px !important;
			}
			.govt-ehrms-card-title {
				font-size: 13px !important;
				font-weight: 500 !important;
				color: #475569 !important;
				margin-bottom: 6px !important;
				line-height: 1.25 !important;
				text-align: center !important;
				min-height: 32px !important;
				display: flex !important;
				align-items: center !important;
				justify-content: center !important;
			}
			.govt-ehrms-card-number {
				font-size: 26px !important;
				font-weight: 800 !important;
				color: #0f172a !important;
				margin-bottom: 6px !important;
				letter-spacing: -0.5px !important;
				line-height: 1.1 !important;
			}
			.govt-ehrms-card-caption {
				font-size: 11px !important;
				font-weight: 600 !important;
				color: #64748b !important;
				background: #f1f5f9 !important;
				padding: 3px 8px !important;
				border-radius: 12px !important;
				max-width: 95% !important;
				overflow: hidden !important;
				text-overflow: ellipsis !important;
				white-space: nowrap !important;
				display: inline-block !important;
			}
		`;
		document.head.appendChild(styleEl);
	}

	// SVG Icons
	const svgIcons = {
		calendar: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>`,
		clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`,
		book: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>`,
		medical_cross: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>`,
		family: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
		star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>`,
		academic: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"></path><path d="M6 12v5c3 3 9 3 12 0v-5"></path></svg>`,
		hospital: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>`
	};

	// 2. DEFAULT CARDS DATA (IMMEDIATE RENDER, ZERO DELAY)
	const defaultCardsData = [
		{ id: "leaves_app", title: "Leaves Applied", value: "0", sub_text: "Total Applications", color: "#f43f5e", icon_type: "calendar", doctype: "CCS Leave Application" },
		{ id: "el", title: "Earned Leave (EL)", value: "300", sub_text: "Available | Max 300d", color: "#0ea5e9", icon_type: "calendar", leave_type: "Earned Leave" },
		{ id: "cl", title: "Casual Leave (CL)", value: "8", sub_text: "Available | Quota 8d", color: "#06b6d4", icon_type: "clock", leave_type: "Casual Leave" },
		{ id: "hpl", title: "Half Pay Leave (HPL)", value: "300", sub_text: "Available | Advance 10d", color: "#f97316", icon_type: "book", leave_type: "Half Pay Leave" },
		{ id: "commuted", title: "Commuted Leave", value: "150", sub_text: "Medical (2x HPL)", color: "#22c55e", icon_type: "medical_cross", leave_type: "Commuted Leave" },
		{ id: "ccl", title: "Child Care Leave (CCL)", value: "730", sub_text: "Lifetime: 730 Days", color: "#8b5cf6", icon_type: "family", leave_type: "Child Care Leave" },
		{ id: "cea", title: "Child Education (CEA)", value: "₹33,750", sub_text: "Sanctioned / Claimed", color: "#ef4444", icon_type: "academic", doctype: "CEA Claim" },
		{ id: "cghs", title: "Medical Claim (MRC-S)", value: "₹0", sub_text: "Sanctioned / Claimed", color: "#14b8a6", icon_type: "hospital", doctype: "CGHS Medical Claim" }
	];

	let currentDashboardEmployee = null;
	let isFetching = false;

	// 3. ENHANCE SIDEBAR (NO TRUNCATION, VIBRANT COLORS)
	function enhanceGovtSidebar() {
		injectGovtStyles();
		const sidebarItems = document.querySelectorAll(".desk-sidebar a, .layout-side-section a, .standard-sidebar-item");
		if (!sidebarItems || sidebarItems.length === 0) return;

		sidebarItems.forEach(function (el) {
			const text = (el.innerText || "").toLowerCase();
			const href = (el.getAttribute("href") || "").toLowerCase();

			if (text.includes("payroll") || text.includes("pay bill") || href.includes("payroll") || href.includes("pay-bill")) {
				el.classList.add("govt-sidebar-payroll");
			} else if (text.includes("tax") || href.includes("tax")) {
				el.classList.add("govt-sidebar-tax");
			} else if (text.includes("leave") || text.includes("do part") || href.includes("leave")) {
				el.classList.add("govt-sidebar-leave");
			} else if (text.includes("claim") || text.includes("cea") || text.includes("medical") || href.includes("claim")) {
				el.classList.add("govt-sidebar-claim");
			} else if (text.includes("tour") || text.includes("ta/da") || text.includes("ta & da") || href.includes("tour")) {
				el.classList.add("govt-sidebar-tour");
			} else if (text.includes("master") || text.includes("employee") || text.includes("setting") || href.includes("master")) {
				el.classList.add("govt-sidebar-master");
			}
		});
	}

	// 4. RENDER e-HRMS DASHBOARD CARDS
	function renderCardsMarkup(container, employeeInfo, cardsList, allEmployees) {
		let empTitle = employeeInfo ? `${employeeInfo.employee_name || employeeInfo.employee_id} (${employeeInfo.designation || 'Staff'})` : "Government Official";

		let optionsHtml = "";
		if (allEmployees && allEmployees.length > 0) {
			allEmployees.forEach(function (e) {
				const selected = (employeeInfo && (employeeInfo.employee_id === e.employee_id)) ? "selected" : "";
				optionsHtml += `<option value="${e.employee_id}" ${selected}>${e.employee_id} - ${e.employee_name} (${e.designation || 'Staff'})</option>`;
			});
		}

		let topBar = `
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
					<button class="btn btn-xs btn-primary" id="govt-ehrms-apply-btn" style="border-radius:6px;font-weight:600;padding:5px 12px;background:#2563eb;color:#fff;">➕ Apply Leave</button>
				</div>
			</div>
		`;

		let cardsHtml = '<div class="govt-ehrms-cards-container">';
		cardsList.forEach(function (c) {
			const color = c.color || "#0ea5e9";
			const iconSvg = svgIcons[c.icon_type] || svgIcons.calendar;

			cardsHtml += `
				<div class="govt-ehrms-card" data-leave="${c.leave_type || ''}" data-doctype="${c.doctype || ''}" style="border: 2px solid ${color};">
					<div class="govt-ehrms-card-circle" style="background-color: ${color};">
						${iconSvg}
					</div>
					<div class="govt-ehrms-card-title">${c.title}</div>
					<div class="govt-ehrms-card-number">${c.value}</div>
					<div class="govt-ehrms-card-caption">${c.sub_text}</div>
				</div>
			`;
		});
		cardsHtml += '</div>';

		container.innerHTML = topBar + cardsHtml;

		// Attach Click Events
		container.querySelectorAll(".govt-ehrms-card").forEach(function (cardEl) {
			cardEl.addEventListener("click", function () {
				const leaveType = this.getAttribute("data-leave");
				const docType = this.getAttribute("data-doctype");
				if (docType) {
					frappe.set_route("List", docType);
				} else if (leaveType) {
					frappe.new_doc("CCS Leave Application", {
						employee: currentDashboardEmployee || "",
						leave_type: leaveType
					});
				} else {
					frappe.set_route("List", "CCS Leave Application");
				}
			});
		});

		const sel = container.querySelector("#govt-ehrms-emp-select");
		if (sel) {
			sel.addEventListener("change", function () {
				fetchDashboardData(this.value);
			});
		}
		const refBtn = container.querySelector("#govt-ehrms-refresh-btn");
		if (refBtn) {
			refBtn.addEventListener("click", function () {
				fetchDashboardData(sel ? sel.value : null);
			});
		}
		const applyBtn = container.querySelector("#govt-ehrms-apply-btn");
		if (applyBtn) {
			applyBtn.addEventListener("click", function () {
				frappe.new_doc("CCS Leave Application", {
					employee: currentDashboardEmployee || ""
				});
			});
		}
	}

	function mountOrUpdateDashboard() {
		injectGovtStyles();

		const curRoute = frappe.get_route_str ? frappe.get_route_str() : "";
		// Do not show on List or Form routes
		if (curRoute.includes("List/") || curRoute.includes("Form/") || curRoute.includes("printview")) {
			const existing = document.getElementById("govt-ehrms-dashboard-section");
			if (existing) existing.remove();
			return;
		}

		// Locate target workspace main container
		const mainSection = document.querySelector(".layout-main-section, .workspace-page, .desk-page .page-content, .layout-main");
		if (!mainSection) return;

		let dashboardWrap = document.getElementById("govt-ehrms-dashboard-section");
		if (!dashboardWrap) {
			dashboardWrap = document.createElement("div");
			dashboardWrap.id = "govt-ehrms-dashboard-section";
			dashboardWrap.className = "govt-ehrms-dashboard-wrapper";

			// Insert right at the top of workspace
			mainSection.insertBefore(dashboardWrap, mainSection.firstChild);

			// Immediately render default statutory cards so there is ZERO blank delay
			renderCardsMarkup(dashboardWrap, null, defaultCardsData, []);
			// Then fetch live metrics
			fetchDashboardData();
		}
	}

	function fetchDashboardData(empId) {
		if (isFetching) return;
		isFetching = true;

		frappe.call({
			method: "govt_hr_payroll.govt_leave_management.leave_dashboard.get_employee_leave_dashboard",
			args: { employee: empId || currentDashboardEmployee },
			callback: function (r) {
				isFetching = false;
				const dashboardWrap = document.getElementById("govt-ehrms-dashboard-section");
				if (!dashboardWrap) return;

				if (r && r.message && r.message.leave_cards) {
					const data = r.message;
					currentDashboardEmployee = data.employee ? data.employee.employee_id : null;
					renderCardsMarkup(dashboardWrap, data.employee, data.leave_cards, data.all_employees);
				}
			},
			error: function () {
				isFetching = false;
			}
		});
	}

	// 5. INITIALIZE AND BIND ROUTE LISTENERS
	$(document).ready(function () {
		injectGovtStyles();
		setTimeout(enhanceGovtSidebar, 300);
		setTimeout(mountOrUpdateDashboard, 400);

		$(document).on("page-change", function () {
			injectGovtStyles();
			setTimeout(enhanceGovtSidebar, 300);
			setTimeout(mountOrUpdateDashboard, 400);
		});

		// Continuous observer to handle Desk dynamic DOM redraws
		setInterval(function () {
			const curRoute = frappe.get_route_str ? frappe.get_route_str() : "";
			if (!curRoute.includes("List/") && !curRoute.includes("Form/")) {
				enhanceGovtSidebar();
				if (!document.getElementById("govt-ehrms-dashboard-section")) {
					mountOrUpdateDashboard();
				}
			}
		}, 2000);
	});
})();
