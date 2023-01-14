# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PosOrder(models.Model):
    _inherit = 'pos.order'

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        copy=False, string='Analytic Account')

    analytic_distribution = fields.Json()

    def _prepare_invoice_line(self, order_line):
        res = super(PosOrder, self)._prepare_invoice_line(order_line)
        # res['analytic_account_id'] = order_line.order_id.account_analytic_id.id \
        #                              or False
        # res['analytic_distribution'] = order_line.order_id.account_analytic_id.id \
        #     or False
        res['analytic_distribution'] = order_line.order_id.analytic_distribution
        return res

    def write(self, vals):
        for order in self:
            if not order.account_analytic_id:
                # vals['account_analytic_id'] = \
                #     order.config_id.account_analytic_id.id or False
                vals['analytic_distribution'] = \
                    order.config_id.analytic_distribution
        return super(PosOrder, self).write(vals)
