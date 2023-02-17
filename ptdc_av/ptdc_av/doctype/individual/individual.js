// Copyright (c) 2022, PTDC Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Individual', {
	// refresh: function(frm) {
	// },

	before_save: function(frm) {
		if (frm.doc.tos) {
			frm.set_value('total_contribution', (frm.doc.tos_contribution));
		} else {
			frm.set_value('total_contribution', (frm.doc.lunch_scheme + frm.doc.in_kind_scheme + frm.doc.personal_contribution));
		}

		if (frm.doc.pt_checkout_action) {
			frm.call('enable_disable_pt_checkout', {
				participant_account: frm.doc.participant_account,
				action: frm.doc.pt_checkout_action
			}).then(r => {
				if (r.message) {
					frm.set_value('pt_checkout_status', 'Disabled');
				} else {
					frm.set_value('pt_checkout_status', 'Enabled');
				}

				if (frm.doc.pt_checkout_action == 'Enable') {
					frappe.show_alert({
						message:__('PT Checkout has been Enabled'),
						indicator:'green'
					}, 5);
				} else {
					frappe.show_alert({
						message:__('PT Checkout has been Disabled'),
						indicator:'red'
					}, 5);
				}

				frm.set_value('pt_checkout_action', '');
			})
		}
	}
});
