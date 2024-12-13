# -*- encoding: UTF-8 -*-


from odoo import fields, api, models, _
from odoo.exceptions import ValidationError


class HelpdeskTicket1(models.Model):

    _inherit = 'helpdesk.ticket'

    parent_id = fields.Many2one('helpdesk.ticket', 'Parent Ticket', ondelete='cascade')
    child_ids = fields.One2many('helpdesk.ticket', 'parent_id', string="Child Ticktes")
    ticket_count = fields.Integer('Child Tickets', compute='_compute_child_ticket_count')
    is_close = fields.Boolean('Closed')

    def name_get(self):
        result = []
        for ticket in self:
            result.append((ticket.id, "%s (#%s)" % (ticket.name, ticket.id)))
        return result

    def write(self, vals):
        res = super(HelpdeskTicket1, self).write(vals)
        if res is not None:
            if vals.get('stage_id'):
                stage = self.env['helpdesk.stage'].browse(vals.get('stage_id'))
                if stage.fold:
                    if not all(child.stage_id == stage for child in self.child_ids):
                        raise ValidationError(
                            _("You cannot closed ticket until child tickets are open!"))
        return res

    @api.constrains('parent_id')
    def _check_parent_id(self):
        for rec in self:
            if not rec._check_recursion():
                raise ValidationError(
                    _('You cannot create recursive tickets.'))

    def _compute_child_ticket_count(self):
        for rec in self:
            ticket_count = self.env['helpdesk.ticket'].search_count([
                ('parent_id', '=', rec.id)])
            rec.ticket_count = ticket_count

    def create_child_ticket(self):
        for res in self:
            action = self.env.ref(
                'helpdesk.helpdesk_ticket_action_main_tree').read()[0]
            action['views'] = [(False, 'form')]
            action['target'] = 'new'
            ctx = {
                    'default_partner_id': res.partner_id and res.partner_id.id or False,
                    'default_ticket_type_id': res.ticket_type_id and res.ticket_type_id.id or False,
                    'default_priority': res.priority,
                    'default_parent_id': res.id
                }
            if res.tag_ids:
                ctx['default_tag_ids'] = [(6, 0, res.tag_ids and res.tag_ids.ids)],
            action['context'] = ctx
            return action

    def action_view_ticket(self):
        ticket_obj = self.env['helpdesk.ticket']
        ticket_ids = ticket_obj.search([
            ('parent_id', '=', self.id)])
        action = self.env.ref('helpdesk.helpdesk_ticket_action_main_tree').read()[0]
        if len(ticket_ids) > 1:
            action['domain'] = [('id', 'in', ticket_ids.ids)]
        elif len(ticket_ids) == 1:
            action['views'] = [
                (self.env.ref('helpdesk.helpdesk_ticket_view_form').id, 'form')]
            action['res_id'] = ticket_ids.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
