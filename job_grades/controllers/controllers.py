# -*- coding: utf-8 -*-
# from odoo import http


# class JobGrades(http.Controller):
#     @http.route('/job_grades/job_grades', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/job_grades/job_grades/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('job_grades.listing', {
#             'root': '/job_grades/job_grades',
#             'objects': http.request.env['job_grades.job_grades'].search([]),
#         })

#     @http.route('/job_grades/job_grades/objects/<model("job_grades.job_grades"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('job_grades.object', {
#             'object': obj
#         })
