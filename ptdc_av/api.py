import frappe
from frappe import _

# called from hooks.py when new 'Contribution Entry' documents are inserted
def add_contribution_payment_entry(doc, method):
	if doc.total_contribution > 0:		# in case of TOS, the total contribution may be 0
		payment_entry = frappe.get_doc({
			"doctype": "Payment Entry",
			"party_type": "Customer",
			"party": doc.participant_account,
			"paid_amount": doc.total_contribution,
			"paid_to": "Cash - PTDC",
			"received_amount": doc.total_contribution
		})
		payment_entry.insert()
		payment_entry.submit()
		# below statement updates the 'Contribution Entry' record with the related 'Payment Entry' record name
		frappe.db.set_value('Contribution Entry', doc.name, 'payment_entry', payment_entry.name)


# called from hooks.py when new 'Purchase Receipt Item' documents (child doctype of 'Purchase Receipt') are inserted
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


# called from hooks.py when new 'PT Purchase Order' documents are inserted
def create_purchase_order(doc, supplier, item_code, qty, required_by):
	# pass
	purchase_order = frappe.get_doc({
		"supplier": doc.supplier,
		"item_code": doc.item_code,
		"qty": doc.required_qty,
		"schedule_date": doc.required_by
	})
	purchase_order.insert()
	purchase_order.submit()
	# below statement updates the 'PT Purchase Order' record with the related 'Purchase Order' record name
	frappe.db.set_value('PT Purchase Order', doc.name, 'purchase_order', purchase_order.name)


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