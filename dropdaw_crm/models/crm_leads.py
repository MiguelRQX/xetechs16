from odoo import models, fields, api

class CrmLeads(models.Model):
    _inherit = 'crm.lead'

    name = fields.Many2one('res.list.name.crm', string="Segmento de mercando",ondelete='cascade')
    meeting_count = fields.Integer('# Meetings old', compute='_compute_meeting_count')

    def _compute_meeting_count(self):
        if self.ids:
            meeting_data = self.env['calendar.event'].sudo().read_group([
                ('opportunity_id', 'in', self.ids)
            ], ['opportunity_id'], ['opportunity_id'])
            mapped_data = {m['opportunity_id'][0]: m['opportunity_id_count'] for m in meeting_data}
        else:
            mapped_data = dict()
        for lead in self:
            lead.meeting_count = mapped_data.get(lead.id, 0)