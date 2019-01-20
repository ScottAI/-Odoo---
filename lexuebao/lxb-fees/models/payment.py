# -*- coding: utf-8 -*-
###############################################################################
#
#    继承修改account.invoice类，开票收款
#
#
#
#
###############################################################################

from odoo import models, fields,api

class LxbPayment(models.Model):
    _inherit = 'account.payment'

    is_deposit = fields.Boolean(string='是否定金',required=True,default=False)
    course_id = fields.Many2one('lxb.course',string='课程')

