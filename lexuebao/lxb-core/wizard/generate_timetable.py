# -*- coding: utf-8 -*-
###############################################################################
#
#    T
#
#
#
#
#
#
#
###############################################################################

import calendar
import datetime
import pytz
import time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GenerateSession(models.TransientModel):
    '''
    一旦使用过批量创建功能，将无法在前台删除课程计划，因为generate_time_table会存储管理字段。所以使用ondelete="cascade"
    '''
    _name = 'generate.time.table'
    _description = '批量生成课时计划'
    _rec_name = 'course_id'

    schedule_id = fields.Many2one('lxb.schedule', '排约课计划',ondelete="cascade",
                                  required=True,default=lambda self:self.env.context.get('schedule_id',False))
    course_id = fields.Many2one('lxb.course', '课程', required=True,ondelete="cascade",related='schedule_id.course_id')
    time_table_lines = fields.One2many(
        'gen.time.table.line', 'gen_time_table', '课时表明细行',ondelete="cascade")
    time_table_lines_1 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', '课时表明细行',
        domain=[('day', '=', '0')])
    time_table_lines_2 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', '课时表明细行',
        domain=[('day', '=', '1')])
    time_table_lines_3 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', '课时表明细行',
        domain=[('day', '=', '2')])
    time_table_lines_4 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', '课时表明细行',
        domain=[('day', '=', '3')])
    time_table_lines_5 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', '课时表明细行',
        domain=[('day', '=', '4')])
    time_table_lines_6 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', '课时表明细行',
        domain=[('day', '=', '5')])
    time_table_lines_7 = fields.One2many(
        'gen.time.table.line', 'gen_time_table', '课时表明细行',
        domain=[('day', '=', '6')])
    start_date = fields.Date(
        'Start Date',related='schedule_id.start_date' ,required=True, default=time.strftime('%Y-%m-01'))
    end_date = fields.Date('End Date', required=True,related='schedule_id.end_date')

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        if start_date > end_date:
            raise ValidationError(_("End Date cannot be set before \
            Start Date."))

    @api.onchange('course_id')
    def onchange_course(self):
        if self.schedule_id and self.course_id:
            if self.schedule_id.course_id != self.course_id:
                self.schedule_id = False

    @api.multi
    def act_gen_time_table(self):
        '''
        通过视图调用此方法批量生成课时表
        :return:
        '''
        for session in self:
            start_date = datetime.datetime.strptime(
                session.start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(session.end_date, '%Y-%m-%d')

            for n in range((end_date - start_date).days + 1):
                curr_date = start_date + datetime.timedelta(n)
                for line in session.time_table_lines:
                    if int(line.day) == curr_date.weekday():

                        hour = line.timing_id.hour
                        if line.timing_id.am_pm == 'pm' and int(hour) != 12:
                            hour = int(hour) + 12
                        per_time = '%s:%s:00' % (hour, line.timing_id.minute)
                        final_date = datetime.datetime.strptime(
                            curr_date.strftime('%Y-%m-%d ') +
                            per_time, '%Y-%m-%d %H:%M:%S')
                        local_tz = pytz.timezone(
                            self.env.user.partner_id.tz or 'Asia/Shanghai')
                        local_dt = local_tz.localize(final_date, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                        curr_start_date = datetime.datetime.strptime(
                            utc_dt, "%Y-%m-%d %H:%M:%S")
                        curr_end_date = curr_start_date + datetime.timedelta(
                            hours=line.timing_id.duration)

                        self.env['lxb.schedule.line'].create({
                            'teacher_id': line.teacher_id.id,
                            'subject_id': line.subject_id.id,
                            'course_id': session.course_id.id,
                            'schedule_id': session.schedule_id.id,
                            'timing_id': line.timing_id.id,
                            #'classroom_id': line.classroom_id.id,
                            'start_datetime':
                            curr_start_date.strftime("%Y-%m-%d %H:%M:%S"),
                            'end_datetime':
                            curr_end_date.strftime("%Y-%m-%d %H:%M:%S"),
                            'type': calendar.day_name[int(line.day)],
                        })
            return {'type': 'ir.actions.act_window_close'}


class GenerateSessionLine(models.TransientModel):
    _name = 'gen.time.table.line'
    _description = 'Generate Time Table Lines'
    _rec_name = 'day'

    gen_time_table = fields.Many2one(
        'generate.time.table', '时间表', required=True)
    teacher_id = fields.Many2one('lxb.teacher', '教师', required=True)
    subject_id = fields.Many2one('lxb.subject', '科目', required=True)
    timing_id = fields.Many2one('lxb.timing', '时间轴', required=True)
    #classroom_id = fields.Many2one('op.classroom', 'Classroom')
    day = fields.Selection([
        ('0', calendar.day_name[0]),
        ('1', calendar.day_name[1]),
        ('2', calendar.day_name[2]),
        ('3', calendar.day_name[3]),
        ('4', calendar.day_name[4]),
        ('5', calendar.day_name[5]),
        ('6', calendar.day_name[6]),
    ], 'Day', required=True)
