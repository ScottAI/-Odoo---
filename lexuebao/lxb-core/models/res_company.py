# -*- coding: utf-8 -*-
###############################################################################
#
#
#    主要存储公司相关信息，是对Odoo公司信息的继承修改
#
#
#
#
#
###############################################################################

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    signature = fields.Binary('Signature')
    accreditation = fields.Text('资格鉴定')
    approval_authority = fields.Text('核准')
    institute_type = fields.Selection([('group','集团总部'),('direct','直营店'),('join','加盟店')],'机构类型')


class ResUsers(models.Model):
    _inherit = "res.users"

    user_line = fields.One2many('lxb.student', 'user_id', 'User Line')
    child_ids = fields.Many2many(
        'res.users', 'res_user_first_rel1',
        'user_id', 'res_user_second_rel1', string='Childs')

    @api.multi
    def create_user(self, records, user_group=None):
        for rec in records:
            if not rec.user_id:
                user_vals = {
                    'name': rec.name,
                    'login': rec.email or rec.name ,
                    'partner_id': rec.partner_id.id
                }
                user_id = self.create(user_vals)
                rec.user_id = user_id
                if user_group:
                    user_group.users = user_group.users + user_id
