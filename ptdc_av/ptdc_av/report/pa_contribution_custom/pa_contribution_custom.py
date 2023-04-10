# Copyright (c) 2023, PTDC Labs and contributors
# For license information, please see license.txt

import frappe, erpnext
from frappe import _, msgprint

def execute(filters=None):
	if not filters:
		return [], []
	# validate_filters(filters)

	columns, data = [], []

	columns = get_columns()

	data = get_data(filters)
	if not data:
		msgprint(_('No records found'))
		return columns, data

	return columns, data

def get_columns():
	return [
		{
			"fieldname": "party_name",
			"label": _("Participant"),
			"fieldtype": "Data",
			"width": 300,
		},

		{
			"fieldname": "address_line1",
			"label": _("Community"),
			"fieldtype": "Data",
			"width": 250,
		},

		{
			"fieldname": "paid_amount",
			"label": _("Contribution"),
			"fieldtype": "Currency",
			"width": 150,
		},

		{
			"fieldname": "remarks",
			"label": _("Remarks"),
			"fieldtype": "Small Text",
			"width": 350,
		},

		{
			"fieldname": "posting_date",
			"label": _("Received on"),
			"fieldtype": "Date",
			"width": 150,
		},
	]

def get_data(filters):
	if filters.month and filters.year_yyyy:
		report_month_year = frappe.db.sql(
			"""
			select `tabPayment Entry`.party_name, tabAddress.address_line1, `tabPayment Entry`.paid_amount,
			`tabPayment Entry`.remarks, `tabPayment Entry`.posting_date
			from `tabPayment Entry`
			join `tabDynamic Link`
			on `tabPayment Entry`.party = `tabDynamic Link`.link_name
			join tabAddress
			on `tabDynamic Link`.parent = tabAddress.name
			where monthname(`tabPayment Entry`.posting_date)=%(month)s and year(`tabPayment Entry`.posting_date)=%(year)s
			""",
			{
				'month': filters.month,
				'year' : filters.year_yyyy
			},
			as_dict=True,
		)
		return report_month_year

	elif filters.month:
		report_monthly = frappe.db.sql(
			"""
			select `tabPayment Entry`.party_name, tabAddress.address_line1, `tabPayment Entry`.paid_amount,
			`tabPayment Entry`.remarks, `tabPayment Entry`.posting_date
			from `tabPayment Entry`
			join `tabDynamic Link`
			on `tabPayment Entry`.party = `tabDynamic Link`.link_name
			join tabAddress
			on `tabDynamic Link`.parent = tabAddress.name
			where monthname(`tabPayment Entry`.posting_date)=%s
			""",
			filters.month,
			as_dict=True,
		)
		return report_monthly

	elif filters.year_yyyy:
		report_yearly = frappe.db.sql(
			"""
			select `tabPayment Entry`.party_name, tabAddress.address_line1, `tabPayment Entry`.paid_amount,
			`tabPayment Entry`.remarks, `tabPayment Entry`.posting_date
			from `tabPayment Entry`
			join `tabDynamic Link`
			on `tabPayment Entry`.party = `tabDynamic Link`.link_name
			join tabAddress
			on `tabDynamic Link`.parent = tabAddress.name
			where year(`tabPayment Entry`.posting_date)=%s
			""",
			filters.year_yyyy,
			as_dict=True,
		)
		return report_yearly
