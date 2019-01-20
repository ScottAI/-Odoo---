# -*- coding: utf-8 -*-
###############################################################################
#
#
#WXBizMsgCrypt 使用demo文件
#
#
#
###############################################################################

import json

from odoo import http
from odoo.http import request

from .. import defs
from .base import BaseController
from .base import convert_static_link

import logging

_logger = logging.getLogger(__name__)

class WxxcxCourseSale(http.Controller, BaseController):

    def _course_basic_dict(self,each_courses):

        _dict = {
            "categoryId": each_courses.wxxcx_category_id.id,
            "characteristic": each_courses.characteristic,
            "dateAdd": each_courses.create_date,
            "dateUpdate": each_courses.write_date,
            "id": each_courses.id,
            "logisticsId": 0,
            "minPrice": each_courses.min_price,
            "name": each_courses.enrollment_id.name,
            "numberFav": each_courses.number_fav,
            "numberGoodReputation": each_courses.number_good_reputation,
            "numberOrders": each_courses.sales_count,
            "originalPrice": each_courses.original_price,
            "paixu": each_courses.sequence or 0,
            "pic": each_courses.get_main_image(),
            "recommendStatus": 0 if not each_courses.recommend_status else 1,
            "recommendStatusStr": dict([value for key,value in defs.GoodsRecommendStatus.__dict__.items()
                                        if not key.startswith('__') and not callable(key)])[each_courses.recommend_status],
            "shopId": 0,
            "status": 0 if each_courses.wxxcx_published else 1,
            "statusStr": '上架' if each_courses.wxxcx_published else '下架',
            "stores": 10,
            "userId": each_courses.create_uid.id,
            "views": each_courses.views,
            "weight": 0
        }
        return _dict

    def _course_category_dict(self,category_id):
        _dict = {
            "dateAdd": category_id.create_date,
            "dateUpdate": category_id.write_date,
            "icon": '',
            "id": category_id.id,
            "isUse": category_id.is_use,
            "key": category_id.key,
            "name": category_id.name,
            "paixu": category_id.sort or 0,
            "pid": category_id.pid.id if category_id.pid else 0,
            "type": category_id.category_type,
            "userId": category_id.create_uid.id
        }
        return _dict

    @http.route('/<string:sub_domain>/shop/courses/list', auth='public', methods=['GET'])
    def list(self, sub_domain, categoryId=False, nameLike=False, **kwargs):
        category_id = categoryId
        try:
            ret, entry = self._check_domain(sub_domain)
            if ret: return ret

            domain = [('wxxcx_published', '=', True)]
            if category_id:
                cate_ids = [int(category_id)] + request.env['wxxcx.course.category'].sudo().browse(
                    int(category_id)).child_ids.ids
                domain.append(('wxxcx_category_id', 'in', cate_ids))
            if nameLike:
                domain.append(('name', 'ilike', nameLike))

            course_list = request.env['course.template'].sudo().search(domain)

            if not course_list:
                return self.res_err(404)

            return self.res_ok([self._course_basic_dict(each_goods) for each_goods in course_list])

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, e.message)

    @http.route('/<string:sub_domain>/shop/courses/detail', auth='public', methods=['GET'])
    def detail(self, sub_domain, id=False, **kwargs):
        course_id = id
        try:
            ret, entry = self._check_domain(sub_domain)
            if ret: return ret

            if not course_id:
                return self.res_err(300)

            course = request.env['course.template'].sudo().browse(int(course_id))

            if not course:
                return self.res_err(404)

            if not course.wxxcx_published:
                return self.res_err(404)

            data = {
                "code": 0,
                "data": {
                    "category": self._course_category_dict(course.wxxcx_category_id),
                    "pics": course.get_images(),
                    "content": convert_static_link(request, course.description_wxapp) if course.description_wxapp else '',
                    "basicInfo": self._course_basic_dict(course)
                },
                "msg": "success"
            }
            self.course_info_ext(data, course)

            _logger.info(str(data))
            course.sudo().write({'views': course.views + 1})
            return self.res_ok(data['data'])

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, e.message)

    def course_info_ext(self, data, goods):
        pass

