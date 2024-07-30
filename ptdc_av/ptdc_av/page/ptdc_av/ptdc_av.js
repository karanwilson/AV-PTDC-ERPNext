frappe.pages['ptdc_av'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'PTDC AV',
		single_column: true
	});

	//this.page.ptdc_av = new frappe.Ptdc_Av.ptdc_av(this.page);
}