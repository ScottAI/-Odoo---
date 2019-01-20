# -*- coding: utf-8 -*-
###############################################################################
#
#
#
#   主要存放学生信息
#
#
#
#
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LxbStudentCourse(models.Model):
    _name = 'lxb.student.course'
    _description = '学生选课信息'

    student_id = fields.Many2one('lxb.student', '学生', ondelete="cascade")
    course_id = fields.Many2one('lxb.course', '课程', required=True)
    schedule_id = fields.Many2one('lxb.schedule', '排约课计划', required=True)
    roll_number = fields.Char('序列号')
    subject_ids = fields.Many2many('lxb.subject', string='科目')

    _sql_constraints = [
        ('unique_name_roll_number_id',
         'unique(roll_number,course_id,schedule_id,student_id)',
         'Roll Number & Student must be unique per schedule!'),
        ('unique_name_roll_number_course_id',
         'unique(roll_number,course_id,schedule_id)',
         'Roll Number must be unique per schedule!'),
        ('unique_name_roll_number_student_id',
         'unique(student_id,course_id,schedule_id)',
         'Student must be unique per schedule!'),
    ]


class LxbStudent(models.Model):
    _name = 'lxb.student'
    _inherits = {'res.partner': 'partner_id'}

    birth_date = fields.Date('Birth Date')

    gender = fields.Selection(
        [('m', '男'), ('f', '女'),
         ('o', '其他')], '性别')
    nationality = fields.Many2one('res.country', '国家')
    emergency_contact = fields.Many2one(
        'res.partner', '紧急联系人')
    class_id = fields.Many2one('lxb.class',string='班级')

    already_partner = fields.Boolean('老学员?')
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    gr_no = fields.Char("学号", size=20,required=True)
    course_detail_ids = fields.One2many('lxb.student.course', 'student_id',
                                        '课程信息')
    company_id = fields.Many2one('res.company', '公司', required=True,
                                 default=lambda self: self.env.user.company_id)


    @api.multi
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "出生日期不可以晚于今天!"))
