# -*- coding: utf-8 -*-

from odoo import models, fields, api
from calendar import monthrange
from datetime import datetime, date
from odoo.exceptions import UserError

class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    fuel_service_id= fields.Many2one('fleet.service.type',string='Feul Service',config_parameter='mgs_fleet_addons.fuel_service_id')

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('mgs_fleet_addons.fuel_service_id',self.fuel_service_id.id)

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    limit_fuel = fields.Float('Fuel Limit')
    fuel_type = fields.Selection([('diesel', 'Diesel'), ('petrol', 'Petrol')])
    consumed_fuel = fields.Float('Consumed Fuel', compute="_compute_consumed_fuel")

    def _compute_consumed_fuel(self):
        consumed_fuel = 0
        for r in self:
            r.consumed_fuel = False
            beginning_date = date.today().replace(day=1)
            last_day = monthrange(beginning_date.year, beginning_date.month)
            ending_date = date.today().replace(day=last_day[1])
            # service_type_id=self.env['fleet.service.type'].search([('id', '=', int(self.env['ir.config_parameter'].sudo().get_param('mgs_fleet_addons.fuel_service_id')))]).id
            rec = self.env['fleet.vehicle.log.services'].search([('vehicle_id', '=', r.id),('service_type_id','=',int(self.env['ir.config_parameter'].sudo().get_param('mgs_fleet_addons.fuel_service_id'))),('date', '>=', beginning_date), ('date', '<=', ending_date)])
            for line in rec:
                consumed_fuel += line.liter
        r.consumed_fuel = consumed_fuel

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    seq = fields.Char(default="/")
    consumed_fuel = fields.Float('Consumed Fuel', compute="_compute_consumed_fuel", store=True)
    limit_fuel = fields.Float('Fuel Limit', compute="_compute_consumed_fuel", store=True)
    fuel_type = fields.Selection([('diesel', 'Diesel'), ('petrol', 'Petrol')])
    item_ids = fields.One2many('mgs_fleet_addons.services_items', 'fleet_service_id')
    liter= fields.Float("liters")
    is_feul = fields.Boolean(string='Is feul',store=True,default=False)
    per_liter = fields.Monetary('Cost per liter')
    amount = fields.Monetary('Cost',compute="_compute_fuel_cost_amount",store=True,readonly=False)
    

    # @api.onchange('consumed_fuel')
    # def _onchange_consumed_fuel(self):
    #     for r in self:
    #         if r.consumed_fuel and r.consumed_fuel > r.limit_fuel:
    #             raise ValidationError('''Limit has been reached the limit.
    #                                     (FADLAN LIMITKII BAAD DHAAFTAY)''')

    @api.constrains('consumed_fuel')
    def check_if_consumed_reached(self):
        if self.consumed_fuel > self.limit_fuel:
            raise UserError('''Limit has been reached the limit.
                                    (FADLAN LIMITKII BAAD DHAAFTAY)''')


    # @api.depends('field')
    # @api.model
    def write(self, vals):
        for r in self:
            if r.is_feul == True and r.odometer== 0.00:
                raise UserError("Please Enter The Odometer")
        result = super(FleetVehicleLogServices, self).write(vals)
        return result


    @api.model
    def create(self, vals):
        # if vals['consumed_fuel'] <= vals['limit_fuel']:
        if vals['is_feul'] == True and vals['odometer'] == 0.0:
            raise UserError("Please Enter The Odometer")
        vals['seq'] = self.env['ir.sequence'].next_by_code('fleet.vehicle.log.services')
        result = super(FleetVehicleLogServices, self).create(vals)
        return result

    @api.onchange('service_type_id')
    def _omchange_service_type_id(self):
        fuel_service_id=int(self.env['ir.config_parameter'].sudo().get_param('mgs_fleet_addons.fuel_service_id'))
        # print(fuel_service_id)
        self.is_feul=True if self.service_type_id.id==fuel_service_id else False

    @api.depends('liter','per_liter')
    def _compute_fuel_cost_amount(self):
        for r in self:
            r.amount = r.liter * r.per_liter
    @api.depends('vehicle_id')
    def _compute_consumed_fuel(self):
        consumed_fuel = 0
        for r in self:
            r.limit_fuel = r.vehicle_id.limit_fuel
            r.consumed_fuel = False
            beginning_date = date.today().replace(day=1)
            last_day = monthrange(beginning_date.year, beginning_date.month)
            ending_date = date.today().replace(day=last_day[1])
            # service_type_id=self.env['fleet.service.type'].search([('id', '=', int(self.env['ir.config_parameter'].sudo().get_param('mgs_fleet_addons.fuel_service_id')))]).id
            rec = self.env['fleet.vehicle.log.services'].search([('vehicle_id', '=', r.vehicle_id.id),('service_type_id','=',int(self.env['ir.config_parameter'].sudo().get_param('mgs_fleet_addons.fuel_service_id'))),('date', '>=', beginning_date), ('date', '<=', ending_date)])
            for line in rec:
                consumed_fuel += line.liter
            r.consumed_fuel = consumed_fuel

