# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from dateutil import rrule
import datetime

class Project(models.Model):
    _inherit = 'project.project'


    project_description = fields.Text('Descripcion', required=False)
    total_week = fields.Integer('Semanas', required=False)
    date_start = fields.Date('Fecha de inicio', required=False, default=fields.Date.today())
    current_week = fields.Integer('Semana actual', compute="_compute_current_week", store=False)
    project_progress = fields.Float('Progreso esperado', compute="_compute_progress", store=True)
    real_progress = fields.Float('Progreso real', compute="_compute_progress", store=True)
    date_estimated = fields.Date('Fecha estimada', default=fields.Date.today())
    date_finished = fields.Date('Fecha comprometida', required=False, default=fields.Date.today())
    spi = fields.Float('SPI', compute="_compute_spi", store=True)
    hour_budget = fields.Float('Budget Hours')
    # extension de last_update_status
    last_update_status = fields.Selection(selection=[
        ('on_track', 'A Tiempo'),
        ('at_risk', 'En Riego'),
        ('off_track', 'Fuera de Tiempo'),
        ('on_hold', 'En Espera')
    ], default='on_track', compute='_compute_last_update_status', store=True)

    @api.depends('date_start')
    def _compute_current_week(self):
        current_week = 0
        for rec in self:
            if rec.date_start:
                weeks = rrule.rrule(rrule.WEEKLY, dtstart=rec.date_start, until=fields.Date.today())
                current_week = weeks.count()
            rec.update({
                'current_week': current_week,
            })

    @api.depends('task_ids', 'date_start', 'total_week', 'current_week')
    def _compute_progress(self):
        #task_obj = self.env['project.task']
        project_progress = 0.00
        real_progress = 0.00
        total_task = 0.00
        task_done = 0.00
        for rec in self:
            if rec.total_week and rec.current_week:
                project_progress = (rec.current_week / (rec.total_week if rec.total_week else 1.00)) * 100
            if rec.task_ids:
                total_task = len(rec.task_ids.ids)
                task_done = len(rec.task_ids.filtered(lambda task: task.stage_id.fold == True).ids)
                real_progress = ((task_done) / (total_task if total_task else 1.00)) * 100
            rec.update({
                'project_progress': project_progress if project_progress <= 100.00 else 100.00,
                'real_progress' : real_progress if real_progress <= 100.00 else 100,
                #'spi': real_progress / (project_progress)
            })

    @api.depends('project_progress', 'real_progress')
    def _compute_spi(self):
        spi = 0.00
        for rec in self:
            spi = (rec.real_progress / (rec.project_progress if rec.project_progress else 1.00)) * 100
            rec.update({
                'spi': spi if spi <= 100 else 100.00
            })


class ProjectTask(models.Model):
    _inherit = "project.task"

    criteria_of_acceptance = fields.Html(string='Criterios de Aceptacion')
    reason_of_task = fields.Html(string='Motivos de la Tarea')
    requeriments = fields.Html(string='Requisitos')

class ProjectUpdate(models.Model):
    _inherit = 'project.update'

    # extension de status
    status = fields.Selection(selection=[
        ('on_track', 'A Tiempo'),
        ('at_risk', 'En Riego'),
        ('off_track', 'Fuera de Tiempo'),
        ('on_hold', 'En Espera')
    ], required=True, tracking=True)
