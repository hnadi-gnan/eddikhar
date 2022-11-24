# -*- coding: utf-8 -*-
# from odoo import http


# class ExchangeOrders(http.Controller):
#     @http.route('/exchange_orders/exchange_orders', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exchange_orders/exchange_orders/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('exchange_orders.listing', {
#             'root': '/exchange_orders/exchange_orders',
#             'objects': http.request.env['exchange_orders.exchange_orders'].search([]),
#         })

#     @http.route('/exchange_orders/exchange_orders/objects/<model("exchange_orders.exchange_orders"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exchange_orders.object', {
#             'object': obj
#         })
