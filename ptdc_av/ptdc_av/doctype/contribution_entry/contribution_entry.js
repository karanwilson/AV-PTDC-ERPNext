// Copyright (c) 2023, PTDC Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contribution Entry', {
	// refresh: function(frm) {
	// },

	lunch_scheme(frm) {
		frm.set_value('lunch_scheme', frm.doc.lunch_scheme);
	},

	in_kind_scheme(frm) {
		frm.set_value('in_kind_scheme', frm.doc.in_kind_scheme);
	},

	personal_contribution(frm) {
		frm.set_value('personal_contribution', frm.doc.personal_contribution);
	},

	before_save(frm) {
		if (!frm.doc.tos) {
			frm.set_value('total_contribution', (frm.doc.lunch_scheme + frm.doc.in_kind_scheme + frm.doc.personal_contribution));
		} else {
			frm.set_value('total_contribution', frm.doc.tos_contribution);
		}
	},

	before_cancel(frm) {
		frm.call('cancel_related_payment_entry', { payment_entry_name: frm.doc.payment_entry })
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
