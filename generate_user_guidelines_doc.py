# Copyright (c) 2026, NexGen ERP Technologies
# Script to generate the comprehensive Word Document (.docx) User Guidelines & SOP

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_user_guidelines():
    doc = docx.Document()

    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    NAVY = RGBColor(30, 58, 138)       # #1e3a8a
    SLATE = RGBColor(71, 85, 105)     # #475569
    DARK = RGBColor(15, 23, 42)       # #0f172a
    GREEN = RGBColor(22, 101, 52)     # #166534

    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def add_header(title, level=1):
        h = doc.add_heading(level=level)
        run = h.add_run(title)
        run.font.name = 'Calibri'
        run.font.bold = True
        if level == 1:
            run.font.size = Pt(17)
            run.font.color.rgb = NAVY
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after = Pt(6)
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = NAVY
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
        elif level == 3:
            run.font.size = Pt(11.5)
            run.font.color.rgb = SLATE
            h.paragraph_format.space_before = Pt(8)
            h.paragraph_format.space_after = Pt(2)
        return h

    def add_callout(text, prefix="OPERATIONAL GUIDELINE: "):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        set_cell_background(cell, "F1F5F9")
        p = cell.paragraphs[0]
        p.paragraph_format.left_indent = Inches(0.15)
        p.paragraph_format.right_indent = Inches(0.15)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        r1 = p.add_run(prefix)
        r1.font.bold = True
        r1.font.name = 'Calibri'
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY
        r2 = p.add_run(text)
        r2.font.name = 'Calibri'
        r2.font.size = Pt(10)
        r2.font.color.rgb = DARK
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ----------------- TITLE & COVER BLOCK -----------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(16)
    title_p.paragraph_format.space_after = Pt(4)
    title_run = title_p.add_run("Government HR & Payroll System")
    title_run.font.name = 'Calibri'
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = NAVY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    sub_run = sub_p.add_run("Standard Operating Procedure (SOP) & Complete User Guidelines")
    sub_run.font.name = 'Calibri'
    sub_run.font.size = Pt(14)
    sub_run.font.color.rgb = SLATE

    # Metadata Table
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Portal Web Address", "https://portal.nexgenerp.in"),
        ("Statutory Compliance", "7th Central Pay Commission, CCS Leave Rules 1972, GFR 2017, CGHS, CEA"),
        ("System Roles", "Govt Employee, Dealing Assistant, Section Officer, DDO, Govt HR Admin"),
        ("Document Version", "Release 1.0 (Frappe Framework v16 - Standalone Custom App)")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        c0 = meta_tbl.cell(row_idx, 0)
        c1 = meta_tbl.cell(row_idx, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "E2E8F0")
        set_cell_background(c1, "F8FAFC")
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.name = 'Calibri'
        r0.font.size = Pt(9.5)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(v)
        r1.font.name = 'Calibri'
        r1.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ----------------- CHAPTER 1 -----------------
    add_header("Chapter 1: Getting Started & System Access", 1)
    doc.add_paragraph(
        "Welcome to the official Government HR & Payroll System. This web application provides a secure, "
        "audit-compliant digital workflow for government departments, strictly aligned with Central Government "
        "pay rules and financial guidelines."
    )

    p = doc.add_paragraph()
    p.add_run("1.1 Accessing the Portal:\n").font.bold = True
    p.add_run("• Open any modern web browser and go to: ")
    r_url = p.add_run("https://portal.nexgenerp.in\n")
    r_url.font.bold = True; r_url.font.color.rgb = NAVY
    p.add_run("• Enter your registered Government Username / Email and Password.\n")
    p.add_run("• Click 'Login'. Upon successful login, you will land on the Desk.\n\n")

    p.add_run("1.2 Navigating the System:\n").font.bold = True
    p.add_run("• ")
    p.add_run("Direct Workspace URL: ").font.bold = True
    r_dir = p.add_run("https://portal.nexgenerp.in/desk/govt-masters\n")
    r_dir.font.bold = True; r_dir.font.color.rgb = NAVY
    p.add_run("• ")
    p.add_run("Left Sidebar: ").font.bold = True
    p.add_run("The sidebar lists all 6 modules (Payroll, Income Tax, Leave Management, Claims, Tour TA/DA, Masters) and all 15 statutory document types for single-click access.\n")
    p.add_run("• ")
    p.add_run("Quick Search: ").font.bold = True
    p.add_run("Press 'Ctrl + G' (or 'Cmd + G' on Mac) to open the Awesomebar and search for any employee, pay bill, leave application, or report instantly.\n")

    add_callout(
        "Never share your portal credentials. All actions (bill preparation, leave recommendations, and financial sanctions) "
        "are digitally logged with timestamps and user IDs for statutory CAG and internal audit trails.",
        "SECURITY NOTICE: "
    )

    # ----------------- CHAPTER 2 -----------------
    add_header("Chapter 2: User Roles & Responsibilities Matrix", 1)
    doc.add_paragraph(
        "To maintain statutory financial discipline under General Financial Rules (GFR), the system "
        "enforces a strict separation of powers across 5 official tiers:"
    )

    roles_data = [
        ("1. Govt Employee", "Self-Service", "Applies for leaves, submits Children Education Allowance (CEA) claims, files Tour Movement Orders, and submits TA/DA final reimbursement bills."),
        ("2. Dealing Assistant (DA)", "Maker (Operations)", "Prepares monthly pay bills using 'Fetch Active Employees', audits employee claim forms, scrutinizes leave balances, and enters retrospective pay arrear matrices."),
        ("3. Section Officer (SO)", "Checker (Supervisory)", "Audits bills prepared by the Dealing Assistant, checks statutory compliance (7th CPC limits, medical proofs, leave caps), and recommends documents for final sanction."),
        ("4. Drawing & Disbursing Officer (DDO)", "Financial Authority", "Final administrative and financial sanctioning authority. Approves pay bills, passes claims for payment, countersigns CGHS/CEA bills, and signs bank advices."),
        ("5. Govt HR Admin", "System Administrator", "Configures master settings, updates Central DA percentages, manages office units, maintains 7th CPC Pay Levels, and oversees user role assignments.")
    ]

    tbl_roles = doc.add_table(rows=len(roles_data)+1, cols=3)
    tbl_roles.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_roles.cell(0, 0).width = Inches(1.8)
    tbl_roles.cell(0, 1).width = Inches(1.5)
    tbl_roles.cell(0, 2).width = Inches(3.2)
    set_cell_background(tbl_roles.cell(0, 0), "1E3A8A")
    set_cell_background(tbl_roles.cell(0, 1), "1E3A8A")
    set_cell_background(tbl_roles.cell(0, 2), "1E3A8A")
    for ci, htxt in enumerate(["Official Role", "Authority Level", "Key Responsibilities"]):
        r = tbl_roles.cell(0, ci).paragraphs[0].add_run(htxt)
        r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)

    for idx, (rname, rlvl, rdesc) in enumerate(roles_data, 1):
        c0 = tbl_roles.cell(idx, 0); c1 = tbl_roles.cell(idx, 1); c2 = tbl_roles.cell(idx, 2)
        c0.width = Inches(1.8); c1.width = Inches(1.5); c2.width = Inches(3.2)
        bg = "F8FAFC" if idx%2==1 else "FFFFFF"
        set_cell_background(c0, bg); set_cell_background(c1, bg); set_cell_background(c2, bg)
        p0 = c0.paragraphs[0]; r0 = p0.add_run(rname); r0.font.bold = True; r0.font.size = Pt(9.5)
        p1 = c1.paragraphs[0]; r1 = p1.add_run(rlvl); r1.font.size = Pt(9.5)
        p2 = c2.paragraphs[0]; r2 = p2.add_run(rdesc); r2.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ----------------- CHAPTER 3 -----------------
    add_header("Chapter 3: Day-to-Day Module Guidelines", 1)

    # Section 3.1
    add_header("3.1 Monthly Pay Bill Processing & 5 Statutory Schedules", 2)
    doc.add_paragraph(
        "Follow these steps every month to disburse salaries in compliance with central treasury rules:"
    )
    p = doc.add_paragraph()
    p.add_run("Step 1: Open New Pay Bill\n").font.bold = True
    p.add_run("• Click 'Pay Bill (Monthly Payroll)' in the sidebar.\n")
    p.add_run("• Click '+ Add Govt Pay Bill'. Select your Office Unit, Month, and Year.\n\n")

    p.add_run("Step 2: Automated Employee Fetching\n").font.bold = True
    p.add_run("• Click the prominent blue button: 'Fetch Active Employees'.\n")
    p.add_run("• All active employees posted in that unit are automatically loaded with their complete 7th CPC earnings and deductions.\n\n")

    p.add_run("Step 3: Verify Automated Calculations\n").font.bold = True
    p.add_run("• Basic Pay (BP): Net after subtracting '*(-) Pension' deduction for re-employed ex-servicemen.\n")
    p.add_run("• Dearness Allowance (DA): Auto-calculated at 53% of Basic Pay.\n")
    p.add_run("• House Rent Allowance (HRA): 30% (Class X), 20% (Class Y), or 10% (Class Z). If government quarters are allotted, HRA is strictly set to ₹0.\n")
    p.add_run("• Transport Allowance (TPT): Includes statutory DA on TPT at the current DA percentage.\n")
    p.add_run("• NPS Tier-1: 10% Employee Contribution + 14% Government Contribution on (BP + DA).\n")
    p.add_run("• Deductions: GPF Monthly Subscription, CGHS, CGEGIS, Licence Fee, and Income Tax TDS + 4% Education Cess.\n")
    p.add_run("• Net Pay: Gross Pay minus Total Deductions.\n\n")

    p.add_run("Step 4: Printing the 5 Mandatory Treasury Schedules\n").font.bold = True
    p.add_run("Click the Printer icon in the top right corner. In the Print Format menu, select:\n")
    p.add_run("1. Monthly Pay & Allowances (Treasury Roster with DDO passing order)\n")
    p.add_run("2. NPS Annexure-II (PRAN employee & government contribution schedule)\n")
    p.add_run("3. GP Fund Recovery Schedule (GPF subscription & loan refunds)\n")
    p.add_run("4. Licence Fee Recovery Schedule (Quarter allotment & fee recovery)\n")
    p.add_run("5. Bank Payment Advice (Direct NEFT/RTGS crediting format)\n")

    # Section 3.2
    add_header("3.2 Annual Income Tax Assessment (FY 2026-27)", 2)
    p = doc.add_paragraph()
    p.add_run("• Open Sidebar -> Income Tax Statement -> click '+ Add Govt Income Tax Statement'.\n")
    p.add_run("• Select the Employee and set Financial Year to '2026-2027'.\n")
    p.add_run("• Choose Tax Regime: New Regime (Section 115BAC) or Old Regime.\n")
    p.add_run("• The system applies the ₹75,000 Standard Deduction under the New Regime (₹50,000 under Old Regime).\n")
    p.add_run("• Section 87A Tax Rebate gives Nil tax if taxable income is up to ₹7,00,000.\n")
    p.add_run("• Slabs apply: ₹3L-₹7L (5%), ₹7L-₹10L (10%), ₹10L-₹12L (15%), ₹12L-₹15L (20%), Above ₹15L (30%) + 4% Cess.\n")
    p.add_run("• Print the '12-Month Tax Statement' for Form 16 issuance and audit records.\n")

    # Section 3.3
    add_header("3.3 Due-Drawn Arrears Management", 2)
    p = doc.add_paragraph()
    p.add_run("When DA rates are revised retrospectively or employees receive delayed promotion / MACP:\n")
    p.add_run("• Open Sidebar -> Due-Drawn Arrears -> click '+ Add Due Drawn Arrear'.\n")
    p.add_run("• Enter the Employee ID and Period From / To.\n")
    p.add_run("• In the item table, enter each month's Due Pay & Allowances vs Drawn Pay & Allowances.\n")
    p.add_run("• Net Arrear Payable is auto-calculated: (Due Gross - Drawn Gross) - (Due NPS - Drawn NPS).\n")
    p.add_run("• Print the official 'Due Drawn Statement' for DDO sanction and PAO passing.\n")

    # Section 3.4
    add_header("3.4 CCS Leave Rules 1972 & DO Part II Orders", 2)
    p = doc.add_paragraph()
    p.add_run("• Applying for Leave: Open Sidebar -> Leave Application. Select employee, leave type, and dates.\n")
    p.add_run("• 180-Day Rule: Continuous Earned Leave (EL) cannot exceed 180 days under CCS Rule 26.\n")
    p.add_run("• Commuted Leave: Automatically debits exactly double (2x) from the employee's Half Pay Leave (HPL) balance and requires a registered medical practitioner certificate.\n")
    p.add_run("• 300-Day Buffer Rule: 15 days advance EL credited on 01 Jan / 01 Jul. If balance is already 286-300 days, excess days are held in buffer credit to offset leaves taken during that half-year.\n")
    p.add_run("• DO Part II Order: Open Sidebar -> DO Part II Order to publish official gazetted sanction notices.\n")

    # Section 3.5
    add_header("3.5 Children Education Allowance (CEA) & CGHS Claims", 2)
    p = doc.add_paragraph()
    p.add_run("• CEA Claim: Sidebar -> CEA Claim. Admissible up to ₹33,750 per child per academic year, and Hostel Subsidy up to ₹1,01,250 per child. Strictly capped at 2 surviving children.\n")
    p.add_run("• Medical Reimbursement (Form MRC-S): Sidebar -> Medical Claim (Form MRC-S). Itemizes OPD consultations, indoor hospital treatments, lab tests, and medicines for serving central government employees.\n")
    p.add_run("• Both claims feature formal printable forms with statutory declaration and DDO countersignatures.\n")

    # Section 3.6
    add_header("3.6 Tour TA/DA & Official Travel Claims", 2)
    p = doc.add_paragraph()
    p.add_run("• Tour Movement Order: Prior administrative approval for official journeys.\n")
    p.add_run("• TA/DA Final Claim: Files travel allowance bills after completion of tour.\n")
    p.add_run("• 7th CPC Ceilings: Level 14+ (Hotel up to ₹9,375, Food ₹1,500), Level 12-13 (Hotel ₹5,625, Food ₹1,200), Level 9-11 (Hotel ₹2,813, Food ₹1,050), Level 6-8 (Hotel ₹938, Food ₹900), Level 5 and below (Hotel ₹563, Food ₹600).\n")
    p.add_run("• Food Duration Slabs: Less than 6 hours = 30%, 6 to 12 hours = 70%, Exceeding 12 hours = 100%.\n")

    # ----------------- CHAPTER 4 -----------------
    add_header("Chapter 4: Approval Workflows & Action Guide", 1)
    doc.add_paragraph(
        "Every official bill and claim follows an automated multi-tier approval workflow:"
    )

    wf_guide = [
        ("Govt Pay Bill", "1. Dealing Assistant drafts bill and clicks 'Submit for Verification'.\n2. Section Officer audits figures and clicks 'Verify & Recommend' (or 'Return with Queries').\n3. DDO reviews and clicks 'Sanction & Finalize' to approve payment and pass bill."),
        ("CCS Leave Application", "1. Employee submits leave application ('Forward for Scrutiny').\n2. Dealing Assistant checks leave admissibility and clicks 'Recommend Leave'.\n3. DDO clicks 'Sanction Leave' (or 'Reject Leave')."),
        ("CEA & Medical Claims", "1. Employee submits claim ('Submit Claim').\n2. Office checks fee receipts / medical bills and clicks 'Verify Claim'.\n3. Section Officer clicks 'Recommend by SO'.\n4. DDO clicks 'Sanction for Payment'."),
        ("Tour TA/DA Bill", "1. Employee submits final bill after movement ('Submit Tour Bill').\n2. Dealing Assistant verifies ticket/hotel vouchers ('Audit Tour Claims').\n3. DDO sanctions bill for treasury payment ('Sanction Travel Bill').")
    ]

    tbl_wfg = doc.add_table(rows=len(wf_guide)+1, cols=2)
    tbl_wfg.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_wfg.cell(0, 0).width = Inches(2.2)
    tbl_wfg.cell(0, 1).width = Inches(4.3)
    set_cell_background(tbl_wfg.cell(0, 0), "1E3A8A")
    set_cell_background(tbl_wfg.cell(0, 1), "1E3A8A")
    r = tbl_wfg.cell(0, 0).paragraphs[0].add_run("Transaction Type")
    r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
    r2 = tbl_wfg.cell(0, 1).paragraphs[0].add_run("Step-by-Step Officer Action Guide")
    r2.font.bold = True; r2.font.color.rgb = RGBColor(255, 255, 255)

    for idx, (tname, tguide) in enumerate(wf_guide, 1):
        c0 = tbl_wfg.cell(idx, 0); c1 = tbl_wfg.cell(idx, 1)
        c0.width = Inches(2.2); c1.width = Inches(4.3)
        bg = "F8FAFC" if idx%2==1 else "FFFFFF"
        set_cell_background(c0, bg); set_cell_background(c1, bg)
        p0 = c0.paragraphs[0]; r0 = p0.add_run(tname); r0.font.bold = True; r0.font.size = Pt(9.5)
        p1 = c1.paragraphs[0]; r1 = p1.add_run(tguide); r1.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ----------------- CHAPTER 5 -----------------
    add_header("Chapter 5: Frequently Asked Questions (FAQ) & Troubleshooting", 1)

    faqs = [
        ("Q1: Why did a user receive 'No permission for Page' error?", 
         "A: In Frappe Desk, users who access workspaces must have the 'Workspace Manager' role assigned, in addition to their 'Govt HR Admin' or departmental roles. Ensure 'Workspace Manager' is checked in User Roles."),
        ("Q2: How do I refresh the sidebar if some DocTypes are not visible?",
         "A: Click the dropdown in the top-left corner ('Masters & Settings v') -> click 'Edit Sidebar' -> click 'Reset to Standard' -> click 'Yes' -> click 'Save'. Then hard refresh your browser tab ('Ctrl + Shift + R')."),
        ("Q3: Why is HRA showing as ₹0 for an employee?",
         "A: Under Central Government rules, an employee allotted official government quarters is not entitled to HRA. Check if 'Government Quarters Availed' is ticked on the employee master."),
        ("Q4: Can we add more than 2 children in a CEA claim?",
         "A: Under Department of Personnel & Training (DoPT) guidelines, CEA is admissible for up to 2 surviving children only. The system automatically restricts claims to a maximum of 2 children in accordance with central rules."),
        ("Q5: Where can I download this guide and system updates?",
         "A: This official Word Document is stored in your 'Govt HR Payroll' folder and is maintained in the central GitHub repository: https://github.com/nexgenerptechnologies/govt-hr-and-payroll.git.")
    ]

    for q, a in faqs:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q)
        r_q.font.bold = True; r_q.font.name = 'Calibri'; r_q.font.size = Pt(10.5); r_q.font.color.rgb = NAVY

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_after = Pt(6)
        r_a = p_a.add_run(a)
        r_a.font.name = 'Calibri'; r_a.font.size = Pt(10); r_a.font.color.rgb = DARK

    # Save to both target naming conventions in D:\Govt HR Payroll
    p1 = os.path.abspath(r'D:\Govt HR Payroll\User_Guidelines_Govt_HR_Payroll.docx')
    p2 = os.path.abspath(r'D:\Govt HR Payroll\Govt_HR_Payroll_User_Guidelines.docx')
    doc.save(p1)
    doc.save(p2)
    print(f"Successfully generated User Guidelines at:\n1. {p1}\n2. {p2}")

if __name__ == '__main__':
    create_user_guidelines()
