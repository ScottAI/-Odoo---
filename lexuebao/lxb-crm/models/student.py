# -*- coding: utf-8 -*-
###############################################################################
#
#    在学生当中增加客户视图信息
#
#
#
#
#
#
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LxbStudent(models.Model):
    _inherit = 'lxb.student'

    res_parterner_ids=fields.Many2many('res.partner',string='客户视图信息')