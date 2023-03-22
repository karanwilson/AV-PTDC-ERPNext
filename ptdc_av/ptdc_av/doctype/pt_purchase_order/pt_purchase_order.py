# Copyright (c) 2023, PTDC Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PTPurchaseOrder(Document):
	#pass
	
	@frappe.whitelist()
	def query_projected_qty(self, item_code):
		bin = frappe.qb.DocType('Bin')
		return frappe.qb.from_(bin).select(bin.projected_qty).where(bin.item_code == item_code).run()
		# query_bin = frappe.qb.from_(bin).select(bin.projected_qty).where(bin.item_code == item_code).run()
		# return query_bin

	@frappe.whitelist()
	def cancel_related_purchase_order(self, purchase_order_name):
		doc = frappe.get_doc('Purchase Order', purchase_order_name)
		doc.cancel()
		return doc.status
