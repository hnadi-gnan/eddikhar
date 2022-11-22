# -*- coding: utf-8 -*-

'''
What am I trying to do:

First:
    1-I am trying to first create a model that can create KPIs or appriasal metrics/parameters dynamically.
    2-Each metric or KPI created by the user can be allocated to a specific deprtment or all deprtments or have specific constraints to be discussed later.

Second:
    1-Each employee is going to be connected to his yearly review report, 
    2-The report for each employee should be created automatically after the metric values have been intered in the yearly appraisal inventory.
    
Third:
    1-I would like to create a model that is simlar to inventory, the model's idea is for 
        1.1-The HR to create an inventory/aapraisal entry, 
        1.2-Simply assign the reponsible(S) for filling out the employee appriasal values.
        1.3-Assign the to be appraised by department, or by name (this is a many field because one appraisal form can be used for many departments or many employees).
        1.4-Assign a due date or validity date.
        1.5-Only the HR can approve the form once completed.
    2-After the creation of the record an inventory form will be dynamically created similar to the one used for inventory
    3-The assigned will have access and simply be able to enter a new record per employee.
    4-In teh settings there should be an option for how many times an employee can be appraised per year.
    5-After the completion and approval fo the appraisal from the HR, the employee record should be connected to that report of hi, mntioned in second part above.
    6-Each employee will have a performance file, similar to the idea of the medical profile to include his grade and his report


'''
'''
TODO:
1-remember to add the category in the view
2-We have to add the minimmum duration of appraisal,
3-


LEARNED THAT:
1-

READ ABOUT:
1-

'''



# from odoo import models, fields, api
from odoo import api, fields, models, _
import logging
from odoo.exceptions import RedirectWarning, UserError, ValidationError

_logger = logging.getLogger(__name__)
# class employee_appraisal(models.Model):
#     _name = 'employee_appraisal.employee_appraisal'
#     _description = 'employee_appraisal.employee_appraisal'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#          †   record.value2 = float(record.value) / 100

#first I will define the dynamic kpi list as per hanadis demo

'''class AppraisalForm(models.Model):
    name = fields.Char(string = 'KPI element Name'
    '''

class AppraisalForm(models.Model):
    _name = 'hr.appraisalform'

class KpiItemCategory(models.Model):
    _name = 'hr.kpiitem.category'
    _description = 'KPI Item Category'

    name = fields.Char(required=True, translate=True)
    #this is not needed
    #code = fields.Char(required=True)
    #this is for multi layered category functionality
    parent_id = fields.Many2one('hr.kpiitem.category', string='Parent',
        help="Linking a KPI Item category to its parent is used only for the reporting purpose.")
    children_ids = fields.One2many('hr.kpiitem.category', 'parent_id', string='Children')
    items = fields.One2many('hr.kpiitem', 'category_id', string='Related KPI Items')
    note = fields.Html(string='Description')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error! You cannot create recursive hierarchy of KPI Item Category.'))
    #this is not needed, as it return the sum of the items on this rule of category, it might be useful later to sum the result of the appraisal on each item in the list of the parent category and its children
    '''
    def _sum_salary_rule_category(self, localdict, amount):
        self.ensure_one()
        if self.parent_id:
            localdict = self.parent_id._sum_salary_rule_category(localdict, amount)
        localdict['categories'].dict[self.code] = localdict['categories'].dict.get(self.code, 0) + amount
        return localdict
    '''

