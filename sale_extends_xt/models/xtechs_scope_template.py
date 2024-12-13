# -*- coding: utf-8 -*-

from odoo import models, fields, api


class XtechsScopeTemplate(models.Model):
    _name = 'xtechs.scope.template'
    _inherit= ['mail.thread']
    _description = 'Modelo para definir plantillas de alcances'

    name = fields.Char(string='Nombre', compute='get_name')
    template_scope = fields.Char(string='Plantilla de alcances', required=True)
    active = fields.Boolean(string='Activo', required=False, default=True)
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.user.company_id.id)
    line_ids = fields.One2many('xtechs.scope.template.lines', 'template_id', string='Alcances')
    hide_company = fields.Boolean(string='Hide', compute='get_companies')

    @api.onchange('template_scope')
    def get_name(self):
        for r in self:
            r.name = str(r.template_scope)

    @api.depends('company_id')
    def get_companies(self):
        for r in self:
            companies = len(self.env.user.company_ids)
            if companies > 1:
                r.hide_company = False
            else:
                r.hide_company = True


class XtechsScopeTemplateLines(models.Model):
    _name='xtechs.scope.template.lines'
    _description='Lineas de plantillas de alcances'
    
    sale_id = fields.Many2one('sale.order', string='Detalle')
    template_id = fields.Many2one('xtechs.scope.template', string='Template')
    scope_id = fields.Many2one('xtechs.scope', string='Alcances')
    time = fields.Float(string='Horas Implementacion', digits=(2,2))
    dev_time = fields.Float(string='Horas Desarrollo', digits=(2,2))
    # description = fields.Html(string='Descripcion', required=True, compute='_onchange_scope_id', inverse='inverse_description', store=True)
    description = fields.Html(string='Descripcion')
    uom_id = fields.Many2one('uom.uom', string='UdM')
    name = fields.Char()
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    sequence = fields.Integer('Sequence',default=100)
    total_time = fields.Float('Total Hrs.', required=False, compute='_compute_total_time')
    

    @api.depends('time', 'dev_time')
    def _compute_total_time(self):
        for rec in self:
            total_time = 0.00
            total_time = rec.time + rec.dev_time
            rec.update({
                'total_time': total_time or 0.00,
            })

    @api.onchange('scope_id')
    def _onchange_scope_id(self):
        if self.scope_id and self.scope_id.description:
            self.description = self.scope_id.description
            self.uom_id = self.scope_id.uom_id.id or False
            self.time = self.scope_id.time or 0.00
            self.dev_time = self.scope_id.dev_time

    # def inverse_description(self):
    #     pass