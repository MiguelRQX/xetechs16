{
    "name": "Helpdesk Stage changes",
    "summary": "Helpdesk Stage changes",
    'author': "Xetechs S.A.",
    "version": "14",
    "category": "CRM",
    "depends": [
        'helpdesk',
        'sale_subscription',
        'helpdesk_timesheet',
        'crm',
        'base',
    ],
    "data": [
        'views/helpdesk_ticket.xml',
        'views/helpdesk_log.xml',
        'views/helpdesk_stage.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}