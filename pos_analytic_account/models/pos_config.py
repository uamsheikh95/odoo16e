# -*- coding: utf-8 -*-

from odoo import models, fields


# class PosConfig(models.Model):
#     _inherit = 'pos.config'

#     account_analytic_id = fields.Many2one('account.analytic.account',
#                                           string='Analytic Account',
#                                           )

#     analytic_distribution = fields.Json()


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # ,  related='pos_config_id.account_analytic_id'
    pos_account_analytic_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account', config_parameter='pos_analytic_account.pos_account_analytic_id')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('pos_analytic_account.pos_account_analytic_id',
                                                  self.pos_account_analytic_id.id)
