# -*- encoding: UTF-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2015-Today Xetechs, S.A.
# (<http://www.xetechs.com>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
import logging

from odoo import fields, models, tools

_logger = logging.getLogger(__name__)


class HelpdeskBudgetHours(models.Model):
    _name = "report.helpdesk.budget.hours"
    _description = "Helpdesk budget Hours"
    _rec_name = "ticket_month"
    _auto = False

    ticket_month = fields.Char('Date')
    contrated_hours = fields.Float(string="Hours Contrated")
    customer_id = fields.Many2one('res.partner', 'Contact')
    parent_id = fields.Many2one('res.partner', 'Customer')
    amount_hours = fields.Float('Consumido', readonly=True)
    contrated_hours = fields.Float('Presupuesto', readonly=True)
    residual = fields.Float('Residual', readonly=True)
    percent = fields.Float('Percent', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
                SELECT
                    row_number() OVER () AS id,
                    to_char(aal.date,'MM/YYYY') AS ticket_month,
                    CASE
                        WHEN cust.parent_id is not null 
                        THEN cust.parent_id
                        ELSE cust.id 
                    END AS parent_id,
					cust.id as customer_id,
					CASE	
                        WHEN cust.parent_id is not null
                        THEN (select contrated_hours from res_partner where id = cust.parent_id limit 1)
                        ELSE cust.contrated_hours
                        END AS contrated_hours,
                    sum(aal.unit_amount) as amount_hours,
                    COALESCE((CASE	
                        WHEN cust.parent_id is not null
                        THEN (select contrated_hours from res_partner where id = cust.parent_id limit 1)
                        ELSE cust.contrated_hours
                        END), 0.00) - COALESCE(SUM(aal.unit_amount), 0.00) as residual,
                    CASE 
                        WHEN (COALESCE((CASE	
                        WHEN cust.parent_id is not null
                        THEN (select contrated_hours from res_partner where id = cust.parent_id limit 1)
                        ELSE cust.contrated_hours
                        END), 0.00) - COALESCE(SUM(aal.unit_amount), 0.00)) < 0.00
                        THEN 100.00
                        ELSE
                            ((COALESCE(SUM(aal.unit_amount), 0.00)) / (CASE	
                                WHEN cust.parent_id is not null
                                THEN (select contrated_hours from res_partner where id = cust.parent_id limit 1)
                                ELSE cust.contrated_hours
                                END)) * 100
                        END AS percent
                FROM 
                    account_analytic_line as aal
                INNER JOIN 
                    helpdesk_ticket ticket on ticket.id = aal.helpdesk_ticket_id
                INNER JOIN 
                    res_partner cust on cust.id = ticket.partner_id
                GROUP By
                    ticket_month,
					cust.id,
					cust.parent_id,
                    contrated_hours
                ORDER BY
                    ticket_month;
        """ %(self._table))

