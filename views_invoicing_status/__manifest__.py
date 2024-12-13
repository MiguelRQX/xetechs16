# -*- coding: utf-8 -*-
{
    'name': 'fields invoicing status',
    'version': '15.0.1.0.0',
    'category': 'Extra tools',
    'sumary': 'Campos de estados de la facturacion',
    'license': 'AGPL-3',
    'author': 'Xetechs',
    'website': 'https://xetechs.odoo.com',
    'maintainer': 'Xetechs, S.A.',
    'depends': [
        'sale',
        'account',
        'account_invoice_emi'
    ],  
    'data': [
        'views/sales_views.xml'
    ],
    'installable': True,
    'aplication': True,
    'auto_install': False,
}
