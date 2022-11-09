# -*- coding: utf-8 -*-
# from odoo import http


# class AccountNotice(http.Controller):
#     @http.route('/account_notice/account_notice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_notice/account_notice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_notice.listing', {
#             'root': '/account_notice/account_notice',
#             'objects': http.request.env['account_notice.account_notice'].search([]),
#         })

#     @http.route('/account_notice/account_notice/objects/<model("account_notice.account_notice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_notice.object', {
#             'object': obj
#         })
