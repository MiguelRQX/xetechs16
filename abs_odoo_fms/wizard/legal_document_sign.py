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
from odoo import api, fields, models

class LegalDocumentSign(models.TransientModel):
    _name = "legal.document.sign.wizard"
    _description = "Sign Documents from a Legal"

    template_id = fields.Many2one("sign.template", "Document Template", required=True, ondelete="cascade")
    partner_id = fields.Many2one("res.partner", "Partner", required=True, ondelete="cascade",default=lambda p: p.env.context.get("active_id", None))
    state = fields.Selection([('non_compete','Non compete'),('nda','NDA')],store=True,string='State')

    def next_sign_document_step(self):
        # Set the reference of NDA and Non compete.
        if self.partner_id and self.state == 'nda':
            self.partner_id.nda = self.state
        if self.partner_id and self.state == 'non_compete':
            self.partner_id.non_compete = self.state

        pending_sign_request = self.partner_id.sign_request_ids.filtered(lambda request: request.template_id == self.template_id and request.state == "sent")
        if pending_sign_request:
            return pending_sign_request.go_to_document()
        else:
            action = self.env['ir.actions.act_window']._for_xml_id('sign.action_sign_send_request')
            action["context"] = {
                "active_id": self.template_id.id,
                "default_partner_id": self.partner_id.id,
            }
            return action
