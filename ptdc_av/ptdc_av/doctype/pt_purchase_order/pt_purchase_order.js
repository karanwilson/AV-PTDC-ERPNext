// Copyright (c) 2023, PTDC Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('PT Purchase Order', {
	// refresh: function(frm) {
	// },

	/*	Shifted to 'PT Purchase Order Item' child table
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
	*/

	before_save(frm) {
		var order_total=0;
		frm.doc.pt_po_items.forEach(item => {
			order_total += item.amount;
		});
		frm.set_value('total', order_total);
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

frappe.ui.form.on('PT Purchase Order Item', {
	item_code: function(frm, cdt, cdn) {
		var item = locals[cdt][cdn];

		if (item.item_code) {
			frm.call('query_projected_qty', { item_code: item.item_code})
				.then(r => {
					item.projected_qty = r.message;
					item.required_qty = r.message;
					frm.refresh_field('pt_po_items');	// pt_po_items is the field name for child table "PT Purchase Order Item" in parent "PT Purchase Order"
				}).then(r => {
					frm.call('get_rate_amount', { 
						item_code: item.item_code,
						qty: item.required_qty
						}).then(r => {
							item.rate = r.message[0];
							item.amount = r.message[1];
							frm.refresh_field('pt_po_items');	// pt_po_items is the field name for child table "PT Purchase Order Item" in parent "PT Purchase Order"
						});
				});
		} else {
			item.projected_qty = null;
			item.required_qty = null;
			item.rate = null;
			item.amount = null;
			frm.refresh_field('pt_po_items');	// pt_po_items is the field name for child table "PT Purchase Order Item" in parent "PT Purchase Order"
		}
	},

	required_qty: function(frm, cdt, cdn) {
		var item = locals[cdt][cdn];

		if (item.required_qty) {
			frm.call('get_rate_amount', { 
				item_code: item.item_code,
				qty: item.required_qty
				})
					.then(r => {
						item.rate = r.message[0];
						item.amount = r.message[1];
						frm.refresh_field('pt_po_items');	// pt_po_items is the field name for child table "PT Purchase Order Item" in parent "PT Purchase Order"
					});
		} else {
			item.rate = null;
			item.amount = null;
			frm.refresh_field('pt_po_items');	// pt_po_items is the field name for child table "PT Purchase Order Item" in parent "PT Purchase Order"
		}
	},

	rate: function(frm, cdt, cdn) {
		var item = locals[cdt][cdn];

		if (item.rate) {
			item.amount = item.rate * item.required_qty;
			frm.refresh_field('pt_po_items');	// pt_po_items is the field name for child table "PT Purchase Order Item" in parent "PT Purchase Order"
		}
	}
})