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
    'name': "乐学宝-微信小程序",
    'version': '1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    'sequence': 3,
    'summary': "微信小程序""",
    'complexity': "easy",
    'author': 'Scott Liu',
    'website': 'http://www.scott-odoo.com',
    'depends': ['lxb-core','sale','lxb-crm','lxb-admission'],
    'data': [
        'views/parent_menu.xml',
        'views/wxxcx_banner_view.xml',
        'views/wxxcx_config_view.xml',
        'views/wxxcx_payment_view.xml',
        'views/wxxcx_user_view.xml',
        'views/course_template_view.xml',
        'views/wxxcx_course_category_view.xml',
        'security/ir.model.access.csv',
        'data/crm_team_data.xml',
        'data/payment_sequence.xml',
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
