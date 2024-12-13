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

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = "res.partner"

    contrated_hours = fields.Float(string="Hours Contrated")
    category = fields.Selection([('bronce', 'Bronce'), ('silver', 'Silver'), ('gold', 'Gold')], string="Category for Helpdesk")
    sale_subscription_id = fields.Many2one('sale.subscription', string='Subscription')
    helpdesk_hour_ids = fields.One2many('report.helpdesk.budget.hours', 'customer_id', 'Helpdesk Consumos')
    contrated_hours_real = fields.Float("Hours Contrated Real", compute="_compute_contrated_hours", store=True)

    @api.depends('contrated_hours', 'parent_id')
    def _compute_contrated_hours(self):
        hours = 0.00
        for rec in self:
            if rec.parent_id:
                hours = rec.parent_id.contrated_hours
            else:
                hours = rec.contrated_hours
            rec.update({
                'contrated_hours_real': hours or 0.00,
            })
