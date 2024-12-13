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

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    contrated_hours = fields.Float(string="Horas contradas", related="partner_parent_id.contrated_hours")
    contrated_hours_real = fields.Float("Horas consumidas", related="partner_parent_id.contrated_hours_real")
    contrated_hours_balance = fields.Float("Saldo", related="partner_parent_id.contrated_hours_balance")
    progress = fields.Float("Progreso", related="partner_parent_id.progress")
    subscription_status = fields.Selection([('active', 'Vigente'), ('inactive', 'Vencida'), ('done', 'Consumida')], string="Estatus", related="partner_parent_id.subscription_status")


    #@api.model_create_multi
    #def create(self, vals_list):
    #    res = super(HelpdeskTicket, self).create(vals_list)
    #    for rec in res:
    #        #vals.update(self._heldeskticket_preprocess(vals))
    #        if rec.contrated_hours_balance < 100.00:
    #            rec.write({
    #                'stage_id': self.env.ref('helpdesk_tracker_hours.stage_suspended').id 
    #            })
    #    return res
