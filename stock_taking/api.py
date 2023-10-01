import frappe

@frappe.whitelist()
def get_stock(item_code,warehouse,to):
    return frappe.db.sql(f""" 
                         select  qty_after_transaction,valuation_rate  from
                         `tabStock Ledger Entry` where item_code=%s and warehouse=%s and posting_date<=%s
                         ORDER BY 
                         CAST(posting_date AS DATETIME) + CAST(posting_time AS TIME) DESC limit 1;
                         """,(item_code,warehouse,to),
                         as_dict=True)

@frappe.whitelist()
def process_stock_entry(stn):
    item_list = frappe.db.sql(f""" 
                        SELECT
                            it.item_code,
                            it.item_name,
                            IFNULL(SUM(ste.available_qty), 0) AS physical_qty,
                            IFNULL(MIN(ste.system_qty), 0) AS system_qty,
                            IFNULL(MIN(ste.valuation_rate), 0) AS rate
                        FROM
                            tabItem AS it
                        LEFT JOIN
                            `tabStock Taking Entry` AS ste ON it.item_code = ste.item_code AND ste.parent = 1
                        GROUP BY
                            it.item_code, it.item_name
                        HAVING
                            physical_qty <> 0 OR system_qty <> 0;
                    """,as_dict=True)
    return item_list

@frappe.whitelist()
def add_payment_entry():
    docPE = frappe.get_doc(dict(
            doctype = 'Payment Entry',
            docstatus = 1,
            mode_of_payment = "Cash - Khobar",
            paid_amount = doc.net_total,
            party_type = "Customer",
            party = doc.customer,
            payment_type = "Receive",
            payment_order_status = "Initiated",
            received_amount = doc.net_total,
            make_payment_via_journal_entry = 0,
            source_exchange_rate = 1,
            target_exchange_rate = 1,
            paid_to = "12012003 - Cash Sales - Khobar - AH",
            paid_to_account_currency = "SAR",
            paid_to_account_type = "Cash",
            reference_date = doc.posting_date,
            reference_no = "1",
            references = [{
                "doctype": "Payment Entry Reference",
                "allocated_amount": doc.net_total,
                "reference_doctype": "Sales Invoice",
                "reference_name": doc.name,
                "parentfield": "references",
                "parenttype": "Payment Entry",
                "exchange_rate": 1
            }]
        )).insert()
    frappe.msgprint("The Payment Entry " + docPE.name + " is created.")

    return