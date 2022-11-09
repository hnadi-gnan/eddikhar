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
