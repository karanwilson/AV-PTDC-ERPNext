import frappe
from frappe import _

# called from hooks.py when new 'Contribution Entry' documents are inserted
def add_contribution_payment_entry(doc, method):
	if doc.total_contribution > 0:		# in case of TOS, the total contribution may be 0
		account = frappe.get_value("Mode of Payment Account", {"parent": "Cash"}, "default_account")
		payment_entry = frappe.get_doc({
			"doctype": "Payment Entry",
			"party_type": "Customer",
			"party": doc.participant_account,
			"paid_amount": doc.total_contribution,
			"paid_to": account,
			"received_amount": doc.total_contribution
		})
		payment_entry.insert()
		payment_entry.submit()
		doc.payment_entry = payment_entry.name		# updates the 'Contribution Entry' record with the related 'Payment Entry' record name


# called from hooks.py when new 'Purchase Receipt' documents are inserted
# below we access 'Purchase Receipt Item' documents (via items[0]), which are a child doctype of 'Purchase Receipt' documents
def update_selling_price_list(doc, method):
	item_price = frappe.get_doc({
		"doctype": "Item Price",
		"item_code": doc.items[0].item_code,
		"uom": doc.items[0].uom,
		"price_list": "Standard Selling",
		"price_list_rate": doc.items[0].rate,
		"batch_no": doc.items[0].batch_no
	})
	item_price.insert()

def delete_item_price(doc, method):
	item_price_name = frappe.get_list('Item Price', filters = {"batch_no": doc.items[0].batch_no})	# returns a list of dicts (key value pairs)
	frappe.delete_doc('Item Price', item_price_name[0].name)	# item_price_name[0].name extracts the value of key 'name'


# called from hooks.py when new 'PT Purchase Order' documents are inserted
def create_purchase_order(doc, method):
	purchase_order = frappe.get_doc({
		"doctype": "Purchase Order",
		"supplier": doc.supplier,
	})
	# 'Purchase Order Item' is a child doctype of 'Purchase Order' document
	"""
	purchase_order_item = frappe.get_doc({
		"doctype": "Purchase Order Item",
		"item_code": doc.item_code,
		"qty": doc.required_qty,
		"schedule_date": doc.required_by,
		"parent": purchase_order.name,
		"parenttype": "Purchase Order",
		"parentfield": "items"
	})
	"""
	for item in doc.pt_po_items:
		purchase_order_item = frappe.get_doc({
			"doctype": "Purchase Order Item",
			"item_code": item.item_code,
			"qty": item.required_qty,
			"schedule_date": item.required_by,
			"parent": purchase_order.name,
			"parenttype": "Purchase Order",
			"parentfield": "items"
		})
		purchase_order.items.append(purchase_order_item)
	purchase_order.insert()
	purchase_order.submit()
	doc.purchase_order = purchase_order.name	# updates the 'PT Purchase Order' record with the related 'Purchase Order' record name


# called from hooks.py when new 'PT Purchase Receipt' documents are inserted
def create_purchase_receipt(doc, method):
	purchase_receipt = frappe.get_doc({
		"doctype": "Purchase Receipt",
		"supplier": doc.supplier,
	})
	# 'Purchase Recept Item' is a child doctype of 'Purchase Receipt' document
	purchase_receipt_item = frappe.get_doc({
		"doctype": "Purchase Receipt Item",
		"item_code": doc.item_code,
		"qty": doc.accepted_qty,
		"rate": doc.rate,
		"parent": purchase_receipt.name,
		"parenttype": "Purchase Receipt",
		"parentfield": "items"
	})
	purchase_receipt.items.append(purchase_receipt_item)
	purchase_receipt.insert()
	purchase_receipt.submit()
	doc.purchase_receipt = purchase_receipt.name	# updates the 'PT Purchase Receipt' record with the related 'Purchase Receipt' record name
	# doc.save is automatically called when the doc is submitted from the live UI


# testing/temp feature: called from hooks.py when 'Container Returns' documents are inserted
# (these returns are now handled in the 'Pour Tous Checkout' app)
def container_return_credit(doc, method):
	return_credit = frappe.get_doc({
		"doctype": "Payment Entry",
		"party_type": "Customer",
		"party": doc.participant_account,
		"paid_amount": doc.total_credit,
		"paid_to": "Cash - PTDC",
		"received_amount": doc.total_credit
	})
	return_credit.insert()
	return_credit.submit()
