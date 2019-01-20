# -*- coding: utf-8 -*-
###############################################################################
#
#    班级
#
#
#
#
###############################################################################

from odoo import models,fields,api

class LxbClass(models.Model):
    _name = 'lxb.class'

    code = fields.Char('班级编号',size=16,required=True,readonly=True,default=lambda x:('_New'))
    name = fields.Char('班级名称',required=True)
    class_advisor = fields.Many2one('lxb.teacher',string='班主任')
    student_no = fields.Integer('学生数',default=0,compute='compute_student_no',readonly=True)
    student_ids = fields.One2many('lxb.student','class_id',string='学生')
    specific_site = fields.Char(size=60,string='具体位置')

    company_id = fields.Many2one('res.company', '公司', required=True,
                                 default=lambda self: self.env.user.company_id)
    schedule_id = fields.Many2one('lxb.schedule','约排课计划')

    @api.model
    def create(self, vals):
        if not vals.get('code') or vals.get('code')=='_New':
            vals['code'] = self.env['ir.sequence'].next_by_code('lxb.class')
        return super(LxbClass, self).create(vals)

    @api.multi
    def compute_student_no(self):
        for record in self:
            record.student_no = record.student_ids.size() if record.student_ids else 0

