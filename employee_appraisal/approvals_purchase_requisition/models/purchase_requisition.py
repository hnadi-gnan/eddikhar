from datetime import datetime, time

from odoo import api, fields, models, _

class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"
    
    
    @api.model
    def _prepare_requisition_line(self, product_id, product_qty, product_uom, req):
        uom_po_qty = product_uom._compute_quantity(product_qty, product_id.uom_po_id)
        return {
            'product_qty': uom_po_qty,
            'product_id': product_id.id,
            'product_uom_id': product_id.uom_po_id.id,
            'requisition_id': req.id,
        }