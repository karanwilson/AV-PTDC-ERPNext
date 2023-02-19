# Copyright (c) 2023, PTDC Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class ContributionEntry(Document):
	# pass

	@frappe.whitelist()
	def cancel_related_payment_entry(self, payment_entry_name):
		doc = frappe.get_doc('Payment Entry', payment_entry_name)
		doc.cancel()
		return doc.docstatus
