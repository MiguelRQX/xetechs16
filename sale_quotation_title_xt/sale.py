# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    note = fields.Html(string="Terminos y Condiciones")
    quotation_title = fields.Char(string="Quotation Title")
