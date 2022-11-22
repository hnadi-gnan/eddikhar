from dateutil.relativedelta import relativedelta
from odoo import fields, models


#This model is intended to link the appraisals of the employee to his profile (similar to payslips for employees)

'''
TODO: 
1-Add the groups on the model, similar to group on payslip count and the reg number fields, and furter understand the group property on the fields
2-Remove all the comments after you finished of all old codes (They arekept for reference now)
3-Add the average of appraisal grades (Per annum) before they are sumed to the next round


'''

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'
    #this is needed but requires change to be mapped to the appraisal report
    appraisal_report_ids = fields.One2many('hr.appraisal.report', 'employee_id', string='Appraisal Reports', readonly=True)
        #slip_ids = fields.One2many('hr.payslip', 'employee_id', string='Payslips', readonly=True)
    #this is needed but requires change to be mapped to appraisal report count
    appraisal_report_count = fields.Integer(compute = '_compute_appraisal_report_count', string='Appraisal Reports Count')
        #payslip_count = fields.Integer(compute='_compute_payslip_count', string='Payslip Count', groups="hr_payroll.group_hr_payroll_user")
    #this is needed but requires validation with the organization
    registration_number = fields.Char('Registration Number of the Employee', groups="hr.group_hr_user", copy=False)
    #this is not needed
    '''
    salary_attachment_ids = fields.One2many(
        'hr.salary.attachment', 'employee_id',
        string='Salary Attachments', groups="hr_payroll.group_hr_payroll_user"'
    '''
    #this is not needed
    '''
    salary_attachment_count = fields.Integer(
        compute='_compute_salary_attachment_count', string="Salary Attachment Count",
        groups="hr_payroll.group_hr_payroll_user")
    '''
    #this is not needed
    #mobile_invoice = fields.Binary(string="Mobile Subscription Invoice", groups="hr_contract.group_hr_contract_manager")
    #this is not needed
    #sim_card = fields.Binary(string="SIM Card Copy", groups="hr_contract.group_hr_contract_manager")
    #this is not needed
    #internet_invoice = fields.Binary(string="Internet Subscription Invoice", groups="hr_contract.group_hr_contract_manager")
    #this constraint is needed if we r going to use the reg number
    _sql_constraints = [
        ('unique_registration_number', 'UNIQUE(registration_number, company_id)', 'No duplication of registration numbers is allowed')
    ]
    #newly added fields
    last_e_appraisal_date = fields.Date(string = "Last Appraisal Report Date", compute= '_compute_last_appraisal_report_date', readonly=True,)
    employee_grade = fields.Integer(string="Employee Grade", help = "This represents the grade of the employee (Please note that this is not used in all organizations)")
    #excluded_kpiitems_ids = 
    
    #this is needed to compute the count o fthe appraisal report btu requires change to be mapped to the appraisal report
    def _compute_appraisal_report_count(self):
        for employee in self:
            employee.appraisal_report_count = len(employee.appraisal_report_ids)
    
    '''
    def _compute_payslip_count(self):
        for employee in self:
            employee.payslip_count = len(employee.slip_ids)

    def _compute_salary_attachment_count(self):
        for employee in self:
            employee.salary_attachment_count = len(employee.salary_attachment_ids)
    '''
    #newly added methods
    #this might not work
    def _compute_last_appraisal_report_date(self):
        for employee in self:
            employee.last_e_appraisal_date = employee.appraisal_report_ids[:-1].date_to