# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, cint

class TADAFinalClaim(Document):
	def validate(self):
		self.calculate_tada_bill()

	def calculate_tada_bill(self):
		hotel_cap, food_cap = get_7th_cpc_entitlements(self.pay_matrix_level)

		# 1. Journey Fare
		tot_fare_claim = 0.0
		tot_fare_pass = 0.0
		for j in self.journey_items:
			tot_fare_claim += flt(j.amount_claimed)
			if not j.amount_passed or j.amount_passed == 0:
				j.amount_passed = j.amount_claimed
			tot_fare_pass += flt(j.amount_passed)

		# 2. Hotel Accommodation
		tot_hotel_claim = 0.0
		tot_hotel_pass = 0.0
		for h in self.hotel_items:
			days = flt(h.no_of_days or 1)
			h.daily_rate_admissible = hotel_cap
			h.total_hotel_claimed = days * flt(h.daily_rate_claimed)
			
			admissible_daily = min(flt(h.daily_rate_claimed), hotel_cap)
			if not h.total_hotel_passed or h.total_hotel_passed == 0:
				h.total_hotel_passed = days * admissible_daily

			tot_hotel_claim += h.total_hotel_claimed
			tot_hotel_pass += flt(h.total_hotel_passed)

		# 3. Food Allowance
		tot_food_claim = 0.0
		tot_food_pass = 0.0
		for f in self.food_items:
			f.daily_food_limit = food_cap
			hrs = flt(f.absence_hours or 12)
			
			# Timing restriction under 7th CPC: <6h = 30%, 6-12h = 70%, >12h = 100%
			if hrs < 6:
				factor = 0.30
				f.slab_percentage = "30% (< 6 hrs)"
			elif hrs <= 12:
				factor = 0.70
				f.slab_percentage = "70% (6 to 12 hrs)"
			else:
				factor = 1.00
				f.slab_percentage = "100% (> 12 hrs)"

			max_admissible_food = round(food_cap * factor)
			if not f.food_amount_passed or f.food_amount_passed == 0:
				f.food_amount_passed = min(flt(f.food_amount_claimed), max_admissible_food)

			tot_food_claim += flt(f.food_amount_claimed)
			tot_food_pass += flt(f.food_amount_passed)

		self.total_fare_claimed = tot_fare_claim
		self.total_hotel_claimed = tot_hotel_claim
		self.total_food_claimed = tot_food_claim
		self.total_amount_claimed = tot_fare_claim + tot_hotel_claim + tot_food_claim

		adv = flt(self.advance_amount_received)
		self.balance_amount_claimed = self.total_amount_claimed - adv

		self.total_passed_amount = tot_fare_pass + tot_hotel_pass + tot_food_pass
		self.net_payable_or_refundable = self.total_passed_amount - adv

def get_7th_cpc_entitlements(pay_matrix_level):
	"""
	7th CPC TA/DA Entitlements as per Ministry of Finance OM / Document Folder 6:
	- Level 14 and above: Hotel cap ₹9,375/day, Food cap ₹1,500/day
	- Level 12 to Level 13A: Hotel cap ₹5,625/day, Food cap ₹1,250/day
	- Level 9 to Level 11: Hotel cap ₹2,812.50/day, Food cap ₹1,125/day
	- Level 6 to Level 8: Hotel cap ₹937.50/day, Food cap ₹1,000/day
	- Level 5 and below: Hotel cap ₹562.50/day, Food cap ₹625/day
	"""
	lvl_str = str(pay_matrix_level or "").replace("Level-", "").replace("Level", "").strip()
	
	try:
		lvl_num = cint(lvl_str)
	except Exception:
		lvl_num = 10

	if lvl_str in ["13A"]:
		return (5625.0, 1250.0)

	if lvl_num >= 14:
		return (9375.0, 1500.0)
	elif lvl_num >= 12:
		return (5625.0, 1250.0)
	elif lvl_num >= 9:
		return (2812.5, 1125.0)
	elif lvl_num >= 6:
		return (937.5, 1000.0)
	else:
		return (562.5, 625.0)
