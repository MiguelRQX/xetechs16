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


class SupportContractType(models.Model):
    _name = "support.contract.type"
    _inherit = ['portal.mixin', 'mail.thread.cc', 'utm.mixin', 'rating.mixin', 'mail.activity.mixin']
    _description = "Plan de soporte"

    name = fields.Char('Plan de soporte', required=True)
    active = fields.Boolean('Activo', required=False, default=True)
    hours = fields.Float('Horas de Soporte', required=True)
    consumed_hours_warning = fields.Float('Aviso de consumo', required=True)
    notes = fields.Text('Notas', required=False)
