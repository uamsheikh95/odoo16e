# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    analytic_tag_ids = fields.Many2many('account.analytic.tag',string='Analytic Tags')
    analytic_tag_id = fields.Many2one('account.analytic.tag', string='Analytic Tag', compute='_compute_analytic_tag_id', store=True)

    @api.depends('analytic_tag_ids')
    def _compute_analytic_tag_id(self):
        for r in self:
            r.analytic_tag_id = False
            if len(r.analytic_tag_ids) > 0:
                r.analytic_tag_id = r.analytic_tag_ids[0]

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.analytic_tag_ids = self.product_id.product_tmpl_id.analytic_tag_ids.ids
