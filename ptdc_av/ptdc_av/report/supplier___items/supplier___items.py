# Copyright (c) 2023, PTDC Labs and contributors
# For license information, please see license.txt

import frappe, erpnext
from frappe import msgprint

from erpnext.stock.stock_ledger import get_previous_sle
from frappe.utils import nowdate, nowtime

def execute(filters=None):
	columns, data = [], []

	if filters:
		columns = get_columns()
		data = get_data(filters)
		if not data:
			msgprint('No records found')
			return columns, data

	return columns, data

def get_columns():
	return [
		{
			"fieldname": "item_code",
			"label": "Code",
			"fieldtype": "Data",
			"width": 60
		},

		{
			"fieldname": "item_name",
			"label": "Description",
			"fieldtype": "Data",
			"width": 400
		},

		{
			"fieldname": "item_group",
			"label": "Category",
			"fieldtype": "Data",
			"width": 200
		},

		{
			"fieldname": "last_purchase_rate",
			"label": "Buying Price",
			"fieldtype": "Currency",
			"width": 125
		},

		{
			"fieldname": "name",
			"label": "Batch",
			"fieldtype": "Data",
			"width": 150
		},

		{
			"fieldname": "batch_qty",
			"label": "Current Stock",
			"fieldtype": "Float",
			"width": 115
		},

		{
			"fieldname": "stock_value",
			"label": "Total Value",
			"fieldtype": "Currency",
			"width": 125
		},
	]

"""
		{
			"fieldname": "address_line1",
			"label": "Supplier Address",
			"fieldtype": "Data",
			"width": 300
		},

		{
			"fieldname": "phone",
			"label": "Phone",
			"fieldtype": "Data",
			"width": 150
		},

		{
			"fieldname": "mobile_no",
			"label": "Mobile No.",
			"fieldtype": "Data",
			"width": 200
		}
"""


def get_data(filters):
	if filters:
		report_data = frappe.db.sql(
			"""
			select tabItem.item_code, tabItem.item_name, tabItem.item_group, tabItem.last_purchase_rate, tabBatch.name, tabBatch.batch_qty
			from tabItem
			join tabBatch
			on tabItem.item_code = tabBatch.item
			where tabBatch.supplier = %s
			""",
			filters.supplier_name,
			as_dict = True
		)

		for row in report_data:
			row["stock_value"] = row["batch_qty"] * row["last_purchase_rate"]

		return report_data
