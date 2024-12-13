# -*- coding: utf-8 -*-

import logging
import datetime
import traceback
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from collections import Counter
from dateutil.relativedelta import relativedelta
from uuid import uuid4

_logger = logging.getLogger(__name__)

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription'

    @api.depends('recurring_invoice_line_ids.price_subtotal')
    def _amount_all(self):
        """
        Compute the total amounts of the subscription.
        """
        for subscription in self:
            amount_tax = 0.0
            recurring_total = 0.0
            for line in subscription.recurring_invoice_line_ids:
                recurring_total += line.price_subtotal
                # _amount_line_tax needs singleton
                amount_tax += line._amount_line_tax()
            recurring_tax = subscription.currency_id and subscription.currency_id.round(amount_tax) or 0.0
            subscription.update({
                'recurring_total': recurring_total,
                'recurring_tax': recurring_tax,
                'recurring_total_incl': recurring_tax + recurring_total,
            })

    #def _prepare_invoice_line(self, line, fiscal_position, date_start=False, date_stop=False):
    #    if 'force_company' in self.env.context:
    #        company = self.env['res.company'].browse(self.env.context['force_company'])
    #    else:
    #        company = line.analytic_account_id.company_id
    #        line = line.with_context(force_company=company.id, company_id=company.id)

    #    fpos = self.env['account.fiscal.position'].browse(fiscal_position or None)
    #    tax_ids = fpos.map_tax(
    #        line.product_id.taxes_id.filtered(lambda t: t.company_id == company)
    #    )
    #    accounts = line.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fpos)
    #    if line.analytic_account_id.pricelist_id.name == "Guatemala":
    #        return {
    #            'name': line.name,
    #            'subscription_id': line.analytic_account_id.id,
    #            'price_unit': line.price_unit or 0.0,
    #            'discount': line.discount,
    #            'quantity': line.quantity,
    #            'product_uom_id': line.uom_id.id,
    #            'product_id': line.product_id.id,
    #            'account_id': accounts['income'],
    #            'tax_ids': [(6, 0, tax_ids.ids)],
    #            'analytic_account_id': line.analytic_account_id.analytic_account_id.id,
    #            'analytic_tag_ids': [(6, 0, line.analytic_account_id.tag_ids.ids)],
    #            'subscription_start_date': date_start,
    #            'subscription_end_date': date_stop,
    #        }
    #    else:

    #        return {
    #            'name': line.name,
    #            'subscription_id': line.analytic_account_id.id,
    #            'price_unit': line.price_unit or 0.0,
    #            'discount': line.discount,
    #            'quantity': line.quantity,
    #            'product_uom_id': line.uom_id.id,
    #            'product_id': line.product_id.id,
    #            'account_id': accounts['income'],
    #            'analytic_account_id': line.analytic_account_id.analytic_account_id.id,
    #            'analytic_tag_ids': [(6, 0, line.analytic_account_id.tag_ids.ids)],
    #            'subscription_start_date': date_start,
    #            'subscription_end_date': date_stop,
    #        }




class SaleSubscriptionLine(models.Model):
    _inherit = "sale.subscription.line"


    @api.depends('quantity', 'discount', 'price_unit', 'analytic_account_id.pricelist_id', 'uom_id')
    def _compute_amount(self):
        """
        Compute the amounts of the Subscription line.
        """
        AccountTax = self.env['account.tax']
        for line in self:
            if line.analytic_account_id.pricelist_id == "Guatemala":
                price = AccountTax._fix_tax_included_price(line.price_unit, line.product_id.sudo().taxes_id, AccountTax)
                price_subtotal = line.quantity * price * (100.0 - line.discount) / 100.0
                if line.analytic_account_id.pricelist_id.sudo().currency_id:
                    price_subtotal = line.analytic_account_id.pricelist_id.sudo().currency_id.round(price_subtotal)
            else:
                price_subtotal = line.quantity * line.price_unit * (100.0 - line.discount) / 100.0
            line.update({
                'price_subtotal': price_subtotal,
            })

