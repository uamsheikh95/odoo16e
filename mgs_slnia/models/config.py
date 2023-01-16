# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PolicyType(models.Model):
    _name = 'mgs_slnia.policy_type'
    _description = 'MGS SLNIA Policy Type'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(string='Policy Type', required=True)


class Period(models.Model):
    _name = 'mgs_slnia.period'
    _description = 'MGS SLNIA Period'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(string='Period', required=True)
