# Copyright (c) 2023, PTDC Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PTPurchaseReceipt(Document):
	# pass

	@frappe.whitelist()
	def cancel_related_purchase_receipt(self, purchase_receipt_name):
		doc = frappe.get_doc('Purchase Receipt', purchase_receipt_name)
		doc.cancel()
		#return doc.docstatus

		if doc.docstatus == 2:
			return doc.docstatus
		else:
			frappe.throw(
				title = 'Error',
				msg = "Unable to delete the 'Purchase Receipt', please verify the event hooks"
			)
