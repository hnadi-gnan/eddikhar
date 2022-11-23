# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
'''
NOTES:
1-Most of the computation done in these fields are manual and so there is no automatic computation


TODO:
1-Link this to the appraisal report once you finish the main features
2-We need to link each appraisal line and appraisal report to a specific user or a specific employee who made the evaluation
3-I need to modify the way the rules of evaluation are fetched, the same flow will apply, using a button to generate items, but i WILL RETRIEVE BASED ON THE EMPLOYEES COMPOANY AND DEPARTMENT (ALLOWED KPI ITEMS)


LEARNED THAT:
1-

READ ABOUT:
1-

'''


#this model is meant to include the appraisal line of each appraisal report
#For now we will not need the payslip input class immitation as it serves another purpose in the original implementation
class HrAppraisalReportLine(models.Model):
    _name = 'hr.appraisal.report.line'
    _description = 'Appraisal Report Line'
    #_order = 'contract_id, sequence, code'
    
    #This is needed by default
    name = fields.Char(required=True)
    #We can choose to keep or remove this later
    note = fields.Text(string='Description')
    #this is not needed for now
    sequence = fields.Integer(required=True, index=True, default=5, help='Used to arrange sequence')
    #this field will not be needed as there are no computations in the appraisal for now, later maybe for coputation of attendance and other stuff
    #code = fields.Char(required=True, help="The code of salary rules can be used as reference in computation of other rules. " "In that case, it is case sensitive.")
    #this is needed and will change to be the report id this line is related to 
    #slip_id = fields.Many2one('hr.payslip', string='Pay Slip', required=True, ondelete='cascade')
    report_id = fields.Many2one('hr.appraisal.report', string = 'Report', required=True, ondelete='cascade')
    #this is needed but needs to be changed and mapped to a kpiitem
    #salary_rule_id = fields.Many2one('hr.salary.rule', string='Rule', required=True)
    kpiitem_id = fields.Many2one('hr.kpiitem', string = 'KPI Item', required = True)
    #this is not needed for now
    #contract_id = fields.Many2one('hr.contract', string='Contract', required=True, index=True)
    #this is needed
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    #this is not needed 
    #rate = fields.Float(string='Rate (%)', digits='Payroll Rate', default=100.0)
    #this is needed as score
    #amount = fields.Monetary()
    score = fields.Integer(string="Employee Score", help="The score of the employee on this item")
    #this is not needed 
    #quantity = fields.Float(digits='Payroll', default=1.0)
    #this is not needed 
    #total = fields.Monetary(compute='_compute_total', string='Total', store=True)
    #this is not needed 
    #amount_select = fields.Selection(related='salary_rule_id.amount_select', readonly=True)
    #this is not needed 
    #amount_fix = fields.Float(related='salary_rule_id.amount_fix', readonly=True)
    #this is not needed 
    #amount_percentage = fields.Float(related='salary_rule_id.amount_percentage', readonly=True)
    #this is not needed 
    #appears_on_payslip = fields.Boolean(related='salary_rule_id.appears_on_payslip', readonly=True)
    #this is not needed for now but might be used, specially since we added the kpiite category 
    #category_id = fields.Many2one(related='salary_rule_id.category_id', readonly=True, store=True)
    #this is not needed 
    #partner_id = fields.Many2one(related='salary_rule_id.partner_id', readonly=True, store=True)
    #this is not needed 
    #this is needed but it is going to be modified to link to the report's date, modified field is rigth underneath it
    #date_from = fields.Date(string='From', related="slip_id.date_from", store=True)
    date_from = fields.Date(string="From Date", related="report_id.date_from", store = True)
    #this is needed but it is going to be modified to link to the report's date, modified field is rigth underneath it
    #date_to = fields.Date(string='To', related="slip_id.date_to", store=True)
    date_to = fields.Date(string = 'To Date', related="report_id.date_to", store=True)
    #this is needed by default for multi company problems, but will change to match teh appraisla reports compamy
    #company_id = fields.Many2one(related='slip_id.company_id')
    company_id = fields.Many2one(related = 'report_id.company_id')
    #this is not needed
    #currency_id = fields.Many2one('res.currency', related='slip_id.currency_id')

    
    #this is not needed because it is related to the compuattion of the field
    '''
    @api.depends('quantity', 'amount', 'rate')
    def _compute_total(self):
        for line in self:
            line.total = float(line.quantity) * line.amount * line.rate / 100
    '''
    #this is needed but needs to be changed 
    '''
    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if 'employee_id' not in values or 'contract_id' not in values:
                payslip = self.env['hr.payslip'].browse(values.get('slip_id'))
                values['employee_id'] = values.get('employee_id') or payslip.employee_id.id
                values['contract_id'] = values.get('contract_id') or payslip.contract_id and payslip.contract_id.id
                if not values['contract_id']:
                    raise UserError(_('You must set a contract to create a payslip line.'))
        return super(HrPayslipLine, self).create(vals_list)
    ''' 
    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            #not needed for now, maybe extra checks later
            #or 'contract_id' not in values
            if 'employee_id' not in values:
                appraisal_report = self.env['hr.appraisal_report'].browse(values.get('appraisal_report_id'))
                values['employee_id'] = values.get('employee_id') or appraisal_report.employee_id.id
                #values['contract_id'] = values.get('contract_id') or payslip.contract_id and payslip.contract_id.id
                '''
                if not values['contract_id']:
                    raise UserError(_('You must set a contract to create a payslip line.'))
                '''
        return super(HrAppraisalReportLine, self).create(vals_list)
