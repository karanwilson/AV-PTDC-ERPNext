// Copyright (c) 2023, PTDC Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contribution Entry', {
	// refresh: function(frm) {
	// }
	before_save: function(frm) {
		frm.set_value('total_contribution', (frm.doc.lunch_scheme + frm.doc.in_kind_scheme + frm.doc.personal_contribution))
	}
});
