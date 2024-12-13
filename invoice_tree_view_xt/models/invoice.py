# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'account.move'

    tc = fields.Float(string="TC", digits=(12,6), compute='compute_exchange_rate', store=True)

    @api.depends('amount_total_signed','amount_total')
    def compute_exchange_rate(self):
        for record in self:
            if not record.amount_total_signed or not record.amount_total:
                record.update({'tc': 1.00})
            else:
                record.update({'tc': round((record.amount_total_signed / record.amount_total),6)})

