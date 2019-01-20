# -*- coding: utf-8 -*-
###############################################################################
#
#
#    处理课程相关的事宜
#
#
#
###############################################################################

from odoo import models, fields,api

class LxbCourse(models.Model):
    _name = 'lxb.course'

    name = fields.Char('课程名', required=True)
    code = fields.Char('课程编号', size=16, required=True, readonly=True, default=lambda x:('New'))
    parent_id = fields.Many2one('lxb.course', '父计划')
    section = fields.Integer('课时')
    evaluation_type = fields.Selection(
        [('normal', '课后作业'), ('GPA', 'GPA'), ('CWA', 'CWA'), ('CCE', 'CCE')],
        '考核方式', default="normal", required=True)
    subject_ids = fields.Many2many('lxb.subject', string='科目')

    serve_type = fields.Selection([('bycourse','按照机构排课'),('byappoint','学生约课')],'上课方式',default='bycourse',required=True)
    pay_type = fields.Selection([('payfirst','预付费'),('ontime','随学随付'),('other','其他')],'付费方式',default='payfirst',required=True)

    schedule_ids = fields.One2many('lxb.schedule','course_id','排课计划')

    company_id = fields.Many2one('res.company', '公司', required=True,
                                 default=lambda self: self.env.user.company_id)

    @api.model
    def create(self,vals):
        if not vals.get('code'):
            vals['code']=self.env['ir.sequence'].next_by_code('lxb.course')
        return super(LxbCourse,self).create(vals)

    _sql_constraints = [
        ('unique_course_code',
         'unique(code)', '课程编号必须唯一!')]
