# -*- coding: utf-8 -*-
# from odoo import http


# class AccountAssetMaintenance(http.Controller):
#     @http.route('/account_asset_maintenance/account_asset_maintenance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_asset_maintenance/account_asset_maintenance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_asset_maintenance.listing', {
#             'root': '/account_asset_maintenance/account_asset_maintenance',
#             'objects': http.request.env['account_asset_maintenance.account_asset_maintenance'].search([]),
#         })

#     @http.route('/account_asset_maintenance/account_asset_maintenance/objects/<model("account_asset_maintenance.account_asset_maintenance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_asset_maintenance.object', {
#             'object': obj
#         })
