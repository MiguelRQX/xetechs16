# -*- coding: utf-8 -*-

{
    'name': 'Megaprint PAF',
    'version': '1.0.1',
    'author': 'Xetechs, S.A.',
    'website': 'https://www.xetechs.com', 
    'support': 'Luis Aquino --> laquino@xetechs.com', 
    'category': 'Accounting',
    'depends': ['account'],
    'summary': 'Megaprint PAF',
    'data': [
        'data/data.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/menuitem.xml',
        'views/res_config_settings_view.xml',
        'views/dte_type_view.xml',
        'views/contract_paf_view.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
