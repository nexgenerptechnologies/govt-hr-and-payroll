# Government HR and Payroll System (Frappe v16)

A specialized, lightweight, standalone **Government HR and Payroll System** developed on the **Frappe Framework v16**, fully compliant with **7th Central Pay Commission (7th CPC)** statutory rules and Government of India financial guidelines.

Built as a single standalone Frappe app (`govt_hr_payroll`) that can be deployed on any intranet/LAN server without requiring ERPNext or any corporate ERP overhead.

---

## 🌟 Key Modules & Features

### 1. 7th CPC Masters & Foundation (`Govt Masters`)
* **7th CPC Pay Matrix**: Pre-configured Levels 1 to 18 with complete 40-cell salary progressions (~3% statutory increments).
* **Government Office / Unit Master**: DDO ID, DDO Unit Code, PAO Code, CDA Code, CDA Nodal Office Name, Department Code, City Classification (X, Y, Z).
* **Comprehensive Govt Employee Master**:
  * Date of Next Increment (DNI: 01-Jan / 01-Jul).
  * Date of Retirement (DOR) automatic computation based on 60th birthday.
  * Re-employed pensioner pensionary benefit deduction (`*(-) Pension`).
  * Government Quarters allotment (Quarter No, Type, Floor, Location, AAN, License Fee recovery).
  * Statutory IDs: PRAN (NPS), GPF Account, CGHS Card, CGEGIS Group (A/B/C), PAN.
  * Banker details (Account No, Branch, IFSC, MICR).

### 2. Monthly Regular & Supplementary Pay Bills (`Govt Payroll`)
* **Automated Pay Bill Generation**: Single-click "Fetch Active Employees" with automatic calculation of:
  * Effective Basic Pay (`Basic Pay - Pension Deduction`).
  * Dearness Allowance (DA %) on Basic Pay.
  * House Rent Allowance (HRA % based on X/Y/Z city, ₹0 if Govt quarters allotted).
  * Transport Allowance (TPT) + DA on TPT.
  * NPS Tier-1 Contributions (Employee 10% + Government 14%).
  * GPF Subscriptions & Advances.
  * Central Govt Health Scheme (CGHS), CGEGIS, License Fee.
  * Income Tax (TDS) + 4% Health & Education Cess.
* **Official Government Print Formats**:
  1. **Monthly Pay and Allowances Bill** (Full landscape roster).
  2. **NPS Annexure-II Monthly Contribution Schedule** (Tier-1 10% & 14% breakdown with PAO/CDA codes).
  3. **GP Fund Schedule** (CDA Code, Unit, Month, Year, GPF No, Subscription & Refund).
  4. **Licence Fee Schedule** (Ministry/Unit, DDO ID, Quarter details, AAN, LF recovery).
  5. **Bank Payment Advice** (Disbursement schedule with IFSC/MICR and Net Pay).
  6. **Supplementary Pay Bill** (For off-cycle allowance releases).

### 3. Due vs Drawn Arrears Engine (`Govt Payroll`)
* **Comparative Due-Drawn Calculator**: Multi-month calculation for:
  * DA Rate Revisions (retrospective Dearness Allowance hikes).
  * Annual Increment Arrears (July / January DNI arrears).
  * Promotion / MACP scale revisions.
* **Statutory Calculation**:
  * Side-by-side computation of `Due (Basic + DA + HRA + TPT + NPS)` vs `Drawn (Basic + DA + HRA + TPT + NPS)`.
  * Computes `Diff of P&A`, `Diff of NPS`, and `Net Arrear Payable = Diff(P&A) - Diff(NPS)`.
* **Print Format**: Official **Due Drawn Statement** landscape sheet.

### 4. CCS Leave Rules 1972 & DO Part II Orders (`Govt Leave Management`)
* **Automated Half-Yearly Credit Engine**:
  * 15 days Earned Leave (EL) + 10 days Half Pay Leave (HPL) auto-credited on 01 January & 01 July.
  * **300-Day Ceiling & 15-Day Buffer Rule**: If an employee has 286–300 days balance, advance credit is placed into a separate buffer pool to set off against leaves taken during the half-year without exceeding the statutory 300-day limit.
* **Leave Application Workflow**:
  * Covers EL, HPL, Commuted Leave, Maternity, Paternity, CCL, and EOL.
  * Validates max 180 continuous EL days at a time.
  * Enforces medical certificate attachment for Commuted Leave (debits 2x HPL).
  * Captures Station Leave permission, address during absence, LTC block year, and leave encashment details.
* **Daily Order Part II (DO Part II)**:
  * Automatic generation of DO Part II / Sanction Order for service book entry upon leave approval.

---

## 🚀 Intranet / On-Premises Installation Guide

### Prerequisites
* **Server**: Ubuntu 22.04 LTS or 24.04 LTS with Static LAN IP (e.g., `192.168.1.50`).
* **Framework**: Frappe Framework v16 Bench.
* **Database**: MariaDB 10.6+.

### Step-by-Step Installation

```bash
# 1. Navigate to your frappe-bench directory
cd /home/frappe/frappe-bench

# 2. Get this app from GitHub
bench get-app https://github.com/nexgenerptechnologies/govt-hr-and-payroll.git

# 3. Create your intranet site (or use an existing site)
bench new-site hrpayroll.local --db-name govt_payroll_db

# 4. Install the app on the site
bench --site hrpayroll.local install-app govt_hr_payroll

# 5. Run migrations to initialize statutory masters and pay levels
bench --site hrpayroll.local migrate

# 6. Enable production mode for internal network access
sudo bench setup production frappe --yes
```

Access the system from any browser on your office network at `http://192.168.1.50` or `http://hrpayroll.local`.

---

## 📄 License
MIT License. Developed by NexGen ERP Technologies.
