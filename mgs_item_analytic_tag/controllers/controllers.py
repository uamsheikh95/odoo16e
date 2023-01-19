# -*- coding: utf-8 -*-
# from odoo import http


# class MgsItemAnalyticTag(http.Controller):
#     @http.route('/mgs_item_analytic_tag/mgs_item_analytic_tag/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mgs_item_analytic_tag/mgs_item_analytic_tag/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mgs_item_analytic_tag.listing', {
#             'root': '/mgs_item_analytic_tag/mgs_item_analytic_tag',
#             'objects': http.request.env['mgs_item_analytic_tag.mgs_item_analytic_tag'].search([]),
#         })

#     @http.route('/mgs_item_analytic_tag/mgs_item_analytic_tag/objects/<model("mgs_item_analytic_tag.mgs_item_analytic_tag"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mgs_item_analytic_tag.object', {
#             'object': obj
#         })
