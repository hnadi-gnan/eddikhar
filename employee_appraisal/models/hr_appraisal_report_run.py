# -*- coding:utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
'''
NOTES:
1-


TODO:
1-change the statuses that are not needed
2-change the view actions for status change later
3-complete the action wizard for creating the reports
4-We have to make sure that the lines generated are generated for the period of the settings


LEARNED THAT:
1-

READ ABOUT:
1-

'''


#this model is meant to include the bathc run of each appraisal run made by an admin (The HR admin in specific)
class HrAppraisalReportRun(models.Model):
    _name = 'hr.appraisal.report.run'
    _description = 'Appraisal Report Batches'
    _order = 'date_end desc'
    #needed
    name = fields.Char(required=True, readonly=True, states={'draft': [('readonly', False)]})
    #this is needed but needs to be changed to report ids
    '''
    slip_ids = fields.One2many('hr.payslip', 'payslip_run_id', string='Payslips', readonly=True,
        states={'draft': [('readonly', False)]})
    '''
    #this is needed
    #remember to remove the paid status
    state = fields.Selection([
        ('draft', 'New'),
        ('verify', 'Confirmed'),
        ('close', 'Done'),
        ('paid', 'Paid'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')
    appraisal_report_ids = fields.One2many('hr.appraisal.report', 
                                           'appraisal_report_run_id', 
                                           string='Appraisal Reports',
                                           readonly=True,
                                           states={'draft': [('readonly', False)]}
                                           )    
    #this is definitely needed and needs to be matched with the one in the report
    date_start = fields.Date(string='Date From', required=True, readonly=True,
        states={'draft': [('readonly', False)]}, default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    #this is definitely needed and needs to be matched with the one in the report
    date_end = fields.Date(string='Date To', required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    #this is not needed
    '''
    credit_note = fields.Boolean(string='Credit Note', readonly=True,
        states={'draft': [('readonly', False)]},
        help="If its checked, indicates that all payslips generated from here are refund payslips.")
    '''
    #this is needed but will change to be report count
    '''
    payslip_count = fields.Integer(compute='_compute_payslip_count')
    '''
    appraisal_report_count = fields.Integer(compute='_compute_appraisal_report_count')
    
    #this is needed
    company_id = fields.Many2one('res.company', string='Company', readonly=True, required=True,
        default=lambda self: self.env.company)
    #this is not needed
    '''
    country_id = fields.Many2one(
        'res.country', string='Country',
        related='company_id.country_id', readonly=True
    )
    '''
    #this is not needed
    '''
    country_code = fields.Char(related='country_id.code', readonly=True)
    '''
    #this is needed and changed right under neath it
    '''
    def _compute_payslip_count(self):
        for payslip_run in self:
            payslip_run.payslip_count = len(payslip_run.slip_ids)
    '''
    def _compute_appraisal_report_count(self):
        for appraisal_report_run in self:
            appraisal_report_run.appraisal_report_count = len(appraisal_report_run.appraisal_report_ids)
    
    #these are all needed for state change but will require modifications on the views
    def action_draft(self):
        self.write({'state': 'draft'})

    def action_open(self):
        self.write({'state': 'verify'})
    
    #this is needed and must change to lock all reports after closure, change is right underneath it
    '''
    #removed
    '''
    def action_close(self):
        if self._are_appraisal_reports_ready():
            self.write({'state': 'close'})
    #this one action is not needed for now as it is for the paid change
    '''
    def action_paid(self):
        self.mapped('slip_ids').action_payslip_paid()
        self.write({'state': 'paid'})
    '''
    #this is needed, but will change, and the change is right underneath it
    '''
    #removed
    '''
    def action_validate(self):
        appraisal_report_done_result = self.mapped('appraisal_report_ids').filtered(lambda appraisal_report: appraisal_report.state not in ['draft', 'cancel']).action_appraisal_report_done()
        self.action_close()
        return appraisal_report_done_result
    
    #this is definitely needed for the wizard of creating the draft appraisal reports and must be completed before th actions
    '''
    def action_open_payslips(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.payslip",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [['id', 'in', self.slip_ids.ids]],
            "name": "Payslips",
        }
    '''
    def action_open_appraisal_reports(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.appraisal.report",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [['id', 'in', self.appraisal_report_ids.ids]],
            "name": "Appraisal Reports",
        }
    #this is needed for the deletion cases, but it must be changed, change is right underneath it
    '''
    @api.ondelete(at_uninstall=False)
    def _unlink_if_draft_or_cancel(self):
        if any(self.filtered(lambda payslip_run: payslip_run.state not in ('draft'))):
            raise UserError(_('You cannot delete a payslip batch which is not draft!'))
        if any(self.mapped('slip_ids').filtered(lambda payslip: payslip.state not in ('draft', 'cancel'))):
            raise UserError(_('You cannot delete a payslip which is not draft or cancelled!'))
    '''
    @api.ondelete(at_uninstall=False)
    def _unlink_if_draft_or_cancel(self):
        if any(self.filtered(lambda appraisal_report_run: appraisal_report_run.state not in ('draft'))):
            raise UserError(_("You cannot delete an appraisal report run (batch) which is not draft"))
        if any(self.mapped('appraisal_report_ids').filtered(lambda appraisal_report: appraisal_report.state not in ('draft', 'cancel'))):
            raise UserError(_("You cannot delete an appraisal report that is not draft or cancelled"))
        
    #this is needed and is used in the status update of close action above
    '''
    def _are_payslips_ready(self):
        return all(slip.state in ['done', 'cancel'] for slip in self.mapped('slip_ids'))
    '''
    def _are_appraisal_reports_ready(self):
        return all(appraisal_report.state in ['done', 'cancel'] for appraisal_report in self.mapped('appraisal_report_ids'))

