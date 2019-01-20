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
###############################################################################

from odoo import models, fields,api

class LxbTiming(models.Model):
    _name = 'lxb.timing'
    _description = 'Period'
    _order = 'sequence'

    name = fields.Char('Name', size=16, required=True)

    hour = fields.Selection(
        [('0','0'),('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
         ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
         ('11', '11'), ('12', '12')], '开始时间-钟点', required=True)
    minute = fields.Selection(
        [('00', '00'), ('15', '15'), ('30', '30'), ('45', '45')], '开始时间-分钟',
        required=True)
    duration = fields.Float('课时长度(小时)')

    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], '上午/下午', required=True)

    sequence = fields.Integer('顺序号')


