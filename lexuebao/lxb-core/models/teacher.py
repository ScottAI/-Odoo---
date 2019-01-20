# -*- coding: utf-8 -*-
###############################################################################
#
#
#    主要是老师的信息
#
#
#
#
#
#
#
###############################################################################

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LxbTeacher(models.Model):

    _name = 'lxb.teacher'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one(
        'res.partner', '合作伙伴', required=True, ondelete="cascade")

    birth_date = fields.Date('出生日期', required=True)

    gender = fields.Selection(
        [('male', '男'), ('female', '女')], '性别', required=True)
    nationality = fields.Many2one('res.country', '国家')
    emergency_contact = fields.Many2one(
        'res.partner', '紧急联系人')
    visa_info = fields.Char('银行卡', size=64)
    id_number = fields.Char('ID 卡号', size=64)
    login = fields.Char(
        '登录', related='partner_id.user_id.login', readonly=1)
    last_login = fields.Datetime(
        '最后登录', related='partner_id.user_id.login_date',
        readonly=1)
    emp_id = fields.Many2one('hr.employee', '雇员')
    company_id = fields.Many2one('res.company', '公司', required=True,
                                 default=lambda self: self.env.user.company_id)
    teacher_subject_ids = fields.Many2many('lxb.subject', string='可授科目')
    appointment_ids = fields.Many2many('lxb.appointment',string='约课计划')

    @api.multi
    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "出生日期不可以晚于今天!"))

    @api.multi
    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'gender': record.gender,
                'address_home_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'supplier': True, 'employee': True})
