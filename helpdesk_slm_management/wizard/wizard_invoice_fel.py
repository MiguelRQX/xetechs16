# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime

from odoo.exceptions import UserError, Warning

class WizardInvoiceFel(models.TransientModel):
    _name = "wizard.invoice.fel"
    _description = "Asistente Facturacion FEL"

    @api.model
    def _default_journal(self):
        return self.env['account.journal'].search([('type', '=', 'sale')], limit=1)


    partner_id = fields.Many2one('res.partner', 'Cliente', required=True, copy=False)
    qty_fel = fields.Float("DTE's Consumidos", required=True, default=0.00)
    qty_extra_fel = fields.Float("DTE's Extra Consumidos", required=True, default=0.00)
    sla_id = fields.Many2one('sla.contract', 'Contrato', required=False)

    #Related fields
    journal_id = fields.Many2one('account.journal', 'Diario de Facturacion', required=True, default=_default_journal)
    currency_id = fields.Many2one('res.currency', 'Moneda', related="sla_id.currency_id")
    extra_price_dte = fields.Monetary('Precio Extra DTE', related="sla_id.extra_price_dte")
    price_dte = fields.Monetary('Precio DTE', related="sla_id.price_dte")


    @api.onchange('sla_id')
    def onchange_partner(self):
        if self.sla_id and self.sla_id.partner_id:
            self.partner_id = self.sla_id.partner_id


    def action_invoice_fel(self):
        for rec in self:
            invoice_lines = []
            invoice_dict = {}
            if rec.sla_id.contract_type == 'helpdesk':
                return True
            if not rec.partner_id:
                raise UserError(('No se puede facturar sin cliente asignado'))
            if not rec.journal_id:
                raise UserError(('No se puede facturar sin diario de facturación asignado'))
            if rec.qty_fel <= 0.00 or rec.qty_extra_fel <= 0.00:
                raise UserError(('No se puede facturar con cantidades menores o igual a cero'))
            invoice_dict = {
                'partner_id': rec.partner_id.id or False,
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.today(),
                'journal_id': rec.journal_id.id or False,
                'sla_id': rec.sla_id.id or False,
                'invoice_line_ids': [],
            }
            if rec.qty_fel > 1.00:
                line = {
                    'product_id': rec.sla_id.product_id.id or False,
                    'account_id': (rec.sla_id.product_id.categ_id.property_account_income_categ_id.id or rec.sla_id.product_id.property_account_income_id.id) or False,
                    'quantity': rec.qty_fel,
                    'price_unit': rec.price_dte,
                    'tax_ids': rec.sla_id.product_id.taxes_id.ids,
                }
                invoice_lines.append((0, 0, line))
            if rec.qty_extra_fel > 1.00:
                line = {
                    'product_id': rec.sla_id.product_id.id or False,
                    'account_id': (rec.sla_id.product_id.categ_id.property_account_income_categ_id.id or rec.sla_id.product_id.property_account_income_id.id) or False,
                    'quantity': rec.qty_extra_fel,
                    'price_unit': rec.extra_price_dte,
                    'tax_ids': rec.sla_id.product_id.taxes_id.ids,
                }
                invoice_lines.append((0, 0, line))
            if invoice_lines and invoice_dict:
                invoice_dict.update({
                    'invoice_line_ids': invoice_lines,
                })
                self.env['account.move'].create(invoice_dict)
        return True
    

