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


import logging

_logger = logging.getLogger(__name__)

class WxxcxCategory(http.Controller,BaseController):

    @http.route('/<string:sub_domain>/shop/courses/category/all', auth='public', methods=['GET'])
    def all(self,sub_domain):
        ret,entry = self._check_domain(sub_domain)
        if ret:return ret

        try:
            all_category = request.env['wxxcx.course.category'].sudo().search([
                ('is_use','=',True)
            ])
            if not all_category:
                return self.res_err(404)

            data=[
                {
                    "dateAdd":each_category.create_date,
                    "dateUpdate":each_category.write_date,
                    "icon": each_category.get_main_image() if each_category.icon else '',
                    "id": each_category.id,
                    "isUse": each_category.is_use,
                    "key": each_category.key,
                    "level": each_category.level,
                    "name": each_category.name,
                    "paixu": each_category.sort or 0,
                    "pid": each_category.pid.id if each_category.pid else 0,
                    "type": each_category.category_type,
                    "userId": each_category.create_uid.id
                } for each_category in all_category
            ]
            return self.res_ok(data)
        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1,e.message)