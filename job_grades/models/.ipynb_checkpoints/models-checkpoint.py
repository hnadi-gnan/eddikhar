# -*- coding: utf-8 -*-

from odoo import models, fields, api


class job_grades(models.Model):
    _name = 'job_grades.job_grades'
    _description = 'job_grades.job_grades'
    _rec_name="grades"
    
    
    def _get_default_currency_id(self):
        return self.env.company.currency_id.id
    
    
    grades = fields.Integer(string = 'Grades')
    currency_id = fields.Many2one("res.currency", string="Valuta", required=True, default = _get_default_currency_id)
    max_rate = fields.Monetary(currency_field="currency_id")
    min_rate = fields.Monetary(currency_field="currency_id")
    bonus_id = fields.One2many ('bonus', 'job_grades_id', string = 'Bonus')
    

class bonus(models.Model):
    _name = 'bonus'
    _inherit = ['mail.thread','job_grades.job_grades']
    _description = 'bonus.job_grades'
    _rec_name = "bonus"
    
    
    @api.depends('min_rate', 'n_wage')
    def _compute_value(self):
        for bonus in self:
            bonus.value = bonus.n_wage - bonus.job_grades_id.min_rate 
            

               
    job_grades_id = fields.Many2one('job_grades.job_grades')
    min_rate = fields.Monetary(related = 'job_grades_id.min_rate')
    currency_id = fields.Many2one("res.currency", string="Valuta", related = "job_grades_id.currency_id",  required=True)
    bonus = fields.Integer(string = 'Bonus')
    n_wage = fields.Monetary(string = 'Wage',currency_field="currency_id")
    value = fields.Monetary(string = 'Bonus value', compute = '_compute_value')
    
    
    

    
class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"
    job_grades_id = fields.Many2one('job_grades.job_grades')

    
class HRcontract(models.Model):
    _inherit = "hr.contract"
    job_grades_id = fields.Many2one('job_grades.job_grades')
    bonus = fields.Many2one('bonus', domain = "[('job_grades_id', '=', job_grades_id)]")
    bonus_value = fields.Monetary('value')
        
    
    @api.depends('bonus', 'job_grades_id')
    def _wage_value(self):
        for contract in self:
            sel_bonus = self.env['bonus'].search([('job_grades_id', '=', contract.job_grades_id.id ),('id','=', contract.bonus.id)])
            contract.wage = sel_bonus.n_wage
            contract.bonus_value = sel_bonus.value
            
        
            
            
            
    
    #@api.depends('bonus', 'job_grades_id')
    #def _bonus_value(self):
        #for contract in self:
            #sel_bonus = self.env['bonus'].search([('job_grades_id', '=', contract.job_grades_id.id ),('id','=', contract.bonus)])
            #contract.bonus_value = sel_bonus.value
            
            
            
    wage = fields.Monetary( compute = '_wage_value')    
        

# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class job_grades(models.Model):
#     _name = 'job_grades.job_grades'
#     _description = 'job_grades.job_grades'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
