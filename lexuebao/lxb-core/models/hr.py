# -*- coding: utf-8 -*-
###############################################################################
#
#
#    主要存储公司雇员的相关信息
#
#
#
#
#
#
#
###############################################################################

from odoo import models, api,fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    teacher_ids = fields.One2many('lxb.teacher','emp_id',string='教师')
    @api.onchange('user_id')
    def onchange_user(self):
        if self.user_id:
            self.user_id.partner_id.supplier = True
            self.work_email = self.user_id.email
            self.company_id = self.user_id.company_id
            self.identification_id = False

    @api.onchange('address_id')
    def onchange_address_id(self):
        if self.address_id:
            self.work_phone = self.address_id.phone
            self.mobile_phone = self.address_id.mobile
