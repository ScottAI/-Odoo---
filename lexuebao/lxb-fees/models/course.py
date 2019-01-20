# -*- coding: utf-8 -*-
##############################################################################
#
#
#
#
#
#
#
#
#
##############################################################################

from odoo import models, fields


class LxbCourse(models.Model):
    _inherit = 'lxb.course'

    fees_term_id = fields.Many2one('lxb.fees.terms', '费用期限')
