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


class Project(models.Model):
    _inherit = "project.project"

    budget_hours = fields.Float('Presupuesto de Horas', required=False)
    consumed_hours = fields.Float('Consumo de horas', required=False, compute="_compute_consumed_hours")
    residual_hours = fields.Float('Residual de horas', required=False, compute="_compute_consumed_hours")
    progress_hours = fields.Float('Progreso', required=False, compute="_compute_consumed_hours")
    hours_ids = fields.One2many('report.project.budget.hours', 'project_id', string="Horas Consumidas")

    @api.depends('hours_ids', 'budget_hours')
    def _compute_consumed_hours(self):
        consumed_hours = 0.00
        for rec in self:
            for item in rec.hours_ids:
                consumed_hours += item.amount_hours
            rec.update({
                'consumed_hours': consumed_hours or 0.00,
                'residual_hours': (rec.budget_hours - consumed_hours) or 0.00,
                'progress_hours': ((consumed_hours / rec.budget_hours if rec.budget_hours > 0.00 else 1.00) * 100) or 0.00,

            })


# class HelpdeskTicket(models.Models):
#     _inherit = "helpdesk.ticket"
