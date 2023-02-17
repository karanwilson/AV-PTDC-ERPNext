# Copyright (c) 2022, PTDC Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Individual(Document):
	# pass

	@frappe.whitelist()
	def enable_disable_pt_checkout(self, participant_account, action):
		if action == 'Enable':
			frappe.db.set_value('Customer', participant_account, 'disabled', False)
			return frappe.get_value('Customer', participant_account, 'disabled')
		else:
			frappe.db.set_value('Customer', participant_account, 'disabled', True)
			return frappe.get_value('Customer', participant_account, 'disabled')
