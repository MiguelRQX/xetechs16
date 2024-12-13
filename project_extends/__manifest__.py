# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Task Extends',
    "version": "15.0.1.0.0",
    'category': 'Project',
    'sequence': 4,
    'summary': 'Project Issue',
    'description': """
Project Task Extends
    """,
    'website': 'https://www.xetechs.com/',
    'author': 'Xetechs, S.A.',
    'support': 'Luis Aquino -> laquino@gmail.com',
    'depends': ['project', 'hr_timesheet', 'sale_timesheet_enterprise', 'project_task_extends'],
    'data': [
        'views/project_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
