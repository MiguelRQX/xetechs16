
{
    'name': 'Rename field of name',
    'version': '15.0.1.0.0',
    'category': 'Account',
    'license': 'AGPL-3',
    'summary': 'change the field name in title and report of invoice',
    'description': """
CHANGE TITLE AND REPORT
========================

This module only change the field name.

    """,
    'author': 'Xetechs',
    'website': 'http://www.xetechs.com',
    'depends': ['account','base','account_invoice_megaprint'],
    'data': ['views/account.xml','views/report_invoice.xml','views/add_information_fel.xml'],
    'installable': True,
}