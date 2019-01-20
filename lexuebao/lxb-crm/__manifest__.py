# -*- coding: utf-8 -*-
##############################################################################
#
#
#
#
#
#
#
#
#
#
##############################################################################

{
    'name': "乐学宝-客户运营中心",
    'version': '1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    'sequence': 3,
    'summary': "客户运营中心""",
    'complexity': "easy",
    'author': 'Scott Liu',
    'website': 'http://www.scott-odoo.com',
    'depends': ['lxb-core','crm'],
    'data': [
        'menu/crm_menu.xml',
        'views/res_partner_view.xml',
        'views/student_view.xml'
    ],
    'demo': [

    ],
    'test': [

    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
