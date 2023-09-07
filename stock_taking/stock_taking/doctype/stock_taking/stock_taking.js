frappe.ui.form.on('Stock Taking', {
	refresh(frm) {
		// your code here
		console.log('hi from script')
	},
	process_data(frm){
	    if (frm.is_dirty()){
	        // frappe.msgprint('not saved')
	    } else {
	        
	        // frappe.msgprint('saved')
	        let item = 'ABL8-1"'
	       
	        var total=0
	        let docw = frappe.get_doc("Stock Taking", 1);
	        docw.physical_stock_entry.forEach(d => {
				if (d.item_code == item) {
					 total += d.available_qty;
					 console.log(total)
				} // if itemcode condition finish here
			} 
			);// foreach finish here
			frappe.call({
			    method:"stock_taking.api.process_stock_entry",
			    args:{'stn':1},
			    callback:function(r){
			        console.log(r)
			    }
			})
			
			;

	    } // if frm.is_dirty finish here

	}
})

frappe.ui.form.on('Stock Taking Entry', {
	item_code(frm, cdt, cdn) {
	   const row = locals[cdt][cdn];
 		frappe.call({
 			// type: 'POST',
 			method: "stock_taking.api.get_stock",
 	 		args: {
 	 		    'item_code':row.item_code ,
 	 	 	    'warehouse' :frm.doc.warehouse,
 	 	 	    'to':frm.doc.to},
 	 		   
 		 	callback: function(r) {
 		 	            if (r.message.length>0){
  						 frappe.model.set_value(cdt, cdn, "available_qty",r.message[0].qty_after_transaction )
 						 frappe.model.set_value(cdt, cdn, "system_qty",r.message[0].qty_after_transaction )
 						 frappe.model.set_value(cdt, cdn, "valuation_rate",r.message[0].valuation_rate )
 						 frappe.model.set_value(cdt, cdn, "page_no",frm.doc.page_no )
 						 frappe.model.set_value(cdt, cdn, "counted_by",frm.doc.counted_by ) }
 						 else {
 						 frappe.model.set_value(cdt, cdn, "page_no",frm.doc.page_no )
 						 frappe.model.set_value(cdt, cdn, "counted_by",frm.doc.counted_by ) 
 						 }
    	     			
 			}
 		});
	}
})
