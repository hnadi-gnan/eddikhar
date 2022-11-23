#-*- coding:utf-8 -*-

from odoo import api, fields, models, _
'''
NOTES:
1-

TODO:
1-

LEARNED THAT:
1-self.env.ref is used to Fetching record using XML id

READ ABOUT:
1-the function get_default_report_id

'''



class HrAppraisalReportStructure(models.Model):
    _name = 'hr.appraisal.report.structure'
    _description = 'Appraisal Report Structure'

    '''
    @api.model
    def _get_default_report_id(self):
        return self.env.ref('hr_payroll.action_report_payslip', False)
    '''
    #this is definitely needed but requires some changes as it doesnt match teh purpose of returning defauklt kpi items
    '''
    @api.model
    def _get_default_rule_ids(self):
        return [
            (0, 0, {
                'name': _('Basic Salary'),
                'sequence': 1,
                'code': 'BASIC',
                'category_id': self.env.ref('hr_payroll.BASIC').id,
                'condition_select': 'none',
                'amount_select': 'code',
                'amount_python_compute': 'result = payslip.paid_amount',
            }),
            (0, 0, {
                'name': _('Gross'),
                'sequence': 100,
                'code': 'GROSS',
                'category_id': self.env.ref('hr_payroll.GROSS').id,
                'condition_select': 'none',
                'amount_select': 'code',
                'amount_python_compute': 'result = categories.BASIC + categories.ALW',
            }),
            (0, 0, {
                'name': _('Deduction'),
                'sequence': 198,
                'code': 'DEDUCTION',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.DEDUCTION',
                'amount_select': 'code',
                'amount_python_compute': """result = -inputs.DEDUCTION.amount
result_name = inputs.DEDUCTION.name""",
            }),
            (0, 0, {
                'name': _('Attachment of Salary'),
                'sequence': 174,
                'code': 'ATTACH_SALARY',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.ATTACH_SALARY',
                'amount_select': 'code',
                'amount_python_compute': """result = -inputs.ATTACH_SALARY.amount
result_name = inputs.ATTACH_SALARY.name""",
            }),
            (0, 0, {
                'name': _('Assignment of Salary'),
                'sequence': 174,
                'code': 'ASSIG_SALARY',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.ASSIG_SALARY',
                'amount_select': 'code',
                'amount_python_compute': """result = -inputs.ASSIG_SALARY.amount
result_name = inputs.ASSIG_SALARY.name""",
            }),
            (0, 0, {
                'name': _('Child Support'),
                'sequence': 174,
                'code': 'CHILD_SUPPORT',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.CHILD_SUPPORT',
                'amount_select': 'code',
                'amount_python_compute': """result = -inputs.CHILD_SUPPORT.amount
result_name = inputs.CHILD_SUPPORT.name""",
            }),
            (0, 0, {
                'name': _('Reimbursement'),
                'sequence': 199,
                'code': 'REIMBURSEMENT',
                'category_id': self.env.ref('hr_payroll.ALW').id,
                'condition_select': 'python',
                'condition_python': 'result = inputs.REIMBURSEMENT',
                'amount_select': 'code',
                'amount_python_compute': """result = inputs.REIMBURSEMENT.amount
result_name = inputs.REIMBURSEMENT.name""",
            }),
            (0, 0, {
                'name': _('Net Salary'),
                'sequence': 200,
                'code': 'NET',
                'category_id': self.env.ref('hr_payroll.NET').id,
                'condition_select': 'none',
                'amount_select': 'code',
                'amount_python_compute': 'result = categories.BASIC + categories.ALW + categories.DED',
            })
        ]
    '''
    #this is needed
    name = fields.Char(required=True)
    #this might be needed and might be removed depends on the usability purpose of the final product
    code = fields.Char()
    #this is needed
    active = fields.Boolean(default=True)
    #tjis is needed
    type_id = fields.Many2one(
        'hr.appraisal.report.structure.type', required=True)
    #this is definitely no tneeded
    #country_id = fields.Many2one('res.country', string='Country', default=lambda self: self.env.company.country_id)
    #this is needed
    note = fields.Html(string='Description')
    #This is needed, but must change to map to kpiitem and also the relationship must be added
    rule_ids = fields.One2many(
        'hr.kpiitem', 'struct_id',
        string='Salary Rules', default=_get_default_rule_ids)
    report_id = fields.Many2one('ir.actions.report',
        string="Report", domain="[('model','=','hr.payslip'),('report_type','=','qweb-pdf')]", default=_get_default_report_id)
    payslip_name = fields.Char(string="Payslip Name", translate=True,
        help="Name to be set on a payslip. Example: 'End of the year bonus'. If not set, the default value is 'Salary Slip'")
    unpaid_work_entry_type_ids = fields.Many2many(
        'hr.work.entry.type', 'hr_payroll_structure_hr_work_entry_type_rel')
    use_worked_day_lines = fields.Boolean(default=True, help="Worked days won't be computed/displayed in payslips.")
    schedule_pay = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi-annually', 'Semi-annually'),
        ('annually', 'Annually'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('bi-monthly', 'Bi-monthly'),
    ], compute='_compute_schedule_pay', store=True, readonly=False,
    string='Scheduled Pay', index=True,
    help="Defines the frequency of the wage payment.")
    input_line_type_ids = fields.Many2many('hr.payslip.input.type', string='Other Input Line')

    @api.depends('type_id')
    def _compute_schedule_pay(self):
        for structure in self:
            if not structure.type_id:
                structure.schedule_pay = 'monthly'
            elif not structure.schedule_pay:
                structure.schedule_pay = structure.type_id.default_schedule_pay

