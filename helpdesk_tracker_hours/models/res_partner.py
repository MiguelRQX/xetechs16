# -*- encoding: UTF-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2015-Today Xetechs, S.A.
# (<http://www.xetechs.com>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
import logging

from odoo import _, api, fields, models
import time


_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    #contrated_hours = fields.Float(string="Hours Contrated")
    category = fields.Selection([('bronce', 'Bronce'), ('silver', 'Silver'), ('gold', 'Gold')], string="Category for Helpdesk")
    sale_subscription_id = fields.Many2one('sale.subscription', string='Suscripción')
    helpdesk_hour_ids = fields.One2many('report.helpdesk.budget.hours', 'customer_id', 'Helpdesk Consumos')
    #New fields
    support_contract_type_id = fields.Many2one('support.contract.type', 'Plan de soporte', required=False, copy=True)
    apply_support = fields.Boolean('Cuenta con plan de soporte', required=False, default=False)
    contrated_hours = fields.Float(string="Horas contradas", related="support_contract_type_id.hours", store=True)
    contrated_hours_real = fields.Float("Horas consumidas", compute="_compute_hours")
    contrated_hours_balance = fields.Float("Saldo", compute="_compute_hours")
    progress = fields.Float("Progreso", compute="_compute_hours")
    date_due = fields.Date('Vencimiento', required=False, copy=False)
    subscription_template_id = fields.Many2one('sale.subscription.template', 'Tipo suscripción', related="sale_subscription_id.template_id")
    subscription_status = fields.Selection([('active', 'Vigente'), ('inactive', 'Vencida'), ('done', 'Consumida')], string="Estatus", compute="_compute_subscription_status")

    @api.depends('date_due')
    def _compute_subscription_status(self):
        for rec in self:
            status = 'active'
            if rec.date_due:
                #    continue
                if rec.date_due >= fields.Date.today():
                    status = 'active'
                if rec.date_due < fields.Date.today():
                    status = 'inactive'
            if rec.progress > 100.00:
                status = 'done'
            rec.update({
                'subscription_status': status,
            })

    @api.depends('support_contract_type_id', 'contrated_hours')
    def _compute_hours(self):
        for rec in self:
            contrated_hours_real = 0.00
            ticket_line_ids = self.env['account.analytic.line'].search([
                ('helpdesk_ticket_id', '!=', False),
                ('date', '>=', time.strftime('%Y-%m-01')),
                ('date', '<=', fields.Date.today()),
                ('partner_id', '=', rec.id),
            ])
            contrated_hours_real = sum(x.unit_amount for x in ticket_line_ids)
            balance = (rec.contrated_hours - contrated_hours_real)
            rec.update({
                'contrated_hours_real': contrated_hours_real,
                'contrated_hours_balance': balance,
                'progress': (contrated_hours_real / (rec.contrated_hours if rec.contrated_hours > 0.00 else 1.00)) * 100
            })

    #@api.onchange('support_contract_type_id')
    #def onchange_subscription(self):
    #    if self.support_contract_type_id:
    #        subscription_ids = self.env['sale.subscription'].
