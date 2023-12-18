import frappe
from frappe import _
from frappe.utils import flt
from posawesome.posawesome.api.posapp import get_available_credit, redeeming_customer_credit

# called from hooks.py when new 'Contribution Entry' documents are inserted
def add_contribution_payment_entry(doc, method):
	if doc.total_contribution > 0:		# in case of TOS, the total contribution may be 0
		account = frappe.get_value("Mode of Payment Account", {"parent": "Cash"}, "default_account")
		payment_entry = frappe.get_doc({
			"doctype": "Payment Entry",
			"party_type": "Customer",
			"party": doc.participant_account,
			"paid_amount": doc.total_contribution,
			"paid_to": account,
			"received_amount": doc.total_contribution
		})
		payment_entry.insert()
		payment_entry.submit()
		doc.payment_entry = payment_entry.name		# updates the 'Contribution Entry' record with the related 'Payment Entry' record name


# called from hooks.py when new 'Purchase Receipt' documents are inserted
# below we access 'Purchase Receipt Item' documents (via items[0]), which are a child doctype of 'Purchase Receipt' documents
def update_selling_price_list(doc, method):
	item_price = frappe.get_doc({
		"doctype": "Item Price",
		"item_code": doc.items[0].item_code,
		"uom": doc.items[0].uom,
		"price_list": "Standard Selling",
		"price_list_rate": doc.items[0].rate,
		"batch_no": doc.items[0].batch_no
	})
	item_price.insert()

def delete_item_price(doc, method):
	item_price_name = frappe.get_list('Item Price', filters = {"batch_no": doc.items[0].batch_no})	# returns a list of dicts (key value pairs)
	frappe.delete_doc('Item Price', item_price_name[0].name)	# item_price_name[0].name extracts the value of key 'name'


# called from hooks.py when new 'PT Purchase Order' documents are inserted
def create_purchase_order(doc, method):
	purchase_order = frappe.get_doc({
		"doctype": "Purchase Order",
		"supplier": doc.supplier,
	})
	# 'Purchase Order Item' is a child doctype of 'Purchase Order' document
	"""
	purchase_order_item = frappe.get_doc({
		"doctype": "Purchase Order Item",
		"item_code": doc.item_code,
		"qty": doc.required_qty,
		"schedule_date": doc.required_by,
		"parent": purchase_order.name,
		"parenttype": "Purchase Order",
		"parentfield": "items"
	})
	"""
	for item in doc.pt_po_items:
		purchase_order_item = frappe.get_doc({
			"doctype": "Purchase Order Item",
			"item_code": item.item_code,
			"qty": item.required_qty,
			"schedule_date": item.required_by,
			"parent": purchase_order.name,
			"parenttype": "Purchase Order",
			"parentfield": "items"
		})
		purchase_order.items.append(purchase_order_item)
	purchase_order.insert()
	purchase_order.submit()
	doc.purchase_order = purchase_order.name	# updates the 'PT Purchase Order' record with the related 'Purchase Order' record name


