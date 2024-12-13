# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2022-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
{
    'name'    : "FMS Module",
    'author'  : 'Ascetic Business Solution',
    'category': 'Accounting/Accounting',
    'summary' : "FMS Module",
    'website' : 'http://www.asceticbs.com',
    'description' : """ """,
    'version' : '15.0.1.0',
    'depends' : ['base','account','project','sign'],
    'license' : 'OPL-1',
    'data'    : [
                 "security/fms_budget_management_security.xml",
                 "security/ir.model.access.csv",
                 "data/product_demo_view.xml",
                 "data/payment_req_seq_view.xml",
                 "data/mail_templates.xml",
                 "wizard/legal_document_sign_views.xml",
                 "views/fms_budget_views.xml",
                 "views/project_views.xml",
                 "views/payment_management_view.xml",
                 "views/res_partner_view.xml",
                 "views/account_move_views.xml",
                ],
    'assets': {},
    'installable' : True,
    'application' : True,
    'auto_install': False,
}
