# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        if not self.location_id.id in self.env.user.stock_location_ids.ids:
            raise UserError("Sorry, you cannot proceed with this transfer.")
        return super(StockPicking, self).button_validate()

class stock_move(models.Model):
    _inherit = 'stock.move'

    @api.constrains('state', 'location_id', 'location_dest_id')
    def check_user_location_rights(self):
        pass
