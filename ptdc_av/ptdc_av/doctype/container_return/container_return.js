// Copyright (c) 2023, PTDC Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Container Return', {
	// refresh: function(frm) {
	// }
	before_save: function(frm) {
		switch(frm.doc.container_type) {
			case "Milk Bottle 1 Litre":
				frm.set_value('total_credit', (frm.doc.quantity * 40));
				break;
			case "Milk Bottle 0.5 Litre":
				frm.set_value('total_credit', (frm.doc.quantity * 20))
				break;
			case "":
				
		}
	}
});
