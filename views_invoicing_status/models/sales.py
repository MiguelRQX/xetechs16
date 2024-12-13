# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    total_invoiced = fields.Monetary('Total Invoiced', compute='_compute_total_invoice')
    amount_due = fields.Monetary('Amount Due', compute='_compute_total_invoice')
    total_paid = fields.Monetary('Total Paid', compute='_compute_total_invoice')
    invoice_pending = fields.Monetary('Invoice Pending', compute='_compute_invoice_pending')

    @api.depends("invoice_ids.amount_total", "invoice_ids.amount_residual")
    def _compute_total_invoice(self):
        for record in self:
            
            total_invoiced = amount_due = total_paid = 0.00

            for invoice in record.invoice_ids:
                if invoice.state not in ['draft', 'cancel']:
                    total_invoiced += invoice.amount_total
                    amount_due += invoice.amount_residual
                    total_paid = total_invoiced - amount_due

            for emi_line in record.account_invoice_emi_id.inv_emi_lines:
                if emi_line.invoice_id and emi_line.invoice_id.state not in ['draft', 'cancel']:
                    total_invoiced += emi_line.invoice_id.amount_total
                    amount_due += emi_line.invoice_id.amount_residual
                    total_paid = total_invoiced - amount_due

            record.update({   'amount_due': amount_due, 
                                'total_invoiced': total_invoiced, 
                                'total_paid': total_paid
                            })

    @api.depends('total_invoiced', 'amount_total')
    def _compute_invoice_pending(self):
        for record in self:
            record.update({'invoice_pending': round((record.amount_total - record.total_invoiced), 2)})
