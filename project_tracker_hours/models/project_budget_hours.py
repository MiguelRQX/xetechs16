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


class ProjectBudgetHours(models.Model):
    _name = "report.project.budget.hours"
    _description = "Project budget Hours"
    _order = 'month, year desc'
    _auto = False

    name = fields.Char('Date')
    project_id = fields.Many2one('project.project', 'Proyecto')
    employee_id = fields.Many2one('hr.employee', 'Empleado', readonly="1")
    month = fields.Char(string="Month", readonly=True)
    year = fields.Char(string="Year", readonly=True)
    amount_hours = fields.Float('Consumido', readonly=True)
    budget_hours = fields.Float('Presupuesto', readonly=True)
    residual = fields.Float('Residual', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              SELECT
                row_number() OVER () AS id, 
                to_char(aal.date,'MM') AS month,
                to_char(aal.date,'YYYY') AS year,
                CONCAT(to_char(aal.date,'MM'), '/', to_char(aal.date,'YYYY')) as name,
                SUM(aal.unit_amount) as amount_hours,
                project_id as project_id,
                aal.employee_id as employee_id,
                pj.budget_hours as budget_hours,
                COALESCE(pj.budget_hours, 0.00) - COALESCE(SUM(aal.unit_amount), 0.00) as residual
            FROM account_analytic_line as aal
            INNER JOIN project_project pj on pj.id = aal.project_id
            GROUP BY 
                month,
                year,
                project_id,
                budget_hours,
                employee_id
            ORDER BY 
                month,year;
        """ %(self._table))


