# -*- coding: utf-8 -*-

from odoo import models, fields, api


class exchange_orders(models.Model):
    _name = 'exchange_orders.exchange_orders'
    _description = 'exchange_orders.exchange_orders'
    
    
    currency_field='company_currency_id', compute='_compute_amount_company_currency_signed')
    date = fields.Date(string= 'Date')
    is_reconciled = fields.Boolean(string="Is Reconciled", store=True,
        compute='_compute_reconciliation_status',
        help="Technical field indicating if the payment is already reconciled.")
    is_matched = fields.Boolean(string="Is Matched With a Bank Statement", store=True,
        compute='_compute_reconciliation_status',
        help="Technical field indicating if the payment has been matched with a statement line.")
    available_partner_bank_ids = fields.Many2many(
        comodel_name='res.partner.bank',
        compute='_compute_available_partner_bank_ids',
    )
    partner_bank_id = fields.Many2one('res.partner.bank', string="Recipient Bank Account",
        readonly=False, store=True, tracking=True,
        compute='_compute_partner_bank_id',
        domain="[('id', 'in', available_partner_bank_ids)]",
        check_company=True)
    is_internal_transfer = fields.Boolean(string="Internal Transfer",
        readonly=False, store=True,
        tracking=True,
        compute="_compute_is_internal_transfer")
    qr_code = fields.Char(string="QR Code",
        compute="_compute_qr_code",
        help="QR-code report URL to use to generate the QR-code to scan with a banking app to perform this payment.")
    paired_internal_transfer_payment_id = fields.Many2one('account.payment',
        help="When an internal transfer is posted, a paired payment is created. "
        "They are cross referenced trough this field", copy=False)

    # == Payment methods fields ==
    payment_method_line_id = fields.Many2one('account.payment.method.line', string='Payment Method',
        readonly=False, store=True, copy=False,
        compute='_compute_payment_method_line_id',
        domain="[('id', 'in', available_payment_method_line_ids)]",
        help="Manual: Pay or Get paid by any method outside of Odoo.\n"
        "Payment Acquirers: Each payment acquirer has its own Payment Method. Request a transaction on/to a card thanks to a payment token saved by the partner when buying or subscribing online.\n"
        "Check: Pay bills by check and print it from Odoo.\n"
        "Batch Deposit: Collect several customer checks at once generating and submitting a batch deposit to your bank. Module account_batch_payment is necessary.\n"
        "SEPA Credit Transfer: Pay in the SEPA zone by submitting a SEPA Credit Transfer file to your bank. Module account_sepa is necessary.\n"
        "SEPA Direct Debit: Get paid in the SEPA zone thanks to a mandate your partner will have granted to you. Module account_sepa is necessary.\n")
    available_payment_method_line_ids = fields.Many2many('account.payment.method.line',
        compute='_compute_payment_method_line_fields')
    hide_payment_method_line = fields.Boolean(
        compute='_compute_payment_method_line_fields',
        help="Technical field used to hide the payment method if the selected journal has only one available which is 'manual'")
    payment_method_id = fields.Many2one(
        related='payment_method_line_id.payment_method_id',
        string="Method",
        tracking=True,
        store=True
    )

    # == Synchronized fields with the account.move.lines ==
    amount = fields.Monetary(currency_field='currency_id')
    payment_type = fields.Selection([
        ('outbound', 'Send'),
        ('inbound', 'Receive'),
    ], string='Payment Type', default='inbound', required=True, tracking=True)
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
    ], default='customer', tracking=True, required=True)
    payment_reference = fields.Char(string="Payment Reference", copy=False, tracking=True,
        help="Reference of the document used to issue this payment. Eg. check number, file name, etc.")
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, readonly=False,
        compute='_compute_currency_id',
        help="The payment's currency.")
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer/Vendor",
        store=True, readonly=False, ondelete='restrict',
        compute='_compute_partner_id',
        domain="['|', ('parent_id','=', False), ('is_company','=', True)]",
        tracking=True,
        check_company=True)
    outstanding_account_id = fields.Many2one(
        comodel_name='account.account',
        string="Outstanding Account",
        store=True,
        compute='_compute_outstanding_account_id',
        check_company=True)
    destination_account_id = fields.Many2one(
        comodel_name='account.account',
        string='Destination Account',
        store=True, readonly=False,
        compute='_compute_destination_account_id',
        domain="[('user_type_id.type', 'in', ('receivable', 'payable')), ('company_id', '=', company_id)]",
        check_company=True)
    destination_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Destination Journal',
        domain="[('type', 'in', ('bank','cash')), ('company_id', '=', company_id), ('id', '!=', journal_id)]",
        check_company=True,
    )
    
