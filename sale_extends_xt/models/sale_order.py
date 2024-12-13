# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit='sale.order.line'
    
    so_approved_line = fields.Boolean(string="SO line approved?", default=False, readonly=True, store=True)
    so_approved_line_discount = fields.Boolean(string="SO line approved?", default=False, readonly=False, store=True)
    
    @api.onchange('price_unit', 'product_uom_qty')
    def _onchange_so_approved(self):
        for line in self:
            in_group = self.env.user.has_group('sale_extends_xt.group_sales_admin_xt')
            if not in_group:
                line.so_approved_line = True
            else:
                line.so_approved_line = False
    
    @api.onchange('discount')
    def _onchange_discount_so_approved(self):
        for line in self:
            in_group = self.env.user.has_group('sale_extends_xt.group_sales_admin_xt')
            if not in_group:
                if line.discount > 5.00:
                    line.so_approved_line_discount = True
                else:
                    line.so_approved_line_discount = False
            else:
                line.so_approved_line_discount = False
                
                
class SaleOrder(models.Model):
    _inherit='sale.order'

    template_id = fields.Many2one('xtechs.scope.template', string='Plantilla de Alcance', required=False)
    line_ids = fields.One2many('xtechs.scope.template.lines', 'sale_id', string='Detalle de Alcances')
    header_note = fields.Html(string='Introduccion')
    footer_note = fields.Html(string='Pie de Pagina')
    so_approved = fields.Boolean(string="SO approved?", default=False, readonly=True, store=True)
    discount_xt = fields.Boolean(string="discount?", default=False, compute='_compute_discount_xt')
    price_xt = fields.Boolean(string="discount in order?", default=False, compute='_compute_price_xt')
    save_order_xt = fields.Char(string="Motivo del Descuento", compute='_compute_save_order_xt')
    note_xt = fields.Boolean(string="note in order?", default=False, store=True)
    note_count_xt = fields.Float(string="note counter", default=0.00)
    discount_note_xt = fields.One2many('sale.order.note', 'sale_id', string='note del descuento')
    global_discount = fields.Float(string="Descuento Global(%)")
    global_discount_xt = fields.Boolean(string="discount?", default=False, store=True)
    state = fields.Selection([
        ('draft', 'Presupuesto'),
        ('approved', 'Presupuesto Aprobado'),
        ('sent', 'Presupuesto Enviado'),
        ('sale', 'Pedido de Venta'),
        ('done', 'Bloqueado'),
        ('cancel', 'Cancelado'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    
    def approve_so(self):
        for order in self:
            order.so_approved = True
            order.state = 'approved'
            order.global_discount_xt = False
            
    def set_global_discount(self):
        for order in self:
            for line in order.order_line:
                line.discount = order.global_discount
            in_group = self.env.user.has_group('sale_extends_xt.group_sales_admin_xt')
            if not in_group and order.state == 'approved':
                order.so_approved = False
                order.state = 'draft'
                order.global_discount_xt = True
                order._compute_save_order_xt()
                order.note_count_xt +=1
                discount_note_xt = []
                discount_note_xt.append((0, 0, {
                    'note_change_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'name': '',
                }))
                order.discount_note_xt = discount_note_xt
                if order.note_count_xt > 0:
                    order.note_xt = True
                  
    @api.onchange('template_id')
    def _onchange_template_id(self):
        x=0
        scope_lines=[]
        self.line_ids = [(5,0,0)]
        if self.template_id:
            for l in self.template_id.line_ids:    
                _logger.info(l)
                scope_lines.append((0,0,{
                    'scope_id' : l.scope_id,
                    'description' : l.description,
                    'time' : l.time,
                    'uom_id' : l.uom_id,
                    'name' : l.name,
                    'sequence' : l.sequence,
                    'display_type' : l.display_type
                }))
            self.line_ids = scope_lines
             
    @api.depends('order_line.so_approved_line')
    def _compute_discount_xt(self):
        for order in self:
            in_group = self.env.user.has_group('sale_extends_xt.group_sales_admin_xt')
            order.discount_xt = False
            if not in_group:
                for line in order.order_line:
                    if line.so_approved_line:
                        order.discount_xt = True
    
    @api.depends('order_line.so_approved_line_discount')
    def _compute_price_xt(self):
        for order in self:
            in_group = self.env.user.has_group('sale_extends_xt.group_sales_admin_xt')
            order.price_xt = False
            if not in_group:
                for line in order.order_line:
                    if line.so_approved_line_discount:
                        order.price_xt = True
    
    @api.onchange('discount_xt', 'price_xt')
    def _onchange_so_approved(self):
        for order in self:
            if order.discount_xt or order.price_xt:
                order.so_approved = False
                order.state = 'draft'
            else:
                order.so_approved = True
    
    @api.onchange('price_xt')
    def _onchange_state_xt(self):
        for order in self:
            if order.state == 'draft' and order.price_xt:
                order.note_count_xt +=1
                discount_note_xt = []
                discount_note_xt.append((0, 0, {
                    'note_change_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'name': '',
                }))
                order.discount_note_xt = discount_note_xt
            if order.note_count_xt > 0:
                order.note_xt = True
                
                
    @api.depends('state', 'price_xt', 'discount_note_xt', 'global_discount_xt')
    def _compute_save_order_xt(self):
        for order in self:
            if order.state == 'draft' and order.price_xt and order.note_xt or order.global_discount_xt and order.state == 'draft':
                line_empty = False
                for line in order.discount_note_xt:
                    if line.name == '':
                        line_empty = True
                if line_empty:
                    order.save_order_xt = ''
                else:
                    order.save_order_xt = 'Listo'
            else:
                order.save_order_xt = 'Listo'
                
                
class SaleOrderNote(models.Model):
    _name = 'sale.order.note'
    _description = 'Sale Order Note'
    
    sale_id = fields.Many2one('sale.order', string='Detalle')
    note_change_date = fields.Datetime('Fecha', readonly=True)
    name = fields.Char('Motivo', required=True)
    
    