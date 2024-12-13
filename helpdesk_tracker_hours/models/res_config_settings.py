# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import requests
import json
from odoo.exceptions import UserError
import base64
import time

class ResCompany(models.Model):
    _inherit = "res.company"

    schedule_type = fields.Selection([('weekly', 'Semanal'), ('monthly', 'Mensual')], 'Enviar', default="weekly")
    user_ids = fields.Many2many('res.users', 'rel_company_users', 'company_id', 'user_id', string="Enviar a")
    user_to_id = fields.Many2one('res.users', 'Enviar a')
    user_cc_id = fields.Many2one('res.users', 'Enviar CC a')

    @api.model
    def _send_email(self):
        company_ids = self.env['res.company'].search([])
        for cmp in company_ids:
            cmp.send_email()
        return True

    def send_email(self, date_from=None, date_to=None):
        for record in self:
            template_id = self.env['ir.model.data'].get_object_reference('helpdesk_tracker_hours','helpdesk_report_template')[1]
            email_template_obj = self.env['mail.template'].browse(template_id)
            if template_id:
                data = {
                    'date_from': str(time.strftime('%Y-%m-01')),
                    'date_to': str(fields.Date.today()),
                }
                report_template_id = self.env.ref('helpdesk_tracker_hours.report_customer_support_pdf').with_context(landscape=True)._render_qweb_pdf(self.id, data=data)
                data_record = base64.b64encode(report_template_id[0])
                ir_values = {
                    'name': "Reporte de Horas",
                    'type': 'binary',
                    'datas': data_record,
                    'store_fname': data_record,
                    'mimetype': 'application/x-pdf',
                }
                values = email_template_obj.generate_email(record.partner_id.id, ['subject', 'body_html', 'email_from', 'email_to', 'partner_to', 'email_cc', 'reply_to', 'scheduled_date'])
                values['email_from'] = record.email
                values['email_to'] = record.user_to_id.partner_id.email
                values['email_cc'] = record.user_cc_id.partner_id.email or ''
                data_id = self.env['ir.attachment'].create(ir_values)
                values['attachment_ids'] = [(6, 0, [data_id.id])]
                mail_mail_obj = self.env['mail.mail']
                msg_id = mail_mail_obj.sudo().create(values)
                if msg_id:
                    msg_id.sudo().send()
                    #email_template_obj.attachment_ids = [(3, data_id.id)]
        return True


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    schedule_type = fields.Selection([('weekly', 'Semanal'), ('monthly', 'Mensual')], 'Enviar', related="company_id.schedule_type", readonly=False)
    user_ids = fields.Many2many(related="company_id.user_ids", readonly=False)
    user_to_id = fields.Many2one('res.users', 'Enviar a', related="company_id.user_to_id", readonly=False)
    user_cc_id = fields.Many2one('res.users', 'Enviar CC a', related="company_id.user_cc_id", readonly=False)


