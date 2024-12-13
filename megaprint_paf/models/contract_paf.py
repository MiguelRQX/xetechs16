# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare

import requests
import json
from odoo.exceptions import UserError

from werkzeug.urls import url_encode

class ContractPaf(models.Model):
    _name = 'contract.paf'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Afiliacion de Emisor'


    name = fields.Char('Correlativo', required=False, default="/", tracking=True)
    date = fields.Date('Fecha', tracking=True, default= fields.Date.today())
    partner_id = fields.Many2one('res.partner', 'Emisor', required=True, tracking=True)
    company_id = fields.Many2one('res.company', 'Re-seller', default=lambda self: self.env.company.id)
    establishment_ids = fields.One2many('customer.establishment', 'contract_id', string="Establecimientos")
    razon_social = fields.Char('Nombre', required=False, readonly=False, tracking=True)
    nit_emisor = fields.Char('Nit', required=False, readonly=False, tracking=True)
    dte_qty = fields.Integer('Cant. DTE', required=True, Default=1.00, tracking=True)
    payment_method = fields.Selection([('1','Mensual'), ('2', 'Anual')], string="Periodo de Cobro", required=False, default='1', tracking=True)
    payment_month = fields.Selection([('1','Enero'), ('2','Febrero'), ('3','Marzo'), ('4','Abril'), ('5','Mayo'), ('6','Junio'), ('7','Julio'), ('8','Agosto'), ('9','Septiembre'), ('10','Octubre'), ('11','Noviembre'), ('12','Diciembre')], string="Mes de pago", default="1", tracking=True)
    affiliation_iva = fields.Selection([('GEN', 'General'), ('EXE', 'Exentos'), ('PEQ', 'Pequeño Contribuyente'), ('PEE', 'Pequeño Contribuyente Electronico'), ('AGR', 'Agropecuario'), ('AGE', 'Agropecuario Electronico')], string="Afiliacion IVA", required=False, default='GEN', tracking=True)
    services_ids = fields.Many2many('paf.service', 'relation_contract_service', 'contract_id', 'service_id', string="Servicios", copy=False, readonly=False, tracking=True)
    certificate_key = fields.Text('Certificado', required=True, default="/")
    private_key = fields.Text('Llave Privada', required=True, default="/")
    state = fields.Selection([('new','Borrador'), ('done','Afiliado'), ('cancel', 'Cancelado')], string="Estado", default="new", tracking=True)
    user_id = fields.Many2one('res.users', 'Usuario', default=lambda self: self.env.user.id, tracking=True)
    dte_type_ids = fields.Many2many('dte.type', 'relation_contract_dte', 'contract_id', 'dte_type_id', string="Documentos", copy=False, readonly=False)
    #PAF Fields
    


    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('contract.paf') or _('/')
        result = super(ContractPaf, self).create(vals)
        return result

    def action_get_rtu(self):
        for rec in self:
            post_url = rec.company_id.url_rtu
            token = rec.company_id.get_access_token()
            if not rec.partner_id:
                raise UserError(('No hay emisor seleccionado.!'))
            if rec.partner_id and not rec.partner_id.vat:
                raise UserError(('El cliente %s no tiene nit registrado.!') %(rec.partner_id.name))
            post_url = (("%s%s") %(post_url, rec.partner_id.vat))
            headers = {
                "Content-Type": "application/json",
                "Authorization": ("Bearer %s" %(token.get('access_token', '')))
            }
            try:
                response  = requests.get(post_url, headers=headers, stream=True, verify=False)
                if response.status_code == 200:
                    #raise UserError(('%s') %(response.content.decode('utf-8')))
                    est_ids = []
                    content = json.loads(response.content.decode('utf-8'))
                    rtu = content.get('rtu', False)
                    for est in rtu.get('establishments', []):
                        res = {
                            'name': est.get('name', False),
                            'street': est.get('streetAvenue', False),
                            'city': est.get('department', False),
                            'state': est.get('municipality', False),
                            'status': True if est.get('status', False) == 'A' else False,
                        }
                        est_ids.append((0,0,res))
                    rec.write({
                        'razon_social': rtu.get('name', False),
                        'nit_emisor': rtu.get('nit', False),
                        'affiliation_iva': rtu.get('ivaAfiliationDTO', False),
                        'establishment_ids': est_ids,
                    })
                else:
                    raise UserError(('%s') %(response.content.decode('utf-8')))
            except Exception as e:
                raise UserError(('%s') %(e))

    def action_send_contract(self):
        return self.write({'state': 'done'})

    def action_cancel(self):
        return self.write({'state': 'cancel'})


class Customerstablishment(models.Model):
    _name = "customer.establishment"
    _description = "Establecimientos de emisor"

    name = fields.Char('Establecimiento', required=False)
    street = fields.Char('Direccion', required=False)
    city = fields.Char('Departamento', required=False)
    state = fields.Char('Municipio', required=False)
    status = fields.Boolean('Activo', default=False)
    contract_id = fields.Many2one('contract.paf', 'Afiliacion', ondelete="cascade")



class PafService(models.Model):
    _name = "paf.service"

    name = fields.Char('Servicio', required=False)
    code = fields.Char('Codigo PAF', required=False)

