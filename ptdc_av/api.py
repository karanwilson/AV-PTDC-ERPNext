import frappe
from frappe import _
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account


# called from hooks.py when a 'Purchase Receipt' document is submitted
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


# called from hooks.py when "Sales Invoice" documents are submitted
def payment_entry_for_return(doc, method):
	if doc.status == "Return":
		mop_cash_list = [
        	i.mode_of_payment
        	for i in doc.payments
        	if "cash" in i.mode_of_payment.lower() and i.type == "Cash"
    	]
		if len(mop_cash_list) > 0:
			cash_account = get_bank_cash_account(mop_cash_list[0], doc.company)
		else:
			cash_account = {
            	"account": frappe.get_value(
                	"Company", doc.company, "default_cash_account"
            	)
        }

    	# creating advance payment
		advance_payment_entry = frappe.get_doc(
            {
               	"doctype": "Payment Entry",
               	#"mode_of_payment": "Cash",
               	"paid_to": cash_account["account"],
               	"payment_type": "Receive",
               	"party_type": "Customer",
               	"party": doc.customer,
               	"paid_amount": -(doc.grand_total),
               	"received_amount": -(doc.grand_total),
               	"company": doc.company,
            }
        )

		advance_payment_entry.flags.ignore_permissions = True
		frappe.flags.ignore_account_permission = True
		advance_payment_entry.save()
		advance_payment_entry.submit()


# called from pt_purchase_order.js
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def supplier_items(doctype, txt, searchfield, start, page_len, filters):
	# using 'distinct' in the sql statement below because the current testing instance has 4 rows for each supplier-item combination in `tabItem Supplier`
	# this could be because the masters were reuploaded more than once (after deleting company/accounting data) during the testing..
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


# called from hooks.py when new 'PT Purchase Order' documents are inserted
def create_purchase_order(doc, method):
	purchase_order = frappe.get_doc({
		"doctype": "Purchase Order",
		"supplier": doc.supplier,
	})
	# 'Purchase Order Item' is a child doctype of 'Purchase Order' document

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


"""
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