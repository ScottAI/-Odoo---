# -*- coding: utf-8 -*-
###############################################################################
#
#
#本文件处理课程表用到的相关route
#
#
#
###############################################################################

import json

from odoo import http,exceptions
from odoo.http import request
from .base import BaseController
from .base import convert_static_link

from .. import defs

import logging

_logger = logging.getLogger(__name__)

class WxxcxTimetable(http.Controller,BaseController):

    def _student_dict(self,each_student):
        _dict = {
            "name":each_student.name,
            "gender":each_student.gender,
            "birthDate":each_student.birth_date,
        }

    def _course_dict(self,each_course):
        _dict = {

        }

    @http.route('/<string:sub_domain>/member/students',auth='public',methods=['GET'])
    def get_students(self,sub_domain,uid=False,**kwargs):
        wxxcx_user_id = uid
        try:
            if not wxxcx_user_id:
                return self.res_err(300)
            ret,entry = self._check_domain(sub_domain)
            if ret:return ret
            wxxcx_user = request.env['wxxcx.user'].sudo().browse(int(wxxcx_user_id))
            if not wxxcx_user or not wxxcx_user.partner_id:
                return self.res_err(404)

            students = request.env['lxb.student'].search([(wxxcx_user.partner_id,'in','res_parterner_ids')])

            data = {
                "code": 0,
                "data":{
                    "students":[
                        {
                            "studentId":each_student.id,
                            "name": each_student.name,
                            "gender": each_student.gender,
                            "birthDate": each_student.birth_date,
                        } for each_student in students
                    ]
                },
            "msg":"success"
            }

            return self.res_ok(data["data"])

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1,e.message)

    @http.route('/<string:sub_domain>/member/courses/timetable',auth='public',methods=['GET'])
    def get_timetable(self,sub_domain,uid=False,student_ids=False,**kwargs):
        user_id = uid
        try:
            if not user_id:
                return  self.res_err(300)
            ret, entry = self._check_domain(sub_domain)
            if ret: return ret

            user = request.env['wxxcx.user'].sudo().browse(int(user_id))

            if not user or not user.partner_id :
                return self.res_err(404)

        except Exception as e:
            _logger.exception(e)
            return self.res_err(-1,e.message)
