# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Project Task Extends',
    "version": "15.0.1.0.0",
    'website': 'https://www.xetechs.odoo.com/',
    'category': 'Project',
    'sequence': 1,
    'summary': 'Project Task Extends',
    'depends': ['project'],
    'description': "",
    'data': [
        'security/ir.model.access.csv',
        'views/task_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
