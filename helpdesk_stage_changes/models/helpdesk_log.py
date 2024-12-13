from odoo import fields, models, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime

class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'
    is_open = fields.Boolean(default=False, string='Etapa inicial')

class HelpdeskLog(models.Model):
    _name = 'helpdesk.log'

    ticket_id = fields.Many2one('helpdesk.ticket')
    change_date = fields.Datetime('Fecha del cambio')
    user_id = fields.Many2one('res.users', string='Usuario')
    last_stage_day_comparison = fields.Float('Dias entre el cambio')
    previous_stage = fields.Text('Stage Anterior')
    current_stage = fields.Text('Stage Nuevo')

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    log_ids = fields.One2many('helpdesk.log', 'ticket_id')
    closure_date = fields.Date('Fecha de cierre', readonly=True)
    closure_date_days_delta = fields.Float('Días transcurridos antes del cierre', readonly=True, compute="_closure_date_days_delta")

    @api.onchange('stage_id')
    def _create_log(self):
        if not self.stage_id.is_open or self.log_ids:
            log_context = {}
            log_context['ticket_id'] = self.id
            log_context['change_date'] = datetime.now()
            log_context['user_id'] = self.env.user.id
            log_context['previous_stage'] = self._origin.stage_id.name
            log_context['current_stage'] = self.stage_id.name
            if self.log_ids:
                delta = datetime.now() - self.log_ids[-1].change_date
                log_context['last_stage_day_comparison'] = float(delta.days)
            self.env['helpdesk.log'].create(log_context)

    def _closure_date_days_delta(self):
        if self.closure_date and self.assign_date:
            delta = self.closure_date - self.assign_date
            self.closure_date_days_delta = delta.days
        else:
            self.closure_date_days_delta = 0



