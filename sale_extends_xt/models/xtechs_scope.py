# -*- coding: utf-8 -*-

from odoo import models, fields, api


class XtechsScope(models.Model):
    _name = 'xtechs.scope'
    _inherit= ['mail.thread']
    _description = 'Modelo para manejar el mantenimiento de alcances'

    name = fields.Char(string='Nombre', compute='get_name')
    uom_id = fields.Many2one('uom.uom', string='UdM')
    scope = fields.Char(string='Alcance', required=True)
    active = fields.Boolean(string='Activo', required=False, default=True)
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.user.company_id.id)
    description = fields.Html(string='Descripción')
    img = fields.Binary(string='img')
    time = fields.Float('Horas Implementacion', required=False)
    dev_time = fields.Float('Horas Desarrollo', required=False)
    hide_company = fields.Boolean(string='Hide', compute='get_companies')
    total_time = fields.Float('Total Hrs.', required=False, compute='_compute_total_time')

    @api.depends('time', 'dev_time')
    def _compute_total_time(self):
        for rec in self:
            total_time = 0.00
            total_time = rec.time + rec.dev_time
            rec.update({
                'total_time': total_time or 0.00,
            })


    @api.onchange('scope')
    def get_name(self):
        for r in self:
            r.name = str(r.scope)

    @api.depends('company_id')
    def get_companies(self):
        for r in self:
            companies = len(self.env.user.company_ids)
            if companies > 1:
                r.hide_company = False
            else:
                r.hide_company = True

