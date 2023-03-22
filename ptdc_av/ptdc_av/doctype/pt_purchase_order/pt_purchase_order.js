// Copyright (c) 2023, PTDC Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('PT Purchase Order', {
	// refresh: function(frm) {
	// },

	item_code(frm) {
		if (frm.doc.item_code) {
			frm.call('query_projected_qty', { item_code: frm.doc.item_code})
				.then(r => {
					frm.set_value('projected_qty', r.message);
					frm.set_value('required_qty', r.message);
				});
		} else {
			frm.set_value('projected_qty', null);
			frm.set_value('required_qty', null);
		}
	},

	before_cancel(frm) {
		frm.call('cancel_related_purchase_order', { purchase_order_name: frm.doc.purchase_order })
			.then(r => {
				if (r.message == 2) {	// a cancelled document has a docstatus of 2
					frappe.show_alert({
						message: __('Cancelled the related Purchase Order'),
						indicator: 'red'
					}, 7);
				}
			})
	}
});
