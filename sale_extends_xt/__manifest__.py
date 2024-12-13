# -*- coding: utf-8 -*-
{
    'name': "Requerimientos xetechs",
    'summary': """
        Agrega el mantenimiento de alcances, las plantillas de alcances y la posibilidad de agregar
        plantillas en los pedidos de venta""",
    'description': """
        Agrega el mantenimiento de alcances, las plantillas de alcances y la posibilidad de agregar
        plantillas en los pedidos de venta. A su vez al seleccionar las plantillas se rellenan las lineas del detalle
        del alcance en los pedidos de venta.
    """,
    'author': "XETECHS",
    'website': "http://www.xetechs.com",
    'category': 'Customizations',
    'version': '0.1',
    'depends': ['sale_management', 'sale', 'mail', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/documents.xml',
        'views/xtechs_scope_views.xml',
        'views/xtechs_scope_template_views.xml',
        'views/sale_order.xml',
        'reports/web_layout.xml',
        'reports/sale_order_report.xml'
    ],
}
