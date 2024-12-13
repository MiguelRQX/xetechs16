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
from . import models
from odoo.api import Environment, SUPERUSER_ID


#Post Update PosOrderLine - Config_id
def post_init_hook(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    lines_ids = env['account.analytic.line'].search([('helpdesk_ticket_id', '!=', False)])
    for line in lines_ids:
        if line.helpdesk_ticket_id and line.helpdesk_ticket_id.partner_id:
            if line.helpdesk_ticket_id.partner_id.parent_id:
                line.write({
                    'partner_id': line.helpdesk_ticket_id.partner_id.parent_id.id or False,
                })
            else:
                line.write({
                    'partner_id': line.helpdesk_ticket_id.partner_id.id or False,
                })