# -*- coding: utf-8 -*-


from odoo import fields, models, api
from odoo.exceptions import UserError, Warning
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

import logging


_logger = logging.getLogger( __name__ )

class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'

    progress_stage = fields.Boolean("Etapa de Progreso", required=False, copy=False, default=False)



class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    #SLA Helpdesk management fields
    helpdesk_sla_id = fields.Many2one('sla.contract', 'SLA de Soporte', compute="_compute_helpdesk_sla", store=True)
    change_to_progress = fields.Datetime('Cambio a Progreso', required=False)
    change_to_close = fields.Datetime('Cambio a Cerrado', required=False)
    date_in_progress = fields.Date('Fecha Max en Progreso', compute="_compute_helpdesk_sla", store=True)
    date_to_respond = fields.Date('Fecha Max para Responder', compute="_compute_helpdesk_sla", store=True)
    date_to_close = fields.Date('Fecha Max para Cerrar', compute="_compute_helpdesk_sla", store=True)
    days_in_progress = fields.Integer('Dias Max en Progreso', compute='_compute_days_status')
    days_to_respond = fields.Integer('Dias Max para Responder', compute='_compute_days_status')
    days_to_close = fields.Integer('Dias Max para Cerrar', compute='_compute_days_status')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Vigente'),
        ('unpaid', 'En Mora'),
        ('suspend', 'Suspendido'),
        ('cancel', 'Cancelado'),
        ('expired', 'Vencido')], string="Estatus", related='helpdesk_sla_id.state')
    contracted_hours = fields.Float('Hrs. Contratadas', related="helpdesk_sla_id.contracted_hours")
    hours_consumed = fields.Float('Hrs. Consumidas', related="helpdesk_sla_id.hours_consumed")
    hours_available = fields.Float('Hrs. Disponibles', related="helpdesk_sla_id.hours_available")

    
    @api.onchange('stage_id')
    def _onchange_stage(self):
        if self.stage_id and self.stage_id.progress_stage:
            self.change_to_progress = fields.Datetime.now()
        if self.stage_id and self.stage_id.is_close:
            self.change_to_close = fields.Datetime.now()

    @api.depends(
        'date_to_respond',
        'date_in_progress',
        'date_to_close'
    )
    def _compute_days_status(self):
        for rec in self:
            days_respond = days_progress = days_close = 0.00
            if rec.date_to_respond:
                days_respond = (rec.date_to_respond - fields.Date.today()).days
            if rec.date_in_progress:
                days_progress = (rec.date_in_progress - fields.Date.today()).days
            if rec.date_to_close:
                days_close = (rec.date_to_close - fields.Date.today()).days
            rec.update({
                'days_to_respond': days_respond or 0.00,
                'days_in_progress': days_progress or 0.00,
                'days_to_close': days_close or 0.00,
            })

    @api.depends('helpdesk_sla_id', 'partner_id')
    def _compute_helpdesk_sla(self):
        for rec in self:
            if rec.partner_id:
                sla_id = False
                if rec.partner_id.type == 'contact' and not rec.partner_id.parent_id:
                    sla_id = self.env['sla.contract'].search([
                        ('partner_id', '=', rec.partner_id.id),
                        ('state', 'not in', ('draft', 'cancel'))], limit=1)
                if rec.partner_id.type == 'contact' and rec.partner_id.parent_id:
                    sla_id = self.env['sla.contract'].search([
                        ('partner_id', '=', rec.partner_id.parent_id.id),
                        ('state', 'not in', ('draft', 'cancel'))], limit=1)
                if sla_id:
                    rec.update({
                        'helpdesk_sla_id': sla_id.id or False,
                        'date_to_respond': (rec.create_date if rec.create_date else fields.Date.today()) + relativedelta(days=sla_id.days_to_respond),
                        'date_in_progress': (rec.create_date if rec.create_date else fields.Date.today()) + relativedelta(days=(sla_id.days_to_respond + sla_id.days_in_progress)),
                        'date_to_close': (rec.create_date if rec.create_date else fields.Date.today()) + relativedelta(days=(sla_id.days_to_respond + sla_id.days_in_progress + sla_id.days_to_close))
                })
