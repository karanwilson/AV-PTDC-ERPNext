// Copyright (c) 2022, PTDC Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Individual', {
	// refresh: function(frm) {
	// },

	tos(frm) {
		if (!frm.doc.tos) {
			frm.set_value('tos_contribution', 0);
			frm.set_value('tos_until', null);
			frm.call('remove_tos_until_todo', { name: frm.doc.name })
				.then(r => {
					if (r.message) {
						frappe.show_alert({
							message: 'Deleted ToDo for disabling TOS',
							indicator:'red'
						}, 7);
					}
				})
		}
	},

	before_save: function(frm) {
		if (!frm.doc.tos) {
			frm.set_value('total_contribution', (frm.doc.lunch_scheme + frm.doc.in_kind_scheme + frm.doc.personal_contribution));
		} else {
			frm.set_value('total_contribution', frm.doc.tos_contribution);
		}

		if (frm.doc.tos && frm.doc.tos_until) {
			frm.call('tos_until_todo', {
				name: frm.doc.name,
				date: frm.doc.tos_until
			}).then(r => {
				let alert_message;
				switch(r.message) {
					case 'Open':
						alert_message = 'Created ToDo for disabling TOS on '+frm.doc.tos_until;
						frappe.show_alert({
							message: alert_message,
							indicator:'green'
						}, 7);
						break;
					case 'date_changed':
						alert_message = 'ToDo date for disabling TOS, changed to '+frm.doc.tos_until;
						frappe.show_alert({
							message: alert_message,
							indicator:'green'
						}, 7);
						break;
					default:
						alert_message = 'ToDo exists for disabling TOS on '+frm.doc.tos_until;
						frappe.show_alert({
							message: alert_message,
							indicator:'green'
						}, 7);
				}
			});
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
					const alert_message = 'PT Checkout has been Enabled for '+frm.doc.participant_name;
					frappe.show_alert({
						message: alert_message,
						indicator:'green'
					}, 7);
				} else {
					const alert_message = 'PT Checkout has been Disabled for '+frm.doc.participant_name;
					frappe.show_alert({
						message: alert_message,
						indicator:'red'
					}, 7);
				}

				frm.set_value('pt_checkout_action', null);
			});
		}
	}
});
