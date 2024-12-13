
{
    'name': 'DropDawn CRM name',
    'category': 'Crm',
    'summary': 'List of CRM name',
    'version': '15.0.1.0.0',
    'description': """
    Dropdawn para el campo de name en el CRM
    """,
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead.xml',
        'views/res_list_crm_name.xml',
    ],
    'installable': True,
    'auto_install': False,
}
