# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import requests
import json
from odoo.exceptions import UserError

class ResCompany(models.Model):
    _inherit = "res.company"

    active_paf = fields.Boolean('Activar Megaprint PAF', default=False)
    username_paf = fields.Char('Usuario PAF', required=False)
    password_paf = fields.Char('Password PAF', required=False)
    token_access_paf = fields.Char('Token', required=False)
    url_token_paf = fields.Text('Url Token',)
    url_type_dte_paf = fields.Text('Url Tipos DTE')
    url_validate_template = fields.Text('Url Validar Plantilla')
    url_rtu = fields.Text('Url RTU')
    url_contract_request = fields.Text('Url Afiliacion')
    url_send_contract = fields.Text('Url Enviar Contrato')


    def get_access_token(self):
        for rec in self:
            post_url = rec.url_token_paf
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": rec.token_access_paf
            }
            if rec.active_paf:
                if not rec.username_paf and not rec.password_paf:
                    raise UserError(('La empresa %s no tiene credenciales configuradas') %(rec.name))
                data = (('grant_type=password&username=%s&password=%s') %(rec.username_paf, rec.password_paf))
                try:
                    response  = requests.post(post_url, data=data, headers=headers, stream=True, verify=False)
                    if response.status_code == 200:
                        content = json.loads(response.content.decode('utf-8'))
                        return content
                    else:
                        raise UserError(('%s') %(response.content.decode('utf-8')))
                except Exception as e:
                    raise UserError(('%s') %(e))
                    #return True


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    active_paf = fields.Boolean('Activar Megaprint PAF', readonly=False, related="company_id.active_paf")
    username_paf = fields.Char('Usuario PAF', readonly=False, related="company_id.username_paf")
    password_paf = fields.Char('Password PAF', readonly=False, related="company_id.password_paf")
    token_access_paf = fields.Char('Token', readonly=False, related="company_id.token_access_paf")

    def action_get_token(self):
        for rec in self:
            post_url = rec.company_id.url_type_dte_paf
            token = rec.company_id.get_access_token()
            headers = {
                "Content-Type": "application/json",
                "Authorization": ("Bearer %s" %(token.get('access_token', '')))
            }
            try:
                response  = requests.get(post_url, headers=headers, stream=True, verify=False)
                if response.status_code == 200:
                    content = json.loads(response.content.decode('utf-8'))
                    #raise UserError(('%s') %(content))
                    for dte in content:
                        #raise UserError(('%s') %(dte))
                        dte_id = self.env['dte.type'].search([('paf_id', '=', int(dte.get('id', False))), ('code', '=', dte.get('code', False))], limit=1)
                        if not dte_id:
                            self.env['dte.type'].create({
                                'paf_id': dte.get('id', False),
                                'name': dte.get('description', False),
                                'code': dte.get('code', False),
                            })
                else:
                    raise UserError(('%s') %(response.content.decode('utf-8')))
            except Exception as e:
                raise UserError(('%s') %(e))
                #return True

