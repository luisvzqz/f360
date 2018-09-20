# -*- coding: utf-8 -*-
from odoo import http

# class 360fin(http.Controller):
#     @http.route('/360fin/360fin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/360fin/360fin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('360fin.listing', {
#             'root': '/360fin/360fin',
#             'objects': http.request.env['360fin.360fin'].search([]),
#         })

#     @http.route('/360fin/360fin/objects/<model("360fin.360fin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('360fin.object', {
#             'object': obj
#         })