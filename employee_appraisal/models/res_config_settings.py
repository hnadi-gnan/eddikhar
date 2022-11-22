from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import UserError

#how many appraisals per year,
#who is the responsible,
#
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    allow_yearly = fields.Boolean("Allow Yearly Appraisal", help = "Check this if you would like to allow the possibiliy of yearly appraisals for employees in all departments")
    #the idea is to create many2many called committee field in the appraisal run that will be filled by the HR reponsible in the organization
    appraisal_committee_per_run = fields.Boolean("Allow Committe per run?",help = "Are the appraisal runs made by committees that change every time?")
    appraisal_run_duraion = fields.Integer(string="Allowed duration per run", help="Please enter the allowed duration you would like a run to have i.e. 1 Months, 2 Months...etc", default=6)
    appraisal_line_duration = fields.Integer(string="duration on appraisal report line", default=6, help="Months")