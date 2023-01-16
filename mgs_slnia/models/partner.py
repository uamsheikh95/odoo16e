# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    is_insurence_company = fields.Boolean(
        string='Is Insurance Company', default=False)


class SLNIACustomer(models.Model):
    _name = 'mgs_slnia.customer'
    _description = 'Customers'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char('Name', required=True)
    mobile = fields.Char(string="Mobile", required=True)
    email = fields.Char(string="Email")
    street = fields.Char(string="Address 1")
    street2 = fields.Char(string="Address 2")
    country_id = fields.Many2one(
        'res.country', string="Country")
    state_id = fields.Many2one(
        'res.country.state', string="State")
    city = fields.Char(string="City")
    id_no = fields.Char(string="Identity No.")
    related_insurance_id = fields.Many2one('res.partner', domain=[('is_insurence_company', '=', True)], auto_join=True, index=True, required=True,
                                           string='Related Insurance Org', help='Related Insurance Organization')
    company_id = fields.Many2one(
        'res.company', auto_join=True, index=True, string='Company')
