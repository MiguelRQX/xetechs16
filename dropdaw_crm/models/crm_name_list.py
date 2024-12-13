from odoo import models, fields, api


class MarketSegment(models.Model):
    _name = 'res.list.name.crm'

    name = fields.Char('Nombre de Oportunidad')
    description = fields.Char('Descripcion')