# called from pt_purchase_order.js
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def supplier_items(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql(
		"""
		select distinct parent, tabItem.item_name, tabItem.item_group
		from `tabItem Supplier`, tabItem
		where `tabItem Supplier`.parent = tabItem.name and supplier = %s
		""",
		txt
	)
	#return frappe.db.sql(
	#	"""
	#	select tabItem.item_code, tabItem.item_name, tabItem.item_group
	#	from tabItem
	#	join tabBatch
	#	on tabItem.item_code = tabBatch.item
	#	where tabBatch.supplier = %s
	#	""",
	#	txt
	#)

# called from hooks.py when new 'PT Purchase Receipt' documents are inserted
def create_purchase_receipt(doc, method):
	purchase_receipt = frappe.get_doc({
		"doctype": "Purchase Receipt",
		"supplier": doc.supplier,
	})
	# 'Purchase Recept Item' is a child doctype of 'Purchase Receipt' document
	purchase_receipt_item = frappe.get_doc({
		"doctype": "Purchase Receipt Item",
		"item_code": doc.item_code,
		"qty": doc.accepted_qty,
		"rate": doc.rate,
		"parent": purchase_receipt.name,
		"parenttype": "Purchase Receipt",
		"parentfield": "items"
	})
	purchase_receipt.items.append(purchase_receipt_item)
	purchase_receipt.insert()
	purchase_receipt.submit()
	doc.purchase_receipt = purchase_receipt.name	# updates the 'PT Purchase Receipt' record with the related 'Purchase Receipt' record name
	# doc.save is automatically called when the doc is submitted from the live UI

"""
# testing/temp feature: called from hooks.py when 'Container Returns' documents are inserted
# (these returns are now handled in the 'Pour Tous Checkout' app)
def container_return_credit(doc, method):
	return_credit = frappe.get_doc({
		"doctype": "Payment Entry",
		"party_type": "Customer",
		"party": doc.participant_account,
		"paid_amount": doc.total_credit,
		"paid_to": "Cash - PTDC",
		"received_amount": doc.total_credit
	})
	return_credit.insert()
	return_credit.submit()
"""

# called from hooks.py after a new 'Invent_bill_2023_11' document is inserted
def invent_billing_action(doc, method):
	fs_ac = (doc.account_number).replace(' PT','')
	customer_name = fs_ac + ' - ' + doc.account_name
	customer_id = frappe.get_value('Customer', {'customer_name': customer_name}, 'name')
	precision = frappe.db.get_single_value('System Settings', 'float_precision')
	sales_invoice_items = frappe.get_all(
		'Invent_bill_items_2023_2024',
		filters={'bill_id': doc.name},
		fields=['product_id', 'quantity', 'adjusted_quantity']
		)

	if doc.is_debit_bill == 'N':
		create_sales_invoice(customer_id, precision, sales_invoice_items)
	else:
		# 'reverse billing' as per 'Invent' workflow
		total_return_amount = 0.00
		for item in sales_invoice_items:
			qty = item['quantity']+item['adjusted_quantity']
			amount = flt(qty, precision) * flt(doc.price, precision)
			total_return_amount += amount
		# create payment entry for total_return_amount
		account = frappe.get_value("Mode of Payment Account", {"parent": "Cash"}, "default_account")
		payment_entry = frappe.get_doc({
			"doctype": "Payment Entry",
			"party_type": "Customer",
			"party": customer_id,
			"paid_amount": total_return_amount,
			"paid_to": account,
			"received_amount": total_return_amount
		})
		payment_entry.insert()
		payment_entry.submit()

def create_sales_invoice(customer_id, precision, sales_invoice_items):
	company = 'Auroville'
	sales_invoice = frappe.get_doc({
		"doctype": "Sales Invoice",
		"company": company,
		"customer": customer_id,
		"update_stock": 1,
		"disable_rounded_total": 1,
		"rounding_adjustment": 0.00,
		"conversion_rate": 1.00,
		"total_taxes_and_charges": 0.00,
		"base_total_taxes_and_charges": 0.00,
		"base_rounding_adjustment": 0.00,
		"rounded_total": 0.00,
		"base_rounded_total": 0.00,
		"update_billed_amount_in_sales_order": 0,
		"is_consolidated": 0,
		"plc_conversion_rate": 1.00,
		"price_list_currency": 'INR',
		"total_net_weight": 0.00,
		"discount_amount": 0.00,
		"base_discount_amount": 0.00,
		"additional_discount_percentage": 0.00,
		"total_billing_amount": 0.00,
		"total_billing_hours": 0.00,
		"base_paid_amount": 0.00,
		"paid_amount": 0.00,
		"base_change_amount": 0.00,
		"change_amount": 0.00,
		"write_off_amount": 0.00,
		"base_write_off_amount": 0.00,
		"loyalty_amount": 0.00,
		"commission_rate": 0.00,
		"total_commission": 0.00
	})

	total_qty = 0.00
	total_amount = 0.00
	for item in sales_invoice_items:
		product_code = frappe.get_value(
			'Invent_stock_product',
			{'product_id': item['product_id']},
			'product_code'
		)
		batch_no = frappe.get_value('Batch', {'item': product_code}, 'batch_id')
		rate, batch_qty = frappe.get_value('Item Price', {'batch_no': batch_no}, 'price_list_rate', 'batch_qty')
		qty = item['quantity']+item['adjusted_quantity']
		amount = flt(qty, precision) * flt(rate, precision)
		# create Sales Invoice Item records
		sales_invoice_item = frappe.get_doc({
			"doctype": "Sales Invoice Item",
			"item_code": product_code,
			"qty": flt(qty, precision),
			"actual_qty": flt(batch_qty, precision),
			"actual_batch_qty": 0.00,
			"delivered_qty": 0.00,
			"weight_per_unit": 0.00,
			"total_weight": 0.00,
			"batch_no": batch_no,
			"rate": flt(rate, precision),
			"base_rate": flt(rate, precision),
			"net_rate": flt(rate, precision),
			"base_net_rate": flt(rate, precision),
			"incoming_rate": flt(rate, precision),
			"price_list_rate": flt(rate, precision),
			"base_price_list_rate": flt(rate, precision),
			"margin_rate_or_amount": 0.00,
			"rate_with_margin": 0.00,
			"base_rate_with_margin": 0.00,
			"discount_percentage": 0.00,
			"stock_uom_rate": flt(rate, precision),
			"is_free_item": 0,
			"grant_commission": 1,
			"amount": amount,
			"net_amount": amount,
			"base_amount": amount,
			"base_net_amount": amount,
			"discount_amount": 0.00
		})
		sales_invoice.items.append(sales_invoice_item)
		total_qty += qty
		total_amount += amount
	sales_invoice.total_qty = flt(total_qty, precision)
	sales_invoice.base_total = sales_invoice.base_net_total = sales_invoice.net_total = sales_invoice.total = flt(total_amount, precision)
	sales_invoice.amount_eligible_for_commission = sales_invoice.base_grand_total = sales_invoice.grand_total = flt(total_amount, precision)
	sales_invoice.outstanding_amount = sales_invoice.grand_total

	if sales_invoice.outstanding_amount > 0 :
		data = {}
		# get the customer's current month balance using a pre-defined function from posapp.py (check the import statements above)
		# receives both 'outstanding invoices' (if any) and 'advance payments' (if any)
		data['customer_credit_dict'] = get_available_credit(customer_id, company)

		if data.get('customer_credit_dict'):
			# allocating/adjusting the invoice amount, against the customer's monthly balance
			is_payment_entry = 0
			data['redeemed_customer_credit'] = 0

			for voucher in data.get('customer_credit_dict'):
				if sales_invoice.outstanding_amount >= voucher.total_credit :
					voucher.credit_to_redeem = voucher.total_credit
					# here in case the voucher.total_credit is an 'outstanding amount',
					# then it will add on to the sales_invoice.outstanding_amount in the below statement, because (-) * (-) = (+)
					sales_invoice.outstanding_amount -= voucher.total_credit
					data['redeemed_customer_credit'] += voucher.credit_to_redeem
					advance_payment = update_advances_sales_invoice(voucher)
					if advance_payment:
						sales_invoice.append("advances", advance_payment)
						sales_invoice.is_pos = 0
						is_payment_entry = 1

				else:
					voucher.credit_to_redeem = sales_invoice.outstanding_amount
					sales_invoice.outstanding_amount = 0
					data['redeemed_customer_credit'] += voucher.credit_to_redeem
					advance_payment = update_advances_sales_invoice(voucher)
					if advance_payment:
						sales_invoice.append("advances", advance_payment)
						sales_invoice.is_pos = 0
						is_payment_entry = 1
	
	sales_invoice.set_missing_values()
	sales_invoice.save()
	sales_invoice.submit()
	# sales_invoice.total_advance		# WIP
	total_cash = 0		# cash payments are not accepted in PTDC
	payments = sales_invoice.payments
	cash_account = None		# this parameter is not used in the called function below
	redeeming_customer_credit(sales_invoice, data, is_payment_entry, total_cash, cash_account, payments)

# updating `tabSales Invoice Advance` and adding entry in Advances under Payments in the Sales Invoice
def	update_advances_sales_invoice(voucher):
	if voucher["type"] == "Advance" and voucher["credit_to_redeem"]:
		advance = frappe.get_doc("Payment Entry", voucher["credit_origin"])
		advance_payment = {
            "reference_type": "Payment Entry",
            "reference_name": advance.name,
            "remarks": advance.remarks,
            "advance_amount": advance.unallocated_amount,
            "allocated_amount": voucher["credit_to_redeem"],
        }
	return advance_payment
