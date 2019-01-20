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

class WizardLxbTeacherEmployee(models.TransientModel):
    _name = 'wizard.lxb.teacher.employee'
    _description = "为教师创建雇员和用户"

    user_boolean = fields.Boolean("要同时创建一个用户吗 ?", default=True)

    @api.multi
    def create_employee(self):
        for record in self:
            active_id = self.env.context.get('active_ids', []) or []
            teacher = self.env['lxb.teacher'].browse(active_id)
            teacher.create_employee()
            if record.user_boolean and not teacher.user_id:
                user_group = self.env.ref('lxb-core.group_lxb_teacher')
                self.env['res.users'].create_user(teacher, user_group)
