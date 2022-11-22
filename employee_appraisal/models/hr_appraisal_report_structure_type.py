# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

'''
NOTES:
1-

TODO:
1-

LEARNED THAT:
1-

READ ABOUT:
1-

'''


#this model is intended to try and create an appraisal report structure type that is set on each employee or department later as teh default appraisal structure or changed based on the duration ...etc
class HrAppraisalReportStructureType(models.Model):
    _inherit = 'hr.appraisal.report.structure.type'
    _description = 'Appraisal Report Structure Type'

    name = fields.Char('Appraisal Report Structure Type')
    #reference to this needs to be checked but we need the field overall
    default_schedule_appraisal_report = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi-annually', 'Semi-annually'),
        ('annually', 'Annually'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('bi-monthly', 'Bi-monthly'),
    ], string='Default Scheduled Appraisal Report', default='semi-annually',
    help="Defines the frequency of the appraisal report.")
    appraisal_report_struct_ids = fields.One2many('hr.appraisal.report.structure', 'type_id', string="Appraisal Reports Structures")
    default_struct_id = fields.Many2one('hr.appraisal.report.structure', string="Regular Appraisal Report Structure")
    #this is not needed for now
    '''
    default_work_entry_type_id = fields.Many2one('hr.work.entry.type', help="Work entry type for regular attendances.", required=True,
                                                 default=lambda self: self.env.ref('hr_work_entry.work_entry_type_attendance', raise_if_not_found=False))
    '''
    #this is not needed for now
    #wage_type = fields.Selection([('monthly', 'Monthly Fixed Wage'), ('hourly', 'Hourly Wage')], default='monthly', required=True)
    appraisal_report_struct_type_count = fields.Integer(compute='_compute_appraisal_report_struct_type_count', string='Appraisal Report Structure Type Count')

    def _compute_appraisal_report_struct_type_count(self):
        for appraisal_report_structure_type in self:
            appraisal_report_structure_type.struct_type_count = len(appraisal_report_structure_type.struct_ids)

    #this is not needed as it will be the same for all.
    '''
    def _check_country(self, vals):
        country_id = vals.get('country_id')
        if country_id and country_id not in self.env.companies.mapped('country_id').ids:
            raise UserError(_('You should also be logged into a company in %s to set this country.', self.env['res.country'].browse(country_id).name))
    '''
    
    def write(self, vals):
        #not needed
        '''
        if self.env.context.get('payroll_check_country'):
            self._check_country(vals)
        '''
        return super().write(vals)

    @api.model
    def create(self, vals):
        #not needed
        '''
        if self.env.context.get('payroll_check_country'):
            self._check_country(vals)
        '''
        return super().create(vals)

