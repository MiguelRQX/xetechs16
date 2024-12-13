# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang

class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'
    
    def map_tax(self, taxes, product=None, partner=None):
        if not self:
            return taxes
        result = self.env['account.tax']
        for tax in taxes:
            taxes_correspondance = self.tax_ids.filtered(lambda t: t.tax_src_id == tax._origin)
            result |= taxes_correspondance.tax_dest_id if taxes_correspondance else tax
        return result