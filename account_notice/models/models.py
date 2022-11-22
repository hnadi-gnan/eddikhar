# -*- coding: utf-8 -*-

from odoo import fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    notice = fields.Boolean(string = 'Is Notice', required=True, readonly=True, copy=False, default = True)
    notice_type = fields.Selection(selection=[(
        'send', 'Send'), ('receive', 'Receive')], string='Notice Type', required=True, readonly=True, copy=False, tracking=True)

    def _inter_company_create_invoices(self):
        ''' Create cross company invoices.
        :return:        The newly created invoices.
        '''

        # Prepare invoice values.
        invoices_vals_per_type = {}
        inverse_types = {
            'in_invoice': 'out_invoice',
            'in_refund': 'out_refund',
            'out_invoice': 'in_invoice',
            'out_refund': 'in_refund',
        }
        notice_inverse = {
            'send': 'receive',
            'receive': 'send',
        }
        for inv in self:
            invoice_vals = inv._inter_company_prepare_invoice_data(inverse_types[inv.move_type], notice_inverse[inv.notice_type])
            invoice_vals['invoice_line_ids'] = []
            for line in inv.invoice_line_ids:
                invoice_vals['invoice_line_ids'].append((0, 0, line._inter_company_prepare_invoice_line_data()))

            inv_new = inv.with_context(default_move_type=invoice_vals['move_type']).new(invoice_vals)
            for line in inv_new.invoice_line_ids.filtered(lambda l: not l.display_type):
                # We need to adapt the taxes following the fiscal position, but we must keep the
                # price unit.
                price_unit = line.price_unit
                line.tax_ids = line._get_computed_taxes()
                line._set_price_and_tax_after_fpos()
                line.price_unit = price_unit

            invoice_vals = inv_new._convert_to_write(inv_new._cache)
            invoice_vals.pop('line_ids', None)

            invoices_vals_per_type.setdefault(invoice_vals['move_type'], [])
            invoices_vals_per_type[invoice_vals['move_type']].append(invoice_vals)

        # Create invoices.
        moves = self.env['account.move']
        for invoice_type, invoices_vals in invoices_vals_per_type.items():
            moves += self.with_context(default_type=invoice_type).create(invoices_vals)
        return moves


    def _inter_company_prepare_invoice_data(self, invoice_type, notice_type):
        ''' Get values to create the invoice.
        /!\ Doesn't care about lines, see '_inter_company_prepare_invoice_line_data'.
        :return: Python dictionary of values.
        '''
        self.ensure_one()
        # We need the fiscal position in the company (already in context) we are creating the
        # invoice, not the fiscal position of the current invoice (self.company)
        delivery_partner_id = self.company_id.partner_id.address_get(['delivery'])['delivery']
        fiscal_position_id = self.env['account.fiscal.position'].get_fiscal_position(
            self.company_id.partner_id.id, delivery_id=delivery_partner_id
        )
        return {
            'move_type': invoice_type,
            'ref': self.ref,
            'partner_id': self.company_id.partner_id.id,
            'currency_id': self.currency_id.id,
            'auto_generated': True,
            'auto_invoice_id': self.id,
            'invoice_date': self.invoice_date,
            'payment_reference': self.payment_reference,
            'invoice_origin': _('%s Invoice: %s') % (self.company_id.name, self.name),
            'fiscal_position_id': fiscal_position_id,
            'notice': self.notice,
            'notice_type': notice_type
        }

#   _name = 'account_notice.account_notice'
#     _description = 'account_notice.account_notice'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
