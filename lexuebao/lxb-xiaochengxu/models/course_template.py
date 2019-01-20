# -*- coding: utf-8 -*-
###############################################################################
#
#
#WXBizMsgCrypt 使用demo文件
#
#
#
###############################################################################

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _name = 'course.template'

    wxxcx_category_id = fields.Many2one('wxxcx.course.category', string='小程序商城分类', ondelete='set null')
    characteristic = fields.Text('商品特色',related="course_id.info")
    recommend_status = fields.Boolean('是否推荐')
    wxxcx_published = fields.Boolean('是否上架', default=True)
    description_wxapp = fields.Html('小程序描述')
    original_price = fields.Float('原始价格', related="course_id.original_price",default=0,store=True)
    present_price = fields.Float('现价', default=0, required=True)
    min_price = fields.Float('最低价', default=0, required=True)
    qty_public_tpl = fields.Integer('库存', default=0)
    number_good_reputation = fields.Integer('好评数', default=0)
    number_fav = fields.Integer('收藏数', default=0)
    views = fields.Integer('浏览量', default=0)
    course_id = fields.Many2one('lxb.course',string='招生信息',required=True)
    name = fields.Char('名称',related="course_id.name",store=True)
    sales_count = fields.Integer('销量',default=0)
    sequence = fields.Integer('序号',default=0)
    image = fields.Binary(string='图片')
    display_pic = fields.Html('图片',compute='_compute_display_pic')

    def get_main_image(self):
        base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return '%s/web/image/course.template/%s/image/300x300'%(base_url, self.id)

    def get_images(self):
        base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        _list = []
        if hasattr(self, 'product_image_ids'):
            for obj in self.product_image_ids:
                _dict = {
                    "id": obj.id,
                    "goodsId": self.id,
                    "pic": '%s/web/image/course.image/%s/image/'%(base_url, obj.id)
                }
                _list.append(_dict)
        else:
            _list.append({
                'id': self.id,
                'goodsId': self.id,
                'pic': '%s/web/image/course.template/%s/image/'%(base_url, self.id)
            })
        return _list

    @api.depends('image')
    def _compute_display_pic(self):
        for each_record in self:
            if each_record.image:
                each_record.display_pic = '''<img src="{pic}" style="max-width:100px;">'''.format(
                    pic=each_record.get_main_image()
                )
            else:
                each_record.display_pic = False

class LxbCourse(models.Model):
    _inherit = "lxb.course"

    qty_public = fields.Integer('库存', default=0, required=True)
    info = fields.Text('商品描述',size='200')
    original_price = fields.Float('原始价格')
    # 字符'property_id1:value_id1,property_id2:value_id2,'
    attr_val_str = fields.Char('课程详情', compute='_compute_attr_val_str',store=True)

    @api.multi
    @api.depends('name','evaluation_type','subject_ids','serve_type','pay_type')
    def _compute_attr_val_str(self):
        for obj in self:
            _str = ''
            attr_val_list = [(key,value) for key,value in obj.__dict__.items() if not key.startswith('__') and not callable(key)]
            for key,value in attr_val_list:
                _str += '%s:%s,'%(key, value)
            obj.attr_val_str = _str

    def get_property_str(self):
        return ', '.join(['%s: %s'%(key, value) for key,value in self.__dict__.items() if not key.startswith('__') and not callable(key)])
