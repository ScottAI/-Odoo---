# -*- coding: utf-8 -*-
###############################################################################
#
#    乐学宝-教务中心，配置文件
#
#
#
#
#
#
#
###############################################################################

{
    'name': '乐学宝-教务中心',
    'version': '1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 1,
    'summary': '培训机构教务管理',
    'complexity': "easy",
    'author': 'Scott Liu',
    'website': 'http://www.scott-odoo.com',
    'depends': ['board', 'document', 'hr', 'web', 'website'],
    'data': [
        'wizard/teacher_create_employee_wizard_view.xml',
        'wizard/teacher_create_user_wizard_view.xml',
        'wizard/student_create_user_wizard_view.xml',
        'wizard/generate_timetable_view.xml',
        'wizard/time_table_report.xml',
        'wizard/session_confirmation.xml',
        'security/lxb_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/student_view.xml',
        'views/hr_view.xml',
        'views/course_view.xml',
        'views/schedule_view.xml',
        'views/subject_view.xml',
        'views/teacher_view.xml',
        'views/res_company_view.xml',
        'views/lxb_template.xml',
        'views/website_assets.xml',
        'views/timetable_templates.xml',
        'views/timetable_view.xml',
        'views/timing_view.xml',
        'views/class_view.xml',
        'menu/lxb_core_menu.xml',
        'menu/teacher_menu.xml',
        'menu/student_menu.xml',
        'menu/timetable_menu.xml',
        'menu/class_menu.xml',
        'menu/lxb_system_menu.xml',
    ],
    'demo': [

    ],
    'test': [

    ],
    'css': ['static/src/css/base.css'],
    'qweb': [
        'static/src/xml/base.xml',
        'static/src/xml/dashboard_ext_lexuebao.xml'],
    'js': [],
    'images': [
        'static/description/icon_faculty.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
