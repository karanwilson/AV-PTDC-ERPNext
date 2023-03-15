import frappe
from frappe import _

# called from hooks.py when new 'Contribution Entry' documents are inserted
def add_contribution_payment_entry(doc, method):
	if doc.total_contribution > 0:		# in case of TOS, the total contribution may be 0
		contribution = frappe.get_doc({
			"doctype": "Payment Entry",
			"party_type": "Customer",
			"party": doc.participant_account,
			"paid_amount": doc.total_contribution,
			"paid_to": "Cash - PTDC",
			"received_amount": doc.total_contribution
		})
		contribution.insert()
		contribution.submit()
		# below statement updates the 'Contribution Entry' record with the related 'Payment Entry' record name
		frappe.db.set_value('Contribution Entry', doc.name, 'related_payment_entry', contribution.name)


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