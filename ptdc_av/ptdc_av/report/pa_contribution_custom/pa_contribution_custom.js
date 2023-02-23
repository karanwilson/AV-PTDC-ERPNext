// Copyright (c) 2023, PTDC Labs and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PA Contribution Custom"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "60px"
		},

		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "60px"
		},

		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
			"width": "60px"
		},

		{
			"fieldname": "year_yyyy",
			"label": __("Year_YYYY"),
			"fieldtype": "Int",
			"width": "60px"
		}
	]
};
