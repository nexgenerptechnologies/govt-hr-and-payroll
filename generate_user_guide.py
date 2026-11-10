# Copyright (c) 2026, NexGen ERP Technologies
# Script to generate the comprehensive Word Document (.docx) User Verification Guide

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_user_guide():
    doc = docx.Document()

    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    NAVY = RGBColor(30, 58, 138)
    SLATE = RGBColor(71, 85, 105)
    DARK = RGBColor(15, 23, 42)

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

    def add_callout(text, prefix="IMPORTANT NOTE: "):
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

    # ----------------- COVER & TITLE -----------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(16)
    title_p.paragraph_format.space_after = Pt(4)
    title_run = title_p.add_run("Government HR & Payroll System (7th CPC)")
    title_run.font.name = 'Calibri'
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = NAVY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    sub_run = sub_p.add_run("Comprehensive End-User Verification & Module Walkthrough Guide")
    sub_run.font.name = 'Calibri'
    sub_run.font.size = Pt(13)
    sub_run.font.color.rgb = SLATE

    # Metadata Table
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Web Portal URL", "https://portal.nexgenerp.in"),
        ("System Architecture", "Frappe Framework v16 (Single Standalone App - No ERPNext Dependency)"),
        ("Statutory Standards", "7th Central Pay Commission (CPC), GFR 2017, CCS Leave Rules 1972, CGHS, CEA"),
        ("Target Audience", "DDOs, Section Officers, Dealing Assistants, HR Managers, Auditors & End Users")
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

    # ----------------- SECTION 1 -----------------
    add_header("1. System Access & How to Log In", 1)
    doc.add_paragraph(
        "This guide walks you step-by-step through every module in the Government HR & Payroll system. "
        "Each module strictly implements the statutory provisions of Folders 1 through 6, fully configured "
        "according to 7th Central Pay Commission (CPC) rules and central government accounting standards."
    )

    p2 = doc.add_paragraph()
    p2.add_run("How to Log In:\n").font.bold = True
    p2.add_run("1. Open your web browser (Google Chrome, Microsoft Edge, or Firefox) and visit: ")
    r_url = p2.add_run("https://portal.nexgenerp.in\n")
    r_url.font.bold = True
    r_url.font.color.rgb = NAVY
    p2.add_run("2. Enter your Email / Username and Password, then click 'Login'.\n")
    p2.add_run("3. You will arrive at the Desk. Click on the 'Government HR & Payroll' app card, or navigate directly to:\n   ")
    r_desk = p2.add_run("https://portal.nexgenerp.in/desk/govt-masters\n")
    r_desk.font.bold = True
    r_desk.font.color.rgb = NAVY

    add_callout(
        "The left-hand sidebar contains direct one-click links to all 6 Modules and all 15 Statutory DocTypes. "
        "You can jump directly to any document at any time without leaving your page.",
        "SIDEBAR NAVIGATION: "
    )

    # ----------------- SECTION 2 -----------------
    add_header("2. Module 1: Masters & 7th CPC Setup", 1)
    doc.add_paragraph(
        "Before processing monthly payroll or claims, verify the core statutory masters that control all "
        "financial calculations across the organization:"
    )

    add_header("A. 7th CPC Pay Matrix (Levels 1 to 18)", 2)
    p = doc.add_paragraph()
    p.add_run("Where to find it: ").font.bold = True
    p.add_run("Sidebar -> CPC Pay Level (1-18)\n")
    p.add_run("What to see: ").font.bold = True
    p.add_run(
        "All 19 standard 7th CPC Pay Levels are pre-configured (Level-1 to Level-18, including Level-13A). "
        "Open any level (e.g. Level-10 or Level-13). You will see the entire vertical cell progression table "
        "auto-calculated with the statutory 3% annual increment rounded to the nearest ₹100."
    )

    add_header("B. Office Unit (DDO / PAO / CDA Master)", 2)
    p = doc.add_paragraph()
    p.add_run("Where to find it: ").font.bold = True
    p.add_run("Sidebar -> Office Unit (DDO/PAO)\n")
    p.add_run("What to see: ").font.bold = True
    p.add_run(
        "Official administrative unit records containing: Ministry/Department Name, DDO ID, DDO Code, "
        "PAO Code, CDA Code, Station, and City Classification (Class X, Y, or Z). "
        "The City Classification automatically governs the HRA rate applied to all employees posted in that unit."
    )

    add_header("C. Employee Master (Comprehensive Service Record)", 2)
    p = doc.add_paragraph()
    p.add_run("Where to find it: ").font.bold = True
    p.add_run("Sidebar -> Employee Master\n")
    p.add_run("Key statutory fields to inspect:\n")
    p.add_run("• Basic Details: First/Last Name, Office/Unit, Designation, DOB, Date of Joining (DOJ).\n")
    p.add_run("• Auto-calculated Date of Retirement (DOR): Automatically computes the last working day of the month on reaching 60 years of age (or last day of previous month if born on the 1st).\n")
    p.add_run("• Date of Next Increment (DNI): Preset to 01-Jan or 01-Jul according to 7th CPC qualifying rules.\n")
    p.add_run("• Quarters Allotment: If ticked, stores Quarter Type, Floor, Quarter No., AAN No., and Monthly Licence Fee. When quarters are allotted, HRA is automatically suppressed to ₹0.\n")
    p.add_run("• Re-employed Pension Deduction: Records '*(-) Pension' deduction for re-employed ex-servicemen.\n")
    p.add_run("• Pension Scheme: NPS (PRAN No.) vs. Old Pension Scheme GPF (GPF No. and monthly subscription).\n")
    p.add_run("• Bank Details: Bank Name, Branch, Account No, IFSC Code, and MICR Code for direct payment advice.\n")

    add_header("D. Payroll Settings (Central Statutory Control)", 2)
    p = doc.add_paragraph()
    p.add_run("Where to find it: ").font.bold = True
    p.add_run("Sidebar -> Payroll Settings\n")
    p.add_run("What to see: ").font.bold = True
    p.add_run(
        "Centrally updates government rates: Current DA Rate (50% / 53%), NPS Employee (10%), "
        "NPS Government Contribution (14%), HRA Class X (30%), Class Y (20%), Class Z (10%), and Health & Education Cess (4%). "
        "Updating here automatically updates all new monthly bills."
    )

    # ----------------- SECTION 3: FOLDER 1 -----------------
    add_header("3. Module 2: Monthly Pay Bill & 5 Statutory Schedules (Folder 1)", 1)
    doc.add_paragraph(
        "This is the primary operational module for processing monthly salary disbursements "
        "under Central Civil Services (CCS) rules and treasury standards."
    )

    add_header("How to Test Generating a Monthly Pay Bill:", 2)
    p = doc.add_paragraph()
    p.add_run("1. Open ").font.name = 'Calibri'
    p.add_run("Sidebar -> Pay Bill (Monthly Payroll)").font.bold = True
    p.add_run(" and click ").font.name = 'Calibri'
    p.add_run("'+ Add Govt Pay Bill'").font.bold = True
    p.add_run(".\n")
    p.add_run("2. Select your ").font.name = 'Calibri'
    p.add_run("Office / Unit").font.bold = True
    p.add_run(", select ").font.name = 'Calibri'
    p.add_run("Month").font.bold = True
    p.add_run(" (e.g. October), and ").font.name = 'Calibri'
    p.add_run("Year").font.bold = True
    p.add_run(" (e.g. 2026).\n")
    p.add_run("3. Click the prominent blue button at the top: ").font.name = 'Calibri'
    r_fetch = p.add_run("'Fetch Active Employees'")
    r_fetch.font.bold = True
    r_fetch.font.color.rgb = NAVY
    p.add_run(".\n")
    p.add_run("4. All active employees belonging to this Office Unit are instantly populated into the Pay Bill Item table with their complete statutory allowances and deductions automatically calculated:\n")
    p.add_run("   • Effective Basic Pay = Basic Pay minus Re-employed Pension deduction\n")
    p.add_run("   • Dearness Allowance (DA) = Basic Pay * DA Rate (53%)\n")
    p.add_run("   • House Rent Allowance (HRA) = 30% / 20% / 10% based on Unit City Class (Zero if quarters allotted)\n")
    p.add_run("   • Transport Allowance (TPT) + DA on TPT\n")
    p.add_run("   • NPS Employee Contribution (10% of BP + DA) + NPS Govt Contribution (14% of BP + DA)\n")
    p.add_run("   • GPF Subscription, CGHS, CGEGIS, Licence Fee, and Monthly Income Tax TDS + 4% Edu Cess\n")
    p.add_run("   • Net Pay = Gross Pay minus Total Deductions\n")
    p.add_run("5. Click ").font.name = 'Calibri'
    p.add_run("'Save'").font.bold = True
    p.add_run(". The bill header summaries are automatically updated with total P&A, total recoveries, and total disbursement.\n")

    add_header("How to View and Print the 5 Statutory Schedules:", 2)
    doc.add_paragraph(
        "Central government treasury rules mandate 5 separate statutory schedules for every monthly bill. "
        "To view and print each schedule:\n"
        "1. Inside the saved Pay Bill, click the Printer icon at the top right.\n"
        "2. In the Print Format dropdown, switch between all 5 official formats:"
    )

    schedules = [
        ("1. Monthly Pay & Allowances", "Complete roster listing PC No., Employee Name, Designation, PAN, Basic Pay, DA, HRA, TPT, Gross, NPS, GPF, CGHS, LF, CGEGIS, Tax, Net Pay, and signature blocks."),
        ("2. NPS Annexure-II", "Official PRAN schedule showing PRAN No., Employee Contribution (10%), Govt Contribution (14%), and Grand Total for PAO remittance."),
        ("3. GP Fund Recovery Schedule", "Statutory GPF schedule showing GPF Account No., Monthly Subscription, Refund of Advances, and Total Deposit for AG audit."),
        ("4. Licence Fee Recovery Schedule", "Estate Directorate schedule listing Quarters No., Type, Floor, AAN No., and Licence Fee recovered for government accommodation."),
        ("5. Bank Payment Advice", "Official bank statement listing Employee Name, Bank Branch, Bank Account No., IFSC Code, and Net Amount for NEFT/RTGS crediting.")
    ]

    tbl_sch = doc.add_table(rows=len(schedules)+1, cols=2)
    tbl_sch.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sch.cell(0, 0).width = Inches(2.3)
    tbl_sch.cell(0, 1).width = Inches(4.2)
    set_cell_background(tbl_sch.cell(0, 0), "1E3A8A")
    set_cell_background(tbl_sch.cell(0, 1), "1E3A8A")
    r = tbl_sch.cell(0, 0).paragraphs[0].add_run("Statutory Schedule")
    r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
    r2 = tbl_sch.cell(0, 1).paragraphs[0].add_run("Purpose & Contents")
    r2.font.bold = True; r2.font.color.rgb = RGBColor(255, 255, 255)

    for idx, (s_name, s_desc) in enumerate(schedules, 1):
        c0 = tbl_sch.cell(idx, 0); c1 = tbl_sch.cell(idx, 1)
        c0.width = Inches(2.3); c1.width = Inches(4.2)
        set_cell_background(c0, "F8FAFC" if idx%2==1 else "FFFFFF")
        set_cell_background(c1, "F8FAFC" if idx%2==1 else "FFFFFF")
        p0 = c0.paragraphs[0]; r0 = p0.add_run(s_name); r0.font.bold = True; r0.font.size = Pt(9.5)
        p1 = c1.paragraphs[0]; r1 = p1.add_run(s_desc); r1.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ----------------- SECTION 4: INCOME TAX -----------------
    add_header("4. Module 3: 12-Month Income Tax Statement (Folder 2)", 1)
    doc.add_paragraph(
        "Central government income tax calculation for FY 2026-27 under the New Tax Regime (Section 115BAC) "
        "and Old Tax Regime."
    )

    p = doc.add_paragraph()
    p.add_run("Where to find it: ").font.bold = True
    p.add_run("Sidebar -> Income Tax Statement\n")
    p.add_run("How to test:\n").font.bold = True
    p.add_run("1. Click ").font.name = 'Calibri'
    p.add_run("'+ Add Govt Income Tax Statement'").font.bold = True
    p.add_run(", select an ").font.name = 'Calibri'
    p.add_run("Employee").font.bold = True
    p.add_run(", and set ").font.name = 'Calibri'
    p.add_run("Financial Year").font.bold = True
    p.add_run(" to '2026-2027'.\n")
    p.add_run("2. The 12-Month March to February salary ledger is automatically available for monthly earnings and deductions.\n")
    p.add_run("3. Choose ").font.name = 'Calibri'
    p.add_run("Tax Regime: New Regime (Sec 115BAC)").font.bold = True
    p.add_run(".\n")
    p.add_run("4. Notice how statutory rules apply automatically:\n")
    p.add_run("   • Standard Deduction: ₹75,000 for New Regime (₹50,000 for Old Regime)\n")
    p.add_run("   • Section 87A Tax Rebate: Nil tax if total taxable income is up to ₹7,00,000\n")
    p.add_run("   • 7th CPC Slabs: Up to ₹3L Nil, 3-7L 5%, 7-10L 10%, 10-12L 15%, 12-15L 20%, Above 15L 30%\n")
    p.add_run("   • Health & Education Cess: Exactly 4% on base tax\n")
    p.add_run("   • Monthly Recommended TDS: Total Annual Tax / Remaining Months\n")
    p.add_run("5. Click ").font.name = 'Calibri'
    p.add_run("Print").font.bold = True
    p.add_run(" to view the formal ").font.name = 'Calibri'
    p.add_run("'12-Month Tax Statement'").font.bold = True
    p.add_run(" print format with employer TDS certificate signature blocks.\n")

    # ----------------- SECTION 5: ARREARS -----------------
    add_header("5. Module 4: Due-Drawn Arrears Engine (Folder 3)", 1)
    doc.add_paragraph(
        "Automates retroactive pay revisions (DA hikes, MACP, promotions) without manual spreadsheet errors."
    )

    p = doc.add_paragraph()
    p.add_run("Where to find it: ").font.bold = True
    p.add_run("Sidebar -> Due-Drawn Arrears\n")
    p.add_run("How to test:\n").font.bold = True
    p.add_run("1. Click ").font.name = 'Calibri'
    p.add_run("'+ Add Due Drawn Arrear'").font.bold = True
    p.add_run(", enter Employee ID, Arrear Period From (e.g. 01-Jan-2026), and To (e.g. 30-Jun-2026).\n")
    p.add_run("2. In the table, enter each month's Due Basic Pay/DA vs. Drawn Basic Pay/DA.\n")
    p.add_run("3. The system computes the comparative matrix row by row:\n")
    p.add_run("   • Difference in Pay & Allowances (Due Gross - Drawn Gross)\n")
    p.add_run("   • Difference in NPS Recovery (Due NPS - Drawn NPS)\n")
    p.add_run("   • Statutory Net Arrear Payable = Diff P&A minus Diff NPS\n")
    p.add_run("4. Click ").font.name = 'Calibri'
    p.add_run("Print").font.bold = True
    p.add_run(" to generate the official ").font.name = 'Calibri'
    p.add_run("'Due Drawn Statement'").font.bold = True
    p.add_run(" comparative schedule for DDO sanction and PAO passing.\n")

    # ----------------- SECTION 6: LEAVE RULES -----------------
    add_header("6. Module 5: CCS Leave Rules 1972 & DO Part II Orders (Folder 4)", 1)
    doc.add_paragraph(
        "Enforces the statutory leave rules of the Central Civil Services (Leave) Rules, 1972."
    )

    p = doc.add_paragraph()
    p.add_run("Where to find it: ").font.bold = True
    p.add_run("Sidebar -> Leave Application, DO Part II Order, Leave Ledger\n")
    p.add_run("Statutory Rules to verify:\n").font.bold = True
    p.add_run("1. ").font.name = 'Calibri'
    p.add_run("180-Day Continuous EL Cap: ").font.bold = True
    p.add_run("Under CCS Rule 26, Earned Leave applied continuously cannot exceed 180 days. Try applying for 185 days; the system automatically validates and prevents submission.\n")
    p.add_run("2. ").font.name = 'Calibri'
    p.add_run("Commuted Leave (2x Debit Rule): ").font.bold = True
    p.add_run("Apply for 5 days of Commuted Leave. The system verifies medical certificate attachment and automatically debits exactly 10 days (2x) from the employee's Half Pay Leave (HPL) ledger.\n")
    p.add_run("3. ").font.name = 'Calibri'
    p.add_run("300-Day Accumulation + 15-Day Buffer Rule: ").font.bold = True
    p.add_run("Central government employees have a 300-day ceiling. When 15 days advance credit is granted on 01 Jan / 01 Jul to an employee already having 290 or 300 days, the excess is stored in 'buffer_credit_days' to be set off against leaves availed during that half-year.\n")
    p.add_run("4. ").font.name = 'Calibri'
    p.add_run("DO Part Two Order: ").font.bold = True
    p.add_run("Open Sidebar -> DO Part II Order. Generate formal daily orders notifying leave grants, promotions, increments, and transfers with Gazette notification numbering.\n")
    p.add_run("5. ").font.name = 'Calibri'
    p.add_run("Official Print Formats: ").font.bold = True
    p.add_run("Print both the 'Leave Application Form' and 'DO Part II Official Sanction Order' directly from their print views.\n")

    # ----------------- SECTION 7: CLAIMS -----------------
    add_header("7. Module 6: Claims & Medical Reimbursements (Folder 5)", 1)
    doc.add_paragraph(
        "Automates statutory reimbursement claims under Children Education Allowance (CEA) "
        "and Central Government Health Scheme (CGHS)."
    )

    p = doc.add_paragraph()
    p.add_run("A. Children Education Allowance (CEA Claim)\n").font.bold = True
    p.add_run("• Where to find it: Sidebar -> CEA Claim\n")
    p.add_run("• Statutory Caps: CEA is admissible at ₹33,750 per child per academic year, and Hostel Subsidy at ₹1,01,250 per child per year.\n")
    p.add_run("• 2-Child Restriction: Maximum 2 surviving children (unless second childbirth resulted in twins/triplets).\n")
    p.add_run("• Print View: Click Print to view the official 'CEA Official Claim Form' with DDO countersignature.\n\n")

    p.add_run("B. CGHS Medical Claim (Form MRC-S for Serving Employees)\n").font.bold = True
    p.add_run("• Where to find it: Sidebar -> Medical Claim (Form MRC-S)\n")
    p.add_run("• Breakdown: Enter breakdown of OPD consultation, indoor hospital treatment, laboratory investigations, and pharmacy bills.\n")
    p.add_run("• Print View: Generates official Central Government Medical Reimbursement Form MRC(S) ready for submission to the Controlling Officer / CMO.\n")

    # ----------------- SECTION 8: TOUR TA/DA -----------------
    add_header("8. Module 7: Tour TA/DA & 7th CPC Entitlements (Folder 6)", 1)
    doc.add_paragraph(
        "Automates official government tour sanctions and travelling allowance claims under 7th CPC rules."
    )

    p = doc.add_paragraph()
    p.add_run("Where to find it: ").font.bold = True
    p.add_run("Sidebar -> Tour Movement Order, TA/DA Final Claim\n")
    p.add_run("How to test:\n").font.bold = True
    p.add_run("1. ").font.name = 'Calibri'
    p.add_run("Tour Movement Order: ").font.bold = True
    p.add_run("Create an official tour movement sanction with Tour Order No., Departure Station, Destination, and Official Purpose.\n")
    p.add_run("2. ").font.name = 'Calibri'
    p.add_run("TADA Final Claim: ").font.bold = True
    p.add_run("Select the employee. Enter the journey details, hotel accommodation bills, and food bills.\n")
    p.add_run("3. ").font.name = 'Calibri'
    p.add_run("Statutory 7th CPC Ceilings: ").font.bold = True
    p.add_run("The system automatically validates hotel and food caps against the employee's pay matrix level:\n")
    p.add_run("   • Pay Level 14 and above: Hotel up to ₹9,375/day, Food ₹1,500/day\n")
    p.add_run("   • Pay Level 12 & 13: Hotel up to ₹5,625/day, Food ₹1,200/day\n")
    p.add_run("   • Pay Level 9 to 11: Hotel up to ₹2,813/day, Food ₹1,050/day\n")
    p.add_run("   • Pay Level 6 to 8: Hotel up to ₹938/day, Food ₹900/day\n")
    p.add_run("   • Pay Level 5 and below: Hotel up to ₹563/day, Food ₹600/day\n")
    p.add_run("4. ").font.name = 'Calibri'
    p.add_run("Food Allowance Duration Slabs: ").font.bold = True
    p.add_run("Less than 6 hours = 30%, 6 to 12 hours = 70%, Exceeding 12 hours = 100%.\n")
    p.add_run("5. ").font.name = 'Calibri'
    p.add_run("Print Format: ").font.bold = True
    p.add_run("Click Print to view the official 'TADA Final Claim Bill' with journey itinerary and certificate by the government servant.\n")

    # ----------------- SECTION 9: APPROVAL WORKFLOW -----------------
    add_header("9. Multi-Tier Approval Matrices (Maker-Checker-DDO)", 1)
    doc.add_paragraph(
        "Central government financial discipline requires strict separation of powers between makers, checkers, "
        "and sanctioning authorities:"
    )

    wf_rows = [
        ("Govt Pay Bill", "Dealing Assistant (Draft) -> Section Officer (Under Verification) -> DDO (Sanctioned & Passed)"),
        ("CCS Leave Application", "Govt Employee (Applied) -> Dealing Assistant (Scrutinized) -> Section Officer (Recommended) -> DDO (Sanctioned)"),
        ("CEA Claim", "Govt Employee (Claim Drafted) -> Dealing Assistant (Scrutinized) -> Section Officer (Recommended) -> DDO (Sanctioned for Payment)"),
        ("Tour TADA Claim", "Govt Employee (Claim Drafted) -> Dealing Assistant (Scrutinized) -> Section Officer (Recommended) -> DDO (Sanctioned for Payment)")
    ]

    tbl_wf = doc.add_table(rows=len(wf_rows)+1, cols=2)
    tbl_wf.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_wf.cell(0, 0).width = Inches(2.3)
    tbl_wf.cell(0, 1).width = Inches(4.2)
    set_cell_background(tbl_wf.cell(0, 0), "1E3A8A")
    set_cell_background(tbl_wf.cell(0, 1), "1E3A8A")
    r = tbl_wf.cell(0, 0).paragraphs[0].add_run("Document Type")
    r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)
    r2 = tbl_wf.cell(0, 1).paragraphs[0].add_run("Statutory Workflow States & Authorities")
    r2.font.bold = True; r2.font.color.rgb = RGBColor(255, 255, 255)

    for idx, (wf_doc_name, wf_flow) in enumerate(wf_rows, 1):
        c0 = tbl_wf.cell(idx, 0); c1 = tbl_wf.cell(idx, 1)
        c0.width = Inches(2.3); c1.width = Inches(4.2)
        set_cell_background(c0, "F8FAFC" if idx%2==1 else "FFFFFF")
        set_cell_background(c1, "F8FAFC" if idx%2==1 else "FFFFFF")
        p0 = c0.paragraphs[0]; r0 = p0.add_run(wf_doc_name); r0.font.bold = True; r0.font.size = Pt(9.5)
        p1 = c1.paragraphs[0]; r1 = p1.add_run(wf_flow); r1.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    add_callout(
        "At each stage, the supervisory officer has the power to either recommend/sanction the document or "
        "'Return with Queries' back to the Dealing Assistant or Employee for rectification.",
        "AUDIT & CONTROL: "
    )

    # ----------------- SECTION 10: CHECKLIST -----------------
    add_header("10. Summary Verification Checklist for End Users", 1)
    doc.add_paragraph("Use this quick checklist when inspecting the system on https://portal.nexgenerp.in:")

    checklist = [
        ("1", "Open Pay Bill & click 'Fetch Active Employees'", "All employees in unit loaded with 53% DA, HRA, NPS (10%+14%), Net Pay"),
        ("2", "Check Pay Bill Print Formats (5 Schedules)", "Monthly Pay Roster, NPS Annexure-II, GPF Schedule, Licence Fee, Bank Advice"),
        ("3", "Open Income Tax Statement", "12-month ledger, ₹75k Standard Deduction, Sec 115BAC slabs, 4% cess"),
        ("4", "Open Due-Drawn Arrears", "Month-by-month comparative matrix: Diff P&A - Diff NPS = Net Arrear"),
        ("5", "Test Leave Application (CCS Leave 1972)", "180-day continuous EL ceiling, Commuted Leave 2x HPL debit + medical proof"),
        ("6", "Test CEA Claim & CGHS Form MRC-S", "₹33,750 CEA & ₹1,01,250 Hostel cap (max 2 children), OPD/Indoor medical breakdown"),
        ("7", "Test Tour TA/DA Bill", "Level 14 to Level 5 hotel/food caps, duration slabs (<6h 30%, 6-12h 70%, >12h 100%)"),
        ("8", "Inspect Left Sidebar Navigation", "Full tree showing all 6 modules and all 15 statutory doctypes in one view")
    ]

    tbl_chk = doc.add_table(rows=len(checklist)+1, cols=3)
    tbl_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_chk.cell(0, 0).width = Inches(0.6)
    tbl_chk.cell(0, 1).width = Inches(2.7)
    tbl_chk.cell(0, 2).width = Inches(3.2)
    set_cell_background(tbl_chk.cell(0, 0), "1E3A8A")
    set_cell_background(tbl_chk.cell(0, 1), "1E3A8A")
    set_cell_background(tbl_chk.cell(0, 2), "1E3A8A")
    for col_i, h_txt in enumerate(["#", "Verification Action", "Expected Statutory Result"]):
        r = tbl_chk.cell(0, col_i).paragraphs[0].add_run(h_txt)
        r.font.bold = True; r.font.color.rgb = RGBColor(255, 255, 255)

    for idx, (c_num, c_act, c_res) in enumerate(checklist, 1):
        c0 = tbl_chk.cell(idx, 0); c1 = tbl_chk.cell(idx, 1); c2 = tbl_chk.cell(idx, 2)
        c0.width = Inches(0.6); c1.width = Inches(2.7); c2.width = Inches(3.2)
        bg = "F8FAFC" if idx%2==1 else "FFFFFF"
        set_cell_background(c0, bg); set_cell_background(c1, bg); set_cell_background(c2, bg)
        p0 = c0.paragraphs[0]; p0.add_run(c_num).font.size = Pt(9.5)
        p1 = c1.paragraphs[0]; r1 = p1.add_run(c_act); r1.font.bold = True; r1.font.size = Pt(9.5)
        p2 = c2.paragraphs[0]; p2.add_run(c_res).font.size = Pt(9.5)

    output_path = os.path.abspath(r'D:\Govt HR Payroll\Government_HR_Payroll_User_Verification_Guide.docx')
    doc.save(output_path)
    print(f"Successfully generated Word document at: {output_path}")

if __name__ == '__main__':
    create_user_guide()
