# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'Sale Quotation Title',
    'version': '15.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Adds a title field on quotations',
    'description': """
Sale Quotation Title
====================

This module only adds a field *quotation_title* on sale.order (to be displayed in report).

    """,
    'author': 'Xetechs',
    'website': 'http://www.xetechs.com',
    'depends': ['sale'],
    'data': ['sale_view.xml','report_saleorder_document_template.xml'],
    'installable': True,
}