class FleetServicesItems(models.Model):
    _name = 'mgs_fleet_addons.services_items'

    name = fields.Char('Item')
    qty = fields.Float('Qty')
    fleet_service_id = fields.Many2one('fleet.vehicle.log.services')


class FleetStatement(models.TransientModel):
    _name = 'mgs_fleet_addons.vehicle_statement_wiz'
    _description = 'Vehicle Statement Wizard'

    date_from = fields.Date('From  Date', default=date.today().replace(day=1))
    date_to = fields.Date('To  Date', default=date.today())
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")

    # @api.multi
    def check_report(self):
        """Call when button 'Get Rep=t' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'vehicle_id': self.vehicle_id.id,
                'vehicle_name': self.vehicle_id.name,
                'vehicle_limit': self.vehicle_id.limit_fuel,
                'vehicle_plate_no': self.vehicle_id.license_plate
            },
        }

        return self.env.ref('mgs_fleet_addons.action_report_vehicle_statement').report_action(self, data=data)

class FleetStatementReport(models.AbstractModel):
    _name = 'report.mgs_fleet_addons.vehicle_statement_wiz_report'
    _description = 'Vehicle Statement Report'

    def _lines(self, date_from, date_to, vehicle_id):
        domain = [('vehicle_id', '=', vehicle_id),('service_type_id','=',int(self.env['ir.config_parameter'].sudo().get_param('mgs_fleet_addons.fuel_service_id')))]

        if date_from:
         domain.append(('date', '>=', date_from))

        if date_to:
            domain.append(('date', '<=', date_to))

        rec = self.env['fleet.vehicle.log.services'].search(domain)
        return rec

        # full_move = []
        #
        # if date_from:
        #     params.append(date_from)
        #
        # if date_to:
        #     params.append(date_to)
        #
        # query = """
        #     select fvlf.seq, fvlf.liter, fvlf.consumed_fuel from fleet_vehicle_log_fuel as fvlf
        #     where id is not null
        # """
        #
        # if date_from:
        #     query+=""" and fvlf.date >= %s::date"""
        #
        # if date_to:
        #     query+=""" and fvlf.date <= %s::date"""
        #
        # if vehicle_id:
        #     query+=""" and fvlf.vehicle_id = """ + str(vehicle_id)
        #
        # query += " order by 1"
        #
        # self.env.cr.execute(query, tuple(params))
        # res = self.env.cr.dictfetchall()
        #
        # return res

    def _sum_consumed_fuel(self, date_from, vehicle_id):
        tot_liter = 0
        date_obj = datetime.strptime(date_from, '%Y-%m-%d')
        if date_obj.day == 1:
            tot_liter = 0
            return tot_liter

        f_date = str(date_obj.year) + '-' + str(date_obj.month) + '-1'
        t_date = date_obj
        params = [f_date, t_date, vehicle_id]

        # query = """
        # select sum(liter)
        # from fleet_vehicle_log_fuel as fuel
        # where fuel.date between %s and %s
        # and fuel.vehicle_id = %s
        # """
        domain = [('service_type_id','=',int(self.env['ir.config_parameter'].sudo().get_param('mgs_fleet_addons.fuel_service_id'))),('date', '>=', f_date), ('date', '<=', t_date), ('vehicle_id', '=', vehicle_id)]
        result = 0
        for fo in self.env['fleet.vehicle.log.services'].search(domain):
            result += fo.liter
        return result

    @api.model
    def _get_report_values(self, docids, data=None):

        # self.model = self.env.context.get('active_model')
        docs = self.env.context.get('active_id')

        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        vehicle_id = data['form']['vehicle_id']
        vehicle_name = data['form']['vehicle_name']
        vehicle_limit = data['form']['vehicle_limit']
        vehicle_plate_no = data['form']['vehicle_plate_no']

        return {
            'doc_ids': self.ids,
            'docs': docs,
            'date_from': date_from,
            'date_to': date_to,
            'vehicle_id': vehicle_id,
            'vehicle_name': vehicle_name,
            'vehicle_limit': vehicle_limit,
            'vehicle_plate_no': vehicle_plate_no,
            'lines': self._lines,
            'sum_consumed_fuel': self._sum_consumed_fuel
        }
