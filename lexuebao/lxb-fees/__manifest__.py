# -*- coding: utf-8 -*-
###############################################################################
#
#
#
#
#
#
#
#
#
###############################################################################

{
    'name': '乐学宝-费用',
    'version': '1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': '费用管理',
    'complexity': "easy",
    'author': 'Scott Liu',
    'website': 'http://www.scott-odoo.com',
    'depends': ['lxb-core','sale', 'account_invoicing'],
    'data': [
        'wizard/fees_detail_report_wizard_view.xml',
        'views/fees_terms_view.xml',
        'views/student_view.xml',
        'views/course_view.xml',
        'views/invoice_view.xml',
        'views/payment_view.xml',
        'security/fees_security.xml',
        'fees_menu.xml',
        'security/ir.model.access.csv',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
