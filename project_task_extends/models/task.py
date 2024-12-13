# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval


class TaskTypes(models.Model):
    _name = "task.types"
    _description = "Project Task Priority"
    _rec_name = "name"

    name = fields.Char('Tipo de Prioridad', required=True)
    code = fields.Char('Codigo', required=False)
    active = fields.Boolean('Activo', required=False, default=True)
    notes = fields.Text('Notas')


class ProjectTask(models.Model):
    _inherit = "project.task"

    task_type_id = fields.Many2one('task.types', 'Prioridad', required=False)
    date_start = fields.Date('Fecha Inicio', required=False)
    parent_task_id = fields.Many2one('project.task', 'Predecesora', required=False)