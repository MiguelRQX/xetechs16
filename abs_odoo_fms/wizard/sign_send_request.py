# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2022-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models, SUPERUSER_ID, _
# Inherited Class SignSendRequest
class SignSendRequest(models.TransientModel):
    _inherit = 'sign.send.request'

    partner_id = fields.Many2one('res.partner',string="Partner")

    @api.onchange('template_id')
    def _onchange_template_id(self):
        self.signer_id = False
        self.filename = self.template_id.display_name
        self.subject = _("Signature Request - %s") % (self.template_id.attachment_id.name or '')
        roles = self.template_id.mapped('sign_item_ids.responsible_id')
        signer_ids = [(0, 0, {
            'role_id': role.id,
            'partner_id': self.partner_id.id,
        }) for role in roles]
        if self.env.context.get('sign_directly_without_mail'):
            if len(roles) == 1:
                signer_ids[0][2]['partner_id'] = self.env.user.partner_id.id
            elif not roles:
                self.signer_id = self.env.user.partner_id.id
        self.signer_ids = [(5, 0, 0)] + signer_ids
        self.signers_count = len(roles)

    def create_request(self, send=True, without_mail=False):
        request_info = super(SignSendRequest, self).create_request(send, without_mail)
        #--------------------Start-------------#
        request_id = request_info["id"]
        if self.partner_id:
            request = self.env["sign.request"].browse(request_id)
            request.partner_id = self.partner_id
        #-----------------------end-----------#
        return request_info