class KpiItem(models.Model):
    _name = 'hr.kpiitem'
    _description = "KPIs List"
    name = fields.Char(string = 'KPI element Name')
    description = fields.Text('Purpose of this KPI elemenbt')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    struct_id = fields.Many2one('hr.appraisal.report.structure', string="Appraisal Report Structure", required=True)
    #_check_company_auto = True
    #applicableDepartments = fields.Many2Many('hr.department', string = "Applicable departments", help="Select the departments at which this KPI is applicable", domain = lambda self: self.env.user.allow)
    #domain = lambda self: self.env. 
    #exclude = fields.One2many('hr.employee', 'items_ids', string = "employees that will not be associated with this field", company_dependent=True)
    highestScore = fields.Integer(string = 'Highest Score possible')
    lowestScore = fields.Integer(string = 'Lowest Score possible')
    note = fields.Text('Note')
    category_id = fields.Many2one('hr.kpiitem.category', string = "Category of this KPI Item")
    sequence = fields.Integer(required=True, index=True, default=5,
        help='Use to arrange sequence')
    
    def _satisfy_conditions(self, localdict):
        '''
_name = 'hr.salary.rule'
    _order = 'sequence, id'
    _description = 'Salary Rule'
    #added
    name = fields.Char(required=True, translate=True)
    #not added
    code = fields.Char(required=True,
        help="The code of salary rules can be used as reference in computation of other rules. "
             "In that case, it is case sensitive.")
    #added
    struct_id = fields.Many2one('hr.payroll.structure', string="Salary Structure", required=True)
    #added but might not need
    sequence = fields.Integer(required=True, index=True, default=5,
        help='Use to arrange calculation sequence')
    #not added because it is not needed
    quantity = fields.Char(default='1.0',
        help="It is used in computation for percentage and fixed amount. "
             "E.g. a rule for Meal Voucher having fixed amount of "
             u"1€ per worked day can have its quantity defined in expression "
             "like worked_days.WORK100.number_of_days.")
    #added
    category_id = fields.Many2one('hr.salary.rule.category', string='Category', required=True)
    #not added and not needed
    active = fields.Boolean(default=True,
        help="If the active field is set to false, it will allow you to hide the salary rule without removing it.")
    #not added and not needed
    appears_on_payslip = fields.Boolean(string='Appears on Payslip', default=True,
        help="Used to display the salary rule on payslip.")
    #not added and not needed for now
    condition_select = fields.Selection([
        ('none', 'Always True'),
        ('range', 'Range'),
        ('python', 'Python Expression')
    ], string="Condition Based on", default='none', required=True)
    #there is a ref to the corrsposning field
    condition_range = fields.Char(string='Range Based on', default='contract.wage',
        help='This will be used to compute the % fields values; in general it is on basic, '
             'but you can also use categories code fields in lowercase as a variable names '
             '(hra, ma, lta, etc.) and the variable basic.')
    #not added and not needed
    condition_python = fields.Text(string='Python Condition', required=True, default="",
        help='Applied this rule for calculation if condition is true. You can specify condition like basic > 1000.')
    condition_range_min = fields.Float(string='Minimum Range', help="The minimum amount, applied for this rule.")
    condition_range_max = fields.Float(string='Maximum Range', help="The maximum amount, applied for this rule.")
    amount_select = fields.Selection([
        ('percentage', 'Percentage (%)'),
        ('fix', 'Fixed Amount'),
        ('code', 'Python Code'),
    ], string='Amount Type', index=True, required=True, default='fix', help="The computation method for the rule amount.")
    amount_fix = fields.Float(string='Fixed Amount', digits='Payroll')
    amount_percentage = fields.Float(string='Percentage (%)', digits='Payroll Rate',
        help='For example, enter 50.0 to apply a percentage of 50%')
    amount_python_compute = fields.Text(string='Python Code', '''
        #default='''
                    # Available variables:
                    #----------------------
                    # payslip: object containing the payslips
                    # employee: hr.employee object
                    # contract: hr.contract object
                    # rules: object containing the rules code (previously computed)
                    # categories: object containing the computed salary rule categories (sum of amount of all rules belonging to that category).
                    # worked_days: object containing the computed worked days.
                    # inputs: object containing the computed inputs.

                    # Note: returned value have to be set in the variable 'result'

                    #result = contract.wage * 0.10''')
    ''' 
    amount_percentage_base = fields.Char(string='Percentage based on', help='result will be affected to a variable')
    partner_id = fields.Many2one('res.partner', string='Partner',
        help="Eventual third party involved in the salary payment of the employees.")
    note = fields.Html(string='Description')

    def _raise_error(self, localdict, error_type, e):
        raise UserError(_("""%s:
- Employee: %s
- Contract: %s
- Payslip: %s
- Salary rule: %s (%s)
- Error: %s""") % (
            error_type,
            localdict['employee'].name,
            localdict['contract'].name,
            localdict['payslip'].dict.name,
            self.name,
            self.code,
            e))

    def _compute_rule(self, localdict):

        """
        :param localdict: dictionary containing the current computation environment
        :return: returns a tuple (amount, qty, rate)
        :rtype: (float, float, float)
        """
        self.ensure_one()
        if self.amount_select == 'fix':
            try:
                return self.amount_fix or 0.0, float(safe_eval(self.quantity, localdict)), 100.0
            except Exception as e:
                self._raise_error(localdict, _("Wrong quantity defined for:"), e)
        if self.amount_select == 'percentage':
            try:
                return (float(safe_eval(self.amount_percentage_base, localdict)),
                        float(safe_eval(self.quantity, localdict)),
                        self.amount_percentage or 0.0)
            except Exception as e:
                self._raise_error(localdict, _("Wrong percentage base or quantity defined for:"), e)
        else:  # python code
            try:
                safe_eval(self.amount_python_compute or 0.0, localdict, mode='exec', nocopy=True)
                return float(localdict['result']), localdict.get('result_qty', 1.0), localdict.get('result_rate', 100.0)
            except Exception as e:
                self._raise_error(localdict, _("Wrong python code defined for:"), e)

    def _satisfy_condition(self, localdict):
        self.ensure_one()
        if self.condition_select == 'none':
            return True
        if self.condition_select == 'range':
            try:
                result = safe_eval(self.condition_range, localdict)
                return self.condition_range_min <= result <= self.condition_range_max
            except Exception as e:
                self._raise_error(localdict, _("Wrong range condition defined for:"), e)
        else:  # python code
            try:
                safe_eval(self.condition_python, localdict, mode='exec', nocopy=True)
                return localdict.get('result', False)
            except Exception as e:
                self._raise_error(localdict, _("Wrong python condition defined for:"), e)
        ''' 