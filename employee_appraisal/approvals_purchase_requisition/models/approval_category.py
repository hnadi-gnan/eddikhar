from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    approval_type = fields.Selection(selection_add=[('requisition', 'Create Purchase agreement')])

    @api.onchange('approval_type')
    def _onchange_approval_type_requisition(self):
        if self.approval_type == 'requisition':
            self.has_product = 'required'
            self.has_quantity = 'required'