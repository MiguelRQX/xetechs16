# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Xetechs expense custom settings',
    'version': '15.0.1.0.0',
    'author': 'xetechs',
    'website': 'https://xetechs.com',
    'category': 'Sale',
    'sequence': 2,
    'summary': 'Xetechs expense custom settings',
    'description': '''Xetechs expense custom settings''',
    'depends': ['base', 'hr_expense',],
    'data': [
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
