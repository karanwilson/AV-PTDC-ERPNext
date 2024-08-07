// Copyright (c) 2023, PTDC Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contribution Entry', {
	refresh: function(frm) {
		frm.add_custom_button(__('Make FS Transfer'), function(){
			frappe.msgprint("Make an FS Transfer with this button");
		});
	},


	before_save(frm) {},

	before_cancel(frm) {
		frm.call('cancel_related_payment_entry', { payment_entry_name: frm.doc.payment_entry_id })
			.then(r => {
				if (r.message == 2) {	// a cancelled document has a docstatus of 2
					frappe.show_alert({
						message: __('Cancelled the related Payment Entry'),
						indicator: 'red'
					}, 7);
				}
			})
	}
});
