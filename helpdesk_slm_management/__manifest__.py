# -*- coding: utf-8 -*-

{
    'name': 'Helpdesk SLA Management',
    'version': '15',
    'author': 'Xetechs, S.A.',
    'website': 'https://www.xetechs.com', 
    'support': 'Luis Aquino --> laquino@xetechs.com', 
    'category': 'Helpdesk',
    'depends': ['helpdesk', 'sale_subscription', 'helpdesk_timesheet'],
    'summary': 'Helpdesk SLA Managment',
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_invoice_fel_view.xml',
        'views/sla_managment_view.xml',
        'views/account_move_view.xml',
        'views/helpdesk_ticket_view.xml',
        'data/data.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
}
