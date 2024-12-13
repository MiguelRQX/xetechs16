
{
    'name': 'Subscription Category',
    'version': '15.0.1.0.0',
    'category': 'Subscription',
    'summary': 'manage and create categories to subscription.',
    'description': """ 
        manage and create categories to subscription.
                    """,
    'author': 'Malek Abushabab',
    'license': 'AGPL-3',
    'depends': ['base','sale','sale_subscription'],
    'data': [
        'security/ir.model.access.csv',
        'views/subscription_view.xml',
        'views/menu_item.xml',
        ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
