from odoo import api, fields, models

class HelpdeskTiket(models.Model):
    _inherit = 'helpdesk.ticket'

    hours_estimate = fields.Float(string ='Horas estimadas')
    date_deadline = fields.Date(string='Fecha de entrega')
    project_client_id = fields.Many2one('project.project', relation='project_ticket_2_rel', string='Proyecto')
    task_id = fields.Many2one('project.task',string= 'Tarea', domain=[('project_id', '=', 'project_client_id')])
    team_id_name = fields.Char(related= 'team_id.name')


    @api.onchange('project_client_id')
    def set_task_domain(self):

        for data in self:
            data.task_id = False
            return {'domain': {'task_id': [('project_id', '=', data.project_client_id.id)]}}

