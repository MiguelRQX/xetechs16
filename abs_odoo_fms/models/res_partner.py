# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2022-today Ascetic Business Solution <www.asceticbs.com>
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
# Inherited Class Partner
class Partner(models.Model):
    _inherit = "res.partner"

    cost = fields.Float("Cost/Hour")
    fms_rating = fields.Selection(selection=[
            ('0', 'Low'),
            ('1', 'Medium'),
            ('2', 'High'),
            ('3', 'Highest'),
        ], string="FMS Rating",compute="_compute_fms_rating")
        
    nda_attachment_id = fields.Many2one("ir.attachment", string="NDA")
    non_compete_attachment_id = fields.Many2one("ir.attachment", string="Non Compete")
    nda_attachment_expiry_date = fields.Date("NDA Expiry Date")
    non_compete_attachment_expiry_date = fields.Date("Non Compete Expiry Date")
    
    payment_option = fields.Selection(selection=[
            ('paypal', 'PayPal'),
            ('wire_transfer', 'Wire Transfer'),
        ], string="Preferred Payment Option")
    paypal_id = fields.Char("PayPal ID")
    bank_name = fields.Char("Bank Name")
    bank_country_id = fields.Many2one('res.country', string='Country')
    bank_street = fields.Char("Bank Street")
    bank_street2 = fields.Char("Bank Street2")
    bank_zip = fields.Char(change_default=True)
    bank_city = fields.Char("Bank City")
    bank_state_id = fields.Many2one("res.country.state", string='Bank State', domain="[('country_id', '=?', bank_country_id)]")
    bank_country_id = fields.Many2one('res.country', string='Bank Country')
    bank_phone_number = fields.Char("Bank Phone Number")
    bank_account_name = fields.Char("Account Name")
    bank_account_number = fields.Char("Account Number")
    swift_code = fields.Char("SWIFT CODE")
    iban_code = fields.Char("IBAN CODE")
    document_warning = fields.Text("Document Warning", compute="_compute_document_warning", store="1")

    fms_performance_ids = fields.One2many("fms.performance", "partner_id", "FMS Performance")
    sign_request_ids = fields.One2many(
        "sign.request", "partner_id", string="Signature Requests")
    nda = fields.Char("NDA Reference")
    non_compete = fields.Char("Non Compete Reference")

    @api.depends('nda_attachment_expiry_date', 'non_compete_attachment_expiry_date')
    def _compute_document_warning(self):
        for record in self:
            record.document_warning = ''
            if record.nda_attachment_expiry_date and record.nda_attachment_expiry_date < fields.Date.today():
                record.document_warning += "NDA Document is expired.\n"
            if record.non_compete_attachment_expiry_date and record.non_compete_attachment_expiry_date < fields.Date.today():
                record.document_warning += "Non Compete Document is expired."

    @api.depends('fms_rating')
    def _compute_fms_rating(self):
        for record in self:
            record.fms_rating = False
            payment_id = self.env['payment.management'].search([('fms_id','=',record.id)])
            if payment_id:
                total = 0.0
                customer_count_list = []
                for line in payment_id:
                    total += float(line.fms_rating)
                customer_count_list += payment_id.ids
                average = (total) / (len(customer_count_list))
                convert_int_average = int(average)
                convert_str_average = str(convert_int_average)
                if average > 1.0 and average <= 2.0:
                    record.fms_rating = '2'
                elif average > 2.0:
                    record.fms_rating = '3'
                else:
                    record.fms_rating = convert_str_average

class FMSPerformance(models.Model):
    _name = "fms.performance"
    description = "FMS Performance"

    partner_id = fields.Many2one('res.partner', 'Customer')
    date = fields.Date('Date')
    review = fields.Char('Review')
