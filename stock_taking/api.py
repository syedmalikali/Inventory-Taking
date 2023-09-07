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
    



