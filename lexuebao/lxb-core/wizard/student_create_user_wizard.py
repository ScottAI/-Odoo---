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
#
###############################################################################

from odoo import models, fields, api


class WizardLxbStudent(models.TransientModel):
    _name = 'wizard.lxb.student'
    _description = "为选中的学生创建用户"

    def _get_students(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []

    student_ids = fields.Many2many(
        'lxb.student', default=_get_students, string='学生')

    @api.multi
    def create_student_user(self):
        user_group = self.env.ref('lxb-core.group_lxb_student')
        active_ids = self.env.context.get('active_ids', []) or []
        records = self.env['lxb.student'].browse(active_ids)
        self.env['res.users'].create_user(records, user_group)
