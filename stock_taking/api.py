import frappe

@frappe.whitelist()
def get_stock(item_code):
    return frappe.db.sql(f""" 
                         select  qty_after_transaction,valuation_rate  from
                         `tabStock Ledger Entry` where item_code=%s and warehouse='Stores - AC'
                         ORDER BY 
                         CAST(posting_date AS DATETIME) + CAST(posting_time AS TIME) DESC limit 1;
                         """,(item_code),
                         as_dict=True)

@frappe.whitelist()
def get_bin(**args):
    item_code = args.get('item_code')
    warehouse = args.get('warehouse')
    to=args.get('to')
    frappe.msgprint(item_code)

    return item_code


