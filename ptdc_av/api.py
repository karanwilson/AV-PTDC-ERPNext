import frappe
from frappe import _

def add_contribution(doc, method):
	if doc.total_contribution > 0:
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