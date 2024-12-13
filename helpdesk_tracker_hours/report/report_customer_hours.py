from odoo import api, models, _
from datetime import datetime

class ReportStockReport(models.AbstractModel):
    _name = 'report.helpdesk_tracker_hours.customer_hours_document'

    @api.model
    def _get_report_values(self, docids, data=None):
        res_data = self.get_values(data=data)
        return {
            'docs': docids,
            'data': res_data,
            'date_from': datetime.strptime(data.get('date_from'), "%Y-%m-%d").strftime("%d/%m/%Y"),
            'date_to': datetime.strptime(data.get('date_to'), "%Y-%m-%d").strftime("%d/%m/%Y"),
            'context': self._context,
        }

    def get_values(self, data=None):
        if not data:
            return {}
        date_from = data.get('date_from', False)
        date_to = data.get('date_to', False)
        partner_ids = self.env['res.partner'].search([
            ('apply_support', '=', True),
            ('active', '=', True)])
        ticket_line_ids = self.env['account.analytic.line'].search([
            ('helpdesk_ticket_id', '!=', False),
            ('date', '>=', date_from),
            ('date', '<=', date_to),
        ])
        ticket_with_contract = []
        res = []
        customer_lines = self.group_by_customer(lines=ticket_line_ids)
        for customer, values in customer_lines.items():
            partner = self.env['res.partner'].browse([customer])
            total_hours = sum(x.unit_amount for x in values)
            line = {
                'type': 'customer',
                'partner': partner.name,
                'employee': "",
                'date': "",
                'ticket': "",
                'contact': "",
                'hours': total_hours or 0.00,
            }
            res.append(line)
            for line in values:
                line = {
                    'type': 'line',
                    'partner': line.partner_id.name,
                    'employee': line.employee_id.name,
                    'date': line.date.strftime("%d/%m/%Y"),
                    'ticket': line.name,
                    'contact': line.helpdesk_ticket_id.partner_id.name,
                    'hours': line.unit_amount,
                }
                res.append(line)
        return res or []
    
    def group_by_customer(self, lines=[]):
        lines_dict = {}
        for line in lines:
            if line.partner_id and line.partner_id.id not in lines_dict:
                lines_dict[line.partner_id.id] = []
            lines_dict[line.partner_id.id].append(line)
        return lines_dict
