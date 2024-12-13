from odoo import api, models, fields


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    project_task_id = fields.Many2one('project.task')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    analytic_line_ids = fields.One2many('account.analytic.line', 'project_task_id')


