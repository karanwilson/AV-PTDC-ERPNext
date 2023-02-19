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


	@frappe.whitelist()
	def tos_until_todo(self, name, date):
		description = 'Disable TOS for '+name
		if not frappe.db.exists('ToDo', {
			'description': description,
			'date': date
			}):

			if frappe.db.exists('ToDo', {'description': description}):
				# in case user has changed the TOS_until date
				# (because this condition matched when the previous one with date field didn't)
				existing_ToDo_name = frappe.db.get_value('ToDo', {'description': description}, 'name')
				frappe.db.set_value('ToDo', existing_ToDo_name, 'date', date)
				return 'date_changed'

			doc = frappe.new_doc('ToDo')
			doc.date = date		# due date
			doc.description = description
			# doc.owner = 		# allocated to
			doc.reference_type = 'Individual'
			doc.reference_name = name		# Individual who is TOS
			doc.insert()
			return doc.status
		else:
			return


	@frappe.whitelist()
	def remove_tos_until_todo(self, name):
		description = 'Disable TOS for '+name
		if frappe.db.exists('ToDo', {'description': description}):
			frappe.db.delete('ToDo', {'description': description})
			return True
		else:
			return False
