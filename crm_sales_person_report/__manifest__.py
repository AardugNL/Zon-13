# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################
{
    'name' : 'CRM Sales Person Activity Report',
    'version' : '13.0.0.1',
    'author' : 'OpenERP SA',
    'category' : 'CRM',
    'description' : """
CRM Sales Team.
====================================
This module shows activity report of the sales person of the sale team.
    """,
    'website': 'https://www.odoo.com',
    'images' : [],
    'depends' : ['base_setup', 'sales_team', 'crm'],
    'data': [
            'security/ir.model.access.csv', 
            'views/crm_sales_person_report.xml', 
            'views/crm_lead_view.xml',
    ],
    'qweb' : [],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
