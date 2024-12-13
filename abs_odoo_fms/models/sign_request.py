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
from odoo import api, fields, models, _
# Inherited Class SignRequest
class SignRequest(models.Model):
    _inherit = "sign.request"

    partner_id = fields.Many2one("res.partner", string="Partner")

    def action_signed(self):
        super(SignRequest, self).action_signed()
        for request in self:
            if request.partner_id:
                request.partner_id.message_post_with_view(
                    "abs_odoo_fms.message_signature_link",
                    values={"request": request, "salesman": self.env.user.partner_id},
                    subtype_id=self.env.ref("mail.mt_note").id,
                    author_id=self.env.user.partner_id.id,
                )
                # attach a copy of the signed document to the SO for easy retrieval
                #-----------------------Start----------------#
                attachment_id =  self.env["ir.attachment"].create(
                    {
                        "name": request.reference,
                        "datas": request.completed_document,
                        "type": "binary",
                        "res_model": self.env["res.partner"]._name,
                        "res_id": request.partner_id.id,
                    })
                if attachment_id and self.partner_id.nda:
                    self.partner_id.nda_attachment_id = attachment_id.id
                    self.partner_id.nda = False
                if attachment_id and self.partner_id.non_compete:
                    self.partner_id.non_compete_attachment_id = attachment_id.id
                    self.partner_id.non_compete = False
                #----------------------------End--------------------#
