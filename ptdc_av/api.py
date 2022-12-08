import frappe
from frappe import _

def add_contribution(doc, method):
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