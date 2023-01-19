# -*- coding: utf-8 -*-

from unittest import result
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_balance = fields.Monetary(string='Partner Balance', readonly=True)

    @api.onchange('partner_id')
    def onchange_partner_balance(self):
        for r in self:
            r.partner_balance = r.partner_id.credit if r.move_type in [
                'out_invoice', 'out_refund', 'out_receipt'] else r.partner_id.debit

    @api.model
    def get_invoice_previous_balance(self):
        for r in self:
            partner_id = r.partner_id.id
            account_type = """('Receivable')""" if r.move_type in [
                'out_invoice', 'out_refund', 'out_receipt'] else """('Payable')"""
            sum_type = 'aml.debit-aml.credit' if r.move_type in [
                'out_invoice', 'out_refund', 'out_receipt'] else 'aml.credit-aml.debit'
            date = r.invoice_date
            company_id = r.company_id.id
            move_id = r.id

        params = [sum_type, account_type,
                  partner_id, company_id, move_id, date]
        acc_rec_query = """
        select sum(%s) as total
        from account_move_line as aml
        left join account_move as am on aml.move_id=am.id
        left join account_account as aa on aml.account_id=aa.id
        left join account_account_type as aat on aa.user_type_id=aat.id
        left join res_partner as rp on aml.partner_id=rp.id
        where aat.name=%s and aml.parent_state='posted'
        and aml.partner_id=%s and aml.company_id=%s and aml.move_id != %s
        and aml.date <= %s
        """

        self.env.cr.execute(acc_rec_query, tuple(params))
        contemp = self.env.cr.fetchone()
        result = 0
        if contemp is not None:
            result = contemp[0] or 0.0
        return result


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    account_balance = fields.Char(string='Acc Balance', readonly=True)
    tranfer_account_balance = fields.Char(
        string='Transfer Acc Balance', default='0', readonly=True)
    partner_balance = fields.Monetary(string='Partner Balance', readonly=True)

    @api.onchange('partner_id')
    def onchange_partner_balance(self):
        for r in self:
            r.partner_balance = r.partner_id.credit if r.payment_type == 'inbound' else r.partner_id.debit

    @api.onchange('journal_id')
    def _onchange_journal_balance(self):
        journal_obj = self.env['account.journal']
        result = 0
        for r in self:
            journal_domain = [('id', '=', r.journal_id.id)]
            for journal in journal_obj.search(journal_domain):
                result = journal.get_journal_dashboard_datas()[
                    'account_balance']

            r.account_balance = result

    @api.onchange('destination_journal_id')
    def _onchange_destination_journal_balance(self):
        journal_obj = self.env['account.journal']
        result = 0
        for r in self:
            journal_domain = [('id', '=', r.destination_journal_id.id)]
            for journal in journal_obj.search(journal_domain):
                result = journal.get_journal_dashboard_datas()[
                    'account_balance']

            r.tranfer_account_balance = result


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    account_balance = fields.Char(string='Acc Balance', readonly=True)

    @api.onchange('journal_id')
    def _onchange_journal_balance(self):
        journal_obj = self.env['account.journal']
        result = 0
        for r in self:
            journal_domain = [('id', '=', r.journal_id.id)]
            for journal in journal_obj.search(journal_domain):
                result = journal.get_journal_dashboard_datas()[
                    'account_balance']

            r.account_balance = result


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_balance = fields.Monetary(
        string='Vendor Balance', related="partner_id.debit", store=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_balance = fields.Monetary(
        string='Customer Balance', related="partner_id.credit", store=True)
