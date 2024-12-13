# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _compute_tax_id(self):
        for line in self:
            if line.order_id.pricelist_id.name == 'Guatemala':
                line = line.with_company(line.company_id)
                fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id.get_fiscal_position(
                    line.order_partner_id.id)
                # If company_id is set, always filter taxes by the company
                taxes = line.product_id.taxes_id.filtered(lambda t: t.company_id == line.env.company)
                line.tax_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id)

    @api.onchange('product_id')
    def product_id_change(self):

        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            if self.order_id.pricelist_id.name == "Guatemala":
                vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                    self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
            else:
                pricelist_item = self.env['product.pricelist.item'].search(
                    [
                        ('product_tmpl_id', '=', self.product_template_id.id),
                        ('pricelist_id', '=', self.order_id.pricelist_id.id)
                    ]
                )
                if len(pricelist_item) == 1:
                    vals['price_unit'] = pricelist_item.fixed_price
                else:
                    vals['price_unit'] = 0

        self.update(vals)

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            if self.order_id.pricelist_id.name == "Guatemala":
                self.price_unit = self.env['account.tax']._fix_tax_included_price_company(
                    self._get_display_price(product),
                    product.taxes_id, self.tax_id,
                    self.company_id)
            else:
                pricelist_item = self.env['product.pricelist.item'].search(
                    [
                        ('product_tmpl_id', '=', self.product_template_id.id),
                        ('pricelist_id', '=', self.order_id.pricelist_id.id)
                    ]
                )
                if len(pricelist_item) == 1:
                    self.price_unit = pricelist_item.fixed_price
                else:
                    self.price_unit = 0


