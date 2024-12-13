# -*- coding: utf-8 -*-


{
    'name': 'Information payment in invoice',
    'version': '1.0.1',
    'author': 'Xetechs, S.A.',
    'website': 'https://www.xetechs.com', 
    'support': 'Xetechs, S.A.', 
    'category': 'Accounting',
    'depends': ['account', 'account_invoice_megaprint'],
    'summary': 'Information payment in invoice',
    'data': [
        'views/information_payment_invoice.xml',
        'views/information_payment_invoice_fel.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}