# -*- coding: utf-8 -*-
from odoo import api, models, fields
class Account_Invoice(models.Model):
    _inherit = 'account.move'

    compute_name = fields.Char(string='',compute='find_name')
    compute_name_serie = fields.Char(string='',compute='find_fel_serie')

    @api.depends("fel_no", "name")
    def find_name(self):
            for invoice in self:
                if invoice.fel_no:
                    invoice.update({'compute_name': invoice.fel_no})
                else:
                    invoice.update({'compute_name': invoice.name})

    @api.depends("fel_serie")
    def find_fel_serie(self):
        for invoice in self:
            if invoice.fel_serie:
                invoice.update({'compute_name_serie':invoice.fel_serie})
            else:
                invoice.update({'compute_name_serie':''})
