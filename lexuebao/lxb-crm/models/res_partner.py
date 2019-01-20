# -*- coding: utf-8 -*-
##############################################################################
#
#
#
#
#    主要是学生办理入学时的相关信息
#
#
##############################################################################

from odoo import api,fields,models

class Partner(models.Model):
    _inherit = 'res.partner'

    relation_type=fields.Selection([('parent','学生家长'),('studentself','学生本人')],string='客户类型')
    student_ids=fields.Many2many('lxb.student',string='学生视图信息')
    relation_with_stu=fields.Selection([('father','爸爸'),('mother','妈妈'),('others','其他')],string='与学生关系')
    company_id = fields.Many2one('res.company', '公司', required=True,
                                 default=lambda self: self.env.user.company_id)