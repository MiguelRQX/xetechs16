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
from lxml import etree
import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    partner_parent_id = fields.Many2one('res.partner', 'Empresa padre', related="partner_id.parent_id", store=True)

    @api.onchange('stage_id')
    def onchange_stage(self):
        if self.stage_id:
            if self.stage_id.is_close:
                self.close_date = fields.Datetime.now()



class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model_create_multi
    def create(self, vals_list):
        #res = super(AccountAnalyticLine, self).create(vals)
        #if (vals.get('project_id') or vals.get('task_id')) and not vals.get('partner_id'):
        for vals in vals_list:
            vals.update(self._heldeskticket_preprocess(vals))
        return super(AccountAnalyticLine, self).create(vals_list)
    
    def _heldeskticket_preprocess(self, vals):
        partner_id = False
        if vals.get('helpdesk_ticket_id'):
            ticket_id = self.env['helpdesk.ticket'].browse(vals['helpdesk_ticket_id'])
            if ticket_id and ticket_id.partner_id:
                if ticket_id.partner_id.parent_id:
                    vals['partner_id'] = ticket_id.partner_id.parent_id.id
                else:
                    vals['partner_id'] = ticket_id.partner_id.id
        #vals['partner_id'] = partner_id
        return vals

    @api.model
    def _action_update_partner(self):
        lines_ids = self.env['account.analytic.line'].search([('helpdesk_ticket_id', '!=', False)])
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

