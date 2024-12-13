# -*- coding: utf-8 -*-

from odoo import fields, models


class DteType(models.Model):
    _name = 'dte.type'
    _description = 'DTE Type'

    name = fields.Char('DTE', required=True)
    paf_id = fields.Integer('PAF Id', index=True, required=False)
    code = fields.Char("Codigo DTE", required=False)
    notes = fields.Text('Descripcion', required=False)


