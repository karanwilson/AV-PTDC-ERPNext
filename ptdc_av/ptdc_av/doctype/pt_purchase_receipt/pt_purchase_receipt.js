// Copyright (c) 2023, PTDC Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('PT Purchase Receipt', {
	// refresh: function(frm) {
	// }

	// after_save(frm) {
	//	 window.location.reload();	// to display the updated 'Purchase Receipt' field 
	// },

	before_cancel(frm) {
		frm.call('cancel_related_purchase_receipt', { purchase_receipt_name: frm.doc.purchase_receipt })
			.then(r => {
				if (r.message == 2) {	// a cancelled document has a docstatus of 2
					frappe.show_alert({
						message: __('Cancelled the related Purchase Receipt'),
						indicator: 'red'
					}, 7);
				}
			})
	}
});
