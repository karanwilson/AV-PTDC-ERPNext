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

	before_save: function(frm) {
		if (frm.doc.tos) {
			frm.set_value('total_contribution', frm.doc.tos_contribution);
		} else {
			frm.set_value('total_contribution', (frm.doc.lunch_scheme + frm.doc.in_kind_scheme + frm.doc.personal_contribution));
		}

		if (frm.doc.total_contribution > 0) {
			frm.call('add_contribution', {
				participant_account: frm.doc.participant_account,
				total_contribution: frm.doc.total_contribution
			}).then(r => {
				frm.set_value('related_payment_entry', (r.message));
			})
		}
	},

	before_cancel: function(frm) {
		// cancel the related Payment Entry
	}
});
