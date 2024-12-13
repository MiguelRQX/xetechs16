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
{
    "name": "Helpdesk Tracker Hours",
    "summary": "Helpdesk Tracker Hours",
    'description': """
            Helpdesk Tracker Hours
        """,
    'author': "Xetechs, S.A.",
    'website': "https://www.xetechs.com",
    "version": "13.01",
    "category": "helpdesk",
    "depends": [
        'helpdesk',
        'helpdesk_extends',
        'hr_timesheet',
        'sale_subscription',
        ],
    "data": [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/project_budget_hours_view.xml',
        'views/support_contract_type_view.xml',
        'views/res_config_settings_view.xml',
        'views/helpdesk_ticket_view.xml',
        'wizard/wizard_customer_hours_view.xml',
        'report/reports.xml',
        'report/report_customer_hours_template.xml',
        'data/email_template.xml',
        'data/data.xml',
    ],
    'sequence': 1,
    'installable': True,
    'auto_install': False,
    'application': True,
}
