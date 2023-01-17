# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PolicyRegisteration(models.Model):
    _name = 'mgs_slnia.policy_registeration'
    _description = 'Policy Registeration'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(string='Reg#', copy=False)
    api_id = fields.Integer(string='API ID')
    related_insurance_id = fields.Many2one('res.partner', domain=[(
        'is_insurence_company', '=', True)], auto_join=True, index=True, required=True, string='Related Insurance Org', help='Related Insurance Organization')
    period_id = fields.Many2one(
        'mgs_slnia.period', index=True, required=True, string='Period')
    customer_id = fields.Many2one(
        'mgs_slnia.customer', index=True, required=True, string='Customer')
    description = fields.Char(string='Description')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', 'Currency', domain=[(
        'active', '=', True)], default=lambda self: self.env.company.currency_id.id)
    policy_amount = fields.Monetary(string='Policy Amount')
    claim_amount = fields.Monetary(string='Claim Amount')
    premium_amount = fields.Monetary(string='Premium Amount')
    tax_amount = fields.Monetary(string='Tax Amount')
