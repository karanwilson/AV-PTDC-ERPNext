# Copyright (c) 2023, PTDC Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PTPurchaseOrderItem(Document):
	pass


def on_doctype_update():
	frappe.db.add_index("Purchase Order Item", ["item_code", "warehouse"])