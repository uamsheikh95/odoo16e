# -*- coding: utf-8 -*-
# from odoo import http


# class MgsSlnia(http.Controller):
#     @http.route('/mgs_slnia/mgs_slnia', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mgs_slnia/mgs_slnia/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mgs_slnia.listing', {
#             'root': '/mgs_slnia/mgs_slnia',
#             'objects': http.request.env['mgs_slnia.mgs_slnia'].search([]),
#         })

#     @http.route('/mgs_slnia/mgs_slnia/objects/<model("mgs_slnia.mgs_slnia"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mgs_slnia.object', {
#             'object': obj
#         })
