from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ApprovalProductLine(models.Model):
    _inherit = 'approval.product.line'
    
    
    purchase_requisition_line_id = fields.Many2one('purchase.requisition.line')
    
    def _domain_product_id_requisition(self):
        """ Filters on product to get only the ones who are available on
        purchase in the case the approval request type is purchase. """
        # TODO: How to manage this when active model isn't approval.category ?
        if 'default_category_id' in self.env.context:
            category_id = self.env.context.get('default_category_id')
        elif self.env.context.get('active_model') == 'approval.category':
            category_id = self.env.context.get('active_id')
        else:
            return []
        category = self.env['approval.category'].browse(category_id)
        if category.approval_type == 'requisition':
            return [('purchase_ok', '=', True)]

    req_uom_qty = fields.Float(
        "Requisition UoM Quantity", compute='_compute_po_uom_qty_requisition',
        help="The quantity converted into the UoM used by the product in Purchase Order.")
    product_id = fields.Many2one(domain=lambda self: self._domain_product_id_requisition())

    @api.depends('approval_request_id.approval_type', 'product_uom_id', 'quantity')
    def _compute_po_uom_qty_requisition(self):
        for line in self:
            approval_type = line.approval_request_id.approval_type
            if approval_type == 'requisition' and line.product_id and line.quantity:
                uom = line.product_uom_id or line.product_id.uom_id
                line.req_uom_qty = uom._compute_quantity(
                    line.quantity,
                    line.product_id.uom_po_id
                )
            else:
                line.req_uom_qty = 0.0
                
                
    def _get_purchase_requisition_values(self):
        """ Get some values used to create a purchase requisition.
        Called in approval.request `action_create_purchase_requisitions`.
        """
        self.ensure_one()
        vals = {
            'origin': self.approval_request_id.name,
            'company_id': self.company_id.id
        }
        return vals

    
   
    def _get_purchase_requisitions_domain(self):
        """ Return a domain to get purchase requisitions where this product line could fit in.
        """
        self.ensure_one()
        domain = [
            ('company_id', '=', self.company_id.id),
            ('state', '=', 'draft'),
        ]
        return domain