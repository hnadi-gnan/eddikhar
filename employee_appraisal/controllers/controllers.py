# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeAppraisal(http.Controller):
#     @http.route('/employee_appraisal/employee_appraisal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_appraisal/employee_appraisal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_appraisal.listing', {
#             'root': '/employee_appraisal/employee_appraisal',
#             'objects': http.request.env['employee_appraisal.employee_appraisal'].search([]),
#         })

#     @http.route('/employee_appraisal/employee_appraisal/objects/<model("employee_appraisal.employee_appraisal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_appraisal.object', {
#             'object': obj
#         })
