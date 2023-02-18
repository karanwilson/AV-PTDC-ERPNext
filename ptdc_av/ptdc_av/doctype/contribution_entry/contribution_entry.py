# Copyright (c) 2023, PTDC Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ContributionEntry(Document):
	# pass

	@frappe.whitelist()
	def add_contribution(self, participant_account, total_contribution):
		contribution = frappe.get_doc({
			"doctype": "Payment Entry",
			"party_type": "Customer",
			"party": participant_account,
			"paid_amount": total_contribution,
			"paid_to": "Cash - PTDC",
			"received_amount": total_contribution
		})
		contribution.insert()
		contribution.submit()
		return contribution.name
