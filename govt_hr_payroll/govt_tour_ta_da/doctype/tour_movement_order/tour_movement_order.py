# Copyright (c) 2026, NexGen ERP Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class TourMovementOrder(Document):
	def validate(self):
		self.validate_destinations()
		self.sync_station_to()

	def validate_destinations(self):
		if self.places_to_visit and len(self.places_to_visit) > 10:
			frappe.throw(_("Maximum 10 places of visit are allowed in a single Tour Movement Order. Found {0}.").format(len(self.places_to_visit)))

	def sync_station_to(self):
		if self.places_to_visit:
			destinations = [d.station_name.strip() for d in self.places_to_visit if d.station_name and d.station_name.strip()]
			if destinations:
				self.station_to = ", ".join(destinations)
