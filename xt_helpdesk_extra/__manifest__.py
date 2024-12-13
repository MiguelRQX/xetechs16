# -*- coding: utf-8 -*-
{
    'name': "HelpDesk extras",
    'author':  'XETECHS GT',
	'website': 'https://www.xetechs.com',
    'category': 'Services/Helpdesk',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk'],

    # always loaded
    'data': [
        'views/helpdesk_ticket_view.xml',
    ]
}