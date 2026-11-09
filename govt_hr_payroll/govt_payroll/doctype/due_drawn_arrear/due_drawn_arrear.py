# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class DueDrawnArrear(Document):
	def validate(self):
		self.calculate_arrears()

	def calculate_arrears(self):
		tot_diff_pna = 0.0
		tot_diff_nps = 0.0

		for item in self.items:
			# 1. Due side calculations
			due_bp = flt(item.due_basic_pay)
			due_da_rate = flt(item.due_da_rate)
			item.due_da_amount = round(due_bp * (due_da_rate / 100.0))

			due_hra_rate = flt(item.due_hra_rate)
			item.due_hra_amount = round(due_bp * (due_hra_rate / 100.0))

			due_tpt = flt(item.due_tpt_allowance)
			item.due_da_on_tpt = round(due_tpt * (due_da_rate / 100.0))

			item.due_total_pna = due_bp + item.due_da_amount + item.due_hra_amount + due_tpt + item.due_da_on_tpt
			item.due_nps_amount = round((due_bp + item.due_da_amount) * 0.10)

			# 2. Drawn side calculations
			dr_bp = flt(item.drawn_basic_pay)
			dr_da_rate = flt(item.drawn_da_rate)
			item.drawn_da_amount = round(dr_bp * (dr_da_rate / 100.0))

			dr_hra_rate = flt(item.drawn_hra_rate)
			item.drawn_hra_amount = round(dr_bp * (dr_hra_rate / 100.0))

			dr_tpt = flt(item.drawn_tpt_allowance)
			item.drawn_da_on_tpt = round(dr_tpt * (dr_da_rate / 100.0))

			item.drawn_total_pna = dr_bp + item.drawn_da_amount + item.drawn_hra_amount + dr_tpt + item.drawn_da_on_tpt
			item.drawn_nps_amount = round((dr_bp + item.drawn_da_amount) * 0.10)

			# 3. Differences
			item.diff_pna = item.due_total_pna - item.drawn_total_pna
			item.diff_nps = item.due_nps_amount - item.drawn_nps_amount
			item.net_arrear = item.diff_pna - item.diff_nps

			tot_diff_pna += item.diff_pna
			tot_diff_nps += item.diff_nps

		self.total_diff_pna = tot_diff_pna
		self.total_diff_nps = tot_diff_nps
		self.net_arrear_payable = tot_diff_pna - tot_diff_nps
