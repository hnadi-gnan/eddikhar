# -*- coding: utf-8 -*-
# from odoo import http


# class ApprovalsPurchaseRequisition(http.Controller):
#     @http.route('/approvals_purchase_requisition/approvals_purchase_requisition', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/approvals_purchase_requisition/approvals_purchase_requisition/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('approvals_purchase_requisition.listing', {
#             'root': '/approvals_purchase_requisition/approvals_purchase_requisition',
#             'objects': http.request.env['approvals_purchase_requisition.approvals_purchase_requisition'].search([]),
#         })

#     @http.route('/approvals_purchase_requisition/approvals_purchase_requisition/objects/<model("approvals_purchase_requisition.approvals_purchase_requisition"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('approvals_purchase_requisition.object', {
#             'object': obj
#         })
