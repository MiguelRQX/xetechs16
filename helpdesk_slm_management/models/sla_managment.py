# -*- coding: utf-8 -*-


from odoo import fields, models, api
from odoo.exceptions import UserError, Warning
import time
from datetime import datetime
from dateutil import relativedelta

import logging


_logger = logging.getLogger( __name__ )


CONTRACT_PRIORITY = [
    ('0', 'All'),
    ('1', 'Baja'),
    ('2', 'Media'),
    ('3', 'Alta'),
]
class SlaContract(models.Model):
    _name = "sla.contract"
    _inherit = ['portal.mixin', 'mail.thread.cc', 'utm.mixin', 'rating.mixin', 'mail.activity.mixin']
    _description = "SLA Contract"

    name = fields.Char('Contract Code', required=False, copy=False, default="/", tracking=True)
    contract_number = fields.Char('Contract Number', required=False, copy=False, default="/", tracking=True)
    partner_id = fields.Many2one('res.partner', 'Cliente', required=False, copy=False, tracking=True)
    contract_from = fields.Date('Fecha Inicio', required=False, copy=False, default=lambda *a: time.strftime('%Y-%m-01'))
    contract_to = fields.Date('Fecha Fin', required=False, copy=False, default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
    contract_type = fields.Selection([
        ('helpdesk', 'Soporte Tecnico'),
        ('fel', 'Facturación Electrónica -FEL-')], string="Tipo de Contrato", required=False, default="helpdesk", tracking=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Vigente'),
        ('unpaid', 'En Mora'),
        ('suspend', 'Suspendido'),
        ('cancel', 'Cancelado'),
        ('expired', 'Vencido')], string="Estatus", required=False, copy=False, default="draft")
    priority = fields.Selection(CONTRACT_PRIORITY, string='Prioridades', default='0')
    subscription_id = fields.Many2one('sale.subscription', 'Suscripción', required=False, copy=False)
    invoice_ids = fields.One2many('account.move', 'sla_id', string='Facturas', required=False, copy=False)
    invoice_count = fields.Integer('# Facturas', compute="_compute_counters")
    
    #helpdesk Fields
    sla_level = fields.Selection([
        ('bronce', 'Bronce'),
        ('silver', 'Plata'),
        ('gold', 'Oro')], string="Tipo de Soporte", required=False, default="bronce", tracking=True)
    contracted_hours = fields.Float('Hrs. Contratadas', required=False, copy=False, tracking=True)
    hours_consumed = fields.Float('Hrs. Consumidas', compute='_compute_ticket_hours')
    hours_available = fields.Float('Hrs. Disponibles', compute='_compute_ticket_hours')
    days_in_progress = fields.Integer('Dias Max en Progreso', required=False, copy=False, tracking=True)
    days_to_respond = fields.Integer('Dias Max para Responder', required=False, copy=False, tracking=True)
    days_to_close = fields.Integer('Dias Max para Cerrar', required=False, copy=False, tracking=True)

    #FEL Fields
    qty_dte = fields.Float('DTE Contratadas', required=False, copy=False)
    extra_price_dte = fields.Monetary('Precio Extra DTE')
    price_dte = fields.Monetary('Precio DTE', required=False, copy=False)
    total_dte = fields.Monetary('Costo Total DTE', compute="_compute_dte", store=False)
    product_id = fields.Many2one('product.product', 'Producto', )

    #helpdesk ticket
    helpdesk_ticket_ids = fields.One2many('helpdesk.ticket', 'helpdesk_sla_id', string='Tickets')
    helpdesk_ticket_count = fields.Integer('# Tickets')


    #Multi-company
    company_id = fields.Many2one('res.company', 'Compañia', required=False, copy=False, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', 'Moneda', related="company_id.currency_id")


    @api.depends('contracted_hours', 'helpdesk_ticket_ids')
    def _compute_ticket_hours(self):
        for rec in self:
            amount_consumed = amount_balance = 0.00
            for line in rec.helpdesk_ticket_ids.timesheet_ids:
                amount_consumed += line.unit_amount
            rec.update({
                'hours_consumed': amount_consumed or 0.00,
                'hours_available': (rec.contracted_hours - amount_consumed) or 0.00,
            })


    @api.depends('invoice_ids', 'helpdesk_ticket_ids')
    def _compute_counters(self):
        for rec in self:
            rec.update({
                'invoice_count': len(rec.invoice_ids.ids) if rec.invoice_ids else 0,
                'helpdesk_ticket_count': len(rec.helpdesk_ticket_ids.ids) if rec.helpdesk_ticket_ids else 0,
            })

    @api.depends('qty_dte', 'price_dte')
    def _compute_dte(self):
        for rec in self:
            rec.update({
                'total_dte': (rec.qty_dte * rec.price_dte) or 0.00,
            })


    def action_active(self):
        for rec in self:
            sequence = ""
            number = self.env['ir.sequence'].next_by_code('sla.contract') or "/"
            if rec.partner_id and rec.partner_id.country_id:
                sequence = (("%s-%s") %(rec.partner_id.country_id.code, number))
            rec.write({
                'state': 'active',
                'name': sequence,
            })
        return True

    def action_view_invoices(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('account.action_move_out_invoice_type')
        action['context'] = {}
        action['domain'] = [('id', 'in', self.invoice_ids.ids)]
        return action

    def action_view_tickets(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('helpdesk.helpdesk_ticket_action_main_tree')
        action['context'] = {}
        action['domain'] = [('id', 'in', self.helpdesk_ticket_ids.ids)]
        return action
