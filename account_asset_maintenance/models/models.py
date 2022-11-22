# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    equipment_id = fields.Many2one('maintenance.equipment', string = 'Equipment', store = True)     
    
    
class AccountAsset(models.Model):
    _inherit = 'account.asset'

    equipment_id = fields.Many2one('maintenance.equipment', string = 'Equipment', compute='_compute_equipment_id')

    @api.onchange('original_move_line_ids')
    def _compute_equipment_id(self):
        for record in self:
            if len(record.original_move_line_ids.equipment_id) > 1:
                raise UserError(_("All the lines should be from the same vehicle"))
            record.equipment_id = record.original_move_line_ids.equipment_id

    def action_open_equipment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.equipment',
            'res_id': self.equipment_id.id,
            'view_ids': [(False, 'form')],
            'view_mode': 'form',
        }                                          
                    


# class account_asset_maintenance(models.Model):
#     _name = 'account_asset_maintenance.account_asset_maintenance'
#     _description = 'account_asset_maintenance.account_asset_maintenance'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
