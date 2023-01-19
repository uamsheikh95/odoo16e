# -*- coding: utf-8 -*-
from odoo import http

# class FleetAddons(http.Controller):
#     @http.route('/mgs_fleet_addons/mgs_fleet_addons/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mgs_fleet_addons/mgs_fleet_addons/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mgs_fleet_addons.listing', {
#             'root': '/mgs_fleet_addons/mgs_fleet_addons',
#             'objects': http.request.env['mgs_fleet_addons.mgs_fleet_addons'].search([]),
#         })

#     @http.route('/mgs_fleet_addons/mgs_fleet_addons/objects/<model("mgs_fleet_addons.mgs_fleet_addons"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mgs_fleet_addons.object', {
#             'object': obj
#         })
