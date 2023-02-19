import frappe
from frappe import _

# called from hook.py when new 'Contribution Entry' documents are inserted
def add_contribution_payment_entry(doc, method):
	if doc.total_contribution > 0:		# in case of TOS, when total contribution may be 0
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