# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
{
    'name': 'Invoice Exchange Rate Tree View',
    'version': '15.0.1.0.0',
    'category': 'Account',
    'license': 'AGPL-3',
    'summary': 'Adds a field on tree view customer invoices',
    'description': """
Sale Quotation Title
====================

This module only adds a field *conversion rate* on account.move customer view.

    """,
    'author': 'Xetechs',
    'website': 'http://www.xetechs.com',
    'depends': ['account','base'],
    'data': ['views/invoice_view.xml'],
    'installable': True,
}
