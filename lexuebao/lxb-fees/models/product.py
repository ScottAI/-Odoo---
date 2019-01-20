# -*- coding: utf-8 -*-
###############################################################################
#
#    继承修改product.product类，使之能够委托继承原来的product和course
#
#
#
#
###############################################################################

from odoo import models, fields


class LxbProduct(models.Model):
    #_name = 'lxb.product'
    _inherit = 'product.product'
    _description = '产品'

    product_info = fields.Text(string='产品说明',size=100)

