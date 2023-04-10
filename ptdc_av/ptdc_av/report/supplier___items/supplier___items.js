// Copyright (c) 2023, PTDC Labs and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Supplier - Items"] = {
	"filters": [
		{
			"fieldname": "supplier_name",
			"label": "Supplier Name",
			"fieldtype": "Link",
			"options": "Supplier",
			//"width": "300"	// this field is not having any effect on the width..
		},
	]
};
