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

class WxxcxBanner(http.Controller, BaseController):

    @http.route('/<string:sub_domain>/banner/list', auth='public', methods=['GET'])
    def list(self, sub_domain, default_banner=True, **kwargs):
        try:
            ret, entry = self._check_domain(sub_domain)
            if ret:return ret

            banner_list = request.env['wxxcx.banner'].sudo().search([
                ('status', '=', True)
            ])

            data = []
            if banner_list:
                data = [
                    {
                        "businessId": each_banner.business_id.id,
                        "dateAdd": each_banner.create_date,
                        "dateUpdate": each_banner.write_date,
                        "id": each_banner.id,
                        "linkUrl": each_banner.link_url or '',
                        "paixu": each_banner.sort or 0,
                        "picUrl": each_banner.get_main_image(),
                        "remark": each_banner.remark or '',
                        "status": 0 if each_banner.status else 1,
                        "statusStr": '显示' if each_banner.status else '不显示',
                        "title": each_banner.title,
                        "type": each_banner.type_mark,
                        "userId": each_banner.create_uid.id
                    } for each_banner in banner_list
                ]

            recommend_goods = request.env(user=1)['course.template'].search([
                ('recommend_status', '=', True),
                ('wxxcx_published', '=', True)
            ], limit=5)

            data += [
                {
                    "goods": True,
                    "businessId": course.id,
                    "dateAdd": course.create_date,
                    "dateUpdate": course.write_date,
                    "id": course.id,
                    "linkUrl": '',
                    "paixu": course.sequence or 0,
                    "picUrl": course.get_main_image(),
                    "remark": '',
                    "status": 0 if course.wxxcx_published else 1,
                    "statusStr": '',
                    "title": course.name,
                    "type": 0,
                    "userId": course.create_uid.id
                } for course in recommend_goods
            ]

            return self.res_ok(data)

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1, e.message)
