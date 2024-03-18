# Copyright (c) 2023, PTDC Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PTPurchaseOrder(Document):
	# pass
	
	@frappe.whitelist()
	def query_projected_qty(self, item_code):
		# to enable an exact match in cases of similar item_codes such as 20, 020, 0020, etc., which are all considered same when matched as Integers
		# hence we need to type cast the item_code value as a String:-
		item_code_str = str(item_code)
		bin = frappe.qb.DocType('Bin')
		# bin is a doctype that stores the 'Projected Qty' docfield
		query_bin = frappe.qb.from_(bin).select(bin.projected_qty).where(bin.item_code == item_code).run()
		if query_bin:
			return query_bin[0][0]		# extracting the value from list query_bin
		return

	@frappe.whitelist()
	def get_rate_amount(self, item_code, qty):
		# to enable an exact match in cases of similar item_codes such as 20, 020, 0020, etc., which are all considered same when matched as Integers
		# hence we need to type cast the item_code value as a String:-
		item_code_str = str(item_code)
		rate = frappe.db.get_value('Item Price', {'item_code': item_code_str, 'buying':'1'}, ['price_list_rate'])
		if rate:
			amount = rate * qty
		else: amount = rate = 0
		return rate,amount

	@frappe.whitelist()
	def cancel_related_purchase_order(self, purchase_order_name):
		doc = frappe.get_doc('Purchase Order', purchase_order_name)
		doc.cancel()
		return doc.docstatus
