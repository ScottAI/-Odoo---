# -*- coding: utf-8 -*-
###############################################################################
#
#
#    本类主要是针对课程的排课
#    注意：只有serve_type是bycourse的才会有排课计划，如果是学生约课的则不需要
#
#
#
###############################################################################

import calendar
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LxbSchedule(models.Model):
    _name = 'lxb.schedule'


    @api.model
    def create(self, vals):
        if not vals.get('code'):
            vals['code'] = self.env['ir.sequence'].next_by_code('lxb.schedule')
        return super(LxbSchedule,self).create(vals)

    code = fields.Char('编码', size=16, required=True,readonly=True,default=lambda x:_('New'))
    name = fields.Char('排约课计划名称', size=32, required=True)
    start_date = fields.Date(
        '开始日期', required=True, default=fields.Date.today())
    end_date = fields.Date('结束日期', required=True)
    course_id = fields.Many2one('lxb.course', '课程', required=True)
    company_id = fields.Many2one('res.company', '公司', required=True,readonly=True,
                                 related='course_id.company_id')

    type = fields.Selection([('schedule','排课'),('appointment','约课')],'计划类型',default='schedule',
                            required=True,compute='generate_shchedule_type')

    #给出具体科目的详细排课计划
    schedule_line_ids = fields.One2many('lxb.schedule.line','schedule_id','时间表')
    appointment_ids = fields.One2many('lxb.appointment','schedule_id','约课表')
    timetable_lines_no = fields.Integer(compute='_compute_lines_no')
    company_id = fields.Many2one('res.company', '公司', required=True,readonly=True,
                                 default=lambda self: self.env.user.company_id)
    #增加班级，计划可以是针对多个班级
    #class_ids = fields.One2many(comodel_name='lxb.class',inverse_name='schedule_id',string='班级')


    _sql_constraints = [
        ('unique_schedule_code',
         'unique(code)', 'Code should be unique per schedule!')]


    @api.one
    @api.depends('course_id')
    def generate_shchedule_type(self):
     #根据课程类型确定计划类型
        if self.course_id and self.course_id.serve_type:
                if self.course_id.serve_type == 'bycourse':
                    self.type = 'schedule'
                elif self.course_id.serve_type == 'byappoint':
                    self.type = 'appointment'
        return self.type


    @api.multi
    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        for record in self:
            start_date = fields.Date.from_string(record.start_date)
            end_date = fields.Date.from_string(record.end_date)
            if start_date > end_date:
                raise ValidationError(_("End Date cannot be set before \
                Start Date."))

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_parent_schedule', False):
            lst = []
            lst.append(self.env.context.get('course_id'))
            courses = self.env['lxb.course'].browse(lst)
            while courses.parent_id:
                lst.append(courses.parent_id.id)
                courses = courses.parent_id
            schedules = self.env['lxb.schedule'].search([('course_id', 'in', lst)])
            return schedules.name_get()
        return super(LxbSchedule, self).name_search(
            name, args, operator=operator, limit=limit)

    @api.multi
    def action_view_timetable(self):
        '''
        根据排约课计划展示计划明细，通过智能按钮触发
        :return:
        '''
        result = self.env.ref('lxb-core.act_open_lxb_session_view')
        id = result and result.id or False
        if self.env['ir.actions.act_window'].browse(id):
            result = self.env['ir.actions.act_window'].browse(id).read()[0]
        line_ids = []
        for schedule in self:
            line_ids += [line.id for line in schedule.schedule_line_ids]
        if len(line_ids)>1:
            result['domain'] = \
                "[('id','in',["+','.join(map(str,line_ids))+"])]"
        else:
            res = self.env.ref('lxb-core.view_lxb_session_form')
            result['views'] = [(res and res.id or False,'form')]
        return result

    @api.multi
    def _compute_lines_no(self):
        self.timetable_lines_no = len(self.schedule_line_ids)
        return len(self.schedule_line_ids)


class LxbAppointment(models.Model):
    _name = 'lxb.appointment'
    _description = '约课'

    name = fields.Char(compute='_compute_name', string='名称', store=True)
    timing_id = fields.Many2one(
        'lxb.timing', '时间轴', required=True, track_visibility="onchange")
    start_datetime = fields.Datetime('开始时间', required=True,
                                     default=lambda self: fields.Datetime.now())
    end_datetime = fields.Datetime('结束时间', required=True)
    teacher_ids = fields.Many2many('lxb.teacher',string='教师')
    schedule_id = fields.Many2one('lxb.schedule', '排约课计划',
                                  required=True)
    company_id = fields.Many2one('res.company', '公司', required=True,
                                 related='schedule_id.company_id')
    subject_id = fields.Many2one('lxb.subject', '科目', required=True,
                                 help="请选择科目")
    #avalable_class_ids = fields.One2many(related='schedule_id.class_ids',string='面向班级',store=True)

    @api.multi
    @api.depends('timing_id', 'start_datetime')
    def _compute_name(self):
        for line in self:
            if line.subject_id  \
                    and line.start_datetime:
                line.name = line.subject_id.name + ':' + \
                            + str(line.timing_id.name)

#是不是再做一个虚拟班级或者虚拟组，用来记录学生和约课的关系？还是修改排约课
#计划，增加student_ids字段




class LxbScheduleLine(models.Model):
    _name = 'lxb.schedule.line'
    _inherit = ['mail.thread']
    _description = '排约课明细'
    _rec_name = 'name'

    @api.multi
    @api.constrains('subject_id','schedule_id')
    def check_subject(self):
    # 检查科目是否属于课程
       if(self.subject_id not in self.schedule_id.course_id.subject_ids):
           raise ValidationError(('''科目%s不属于课程计划%s''')%(self.subject_id.name,
                                                       self.schedule_id.name))
    @api.multi
    @api.constrains('subject_id','teacher_id')
    def check_teacher(self):
        #检查教师是否可以进行对应科目的授课
        if(self.subject_id not in self.teacher_id.teacher_subject_ids):
            raise ValidationError(('''教师%s不可以进行科目%s的授课''')%(self.teacher_id.name,
                                                            self.subject_id.name))

    @api.constrains('start_datetime', 'end_datetime')
    def _check_date_time(self):
        if self.start_datetime > self.end_datetime:
            raise ValidationError(_(
                'End Time cannot be set before Start Time.'))

    @api.multi
    @api.depends('teacher_id', 'subject_id', 'start_datetime')
    def _compute_name(self):
        for line in self:
            if line.teacher_id and line.subject_id \
                    and line.start_datetime:
                line.name = line.teacher_id.name + ':' + \
                               line.subject_id.name + ':' + str(line.timing_id.name)

    @api.multi
    @api.depends('start_datetime')
    def _compute_day(self):
        for record in self:
            record.type = fields.Datetime.from_string(
                record.start_datetime).strftime("%A")

    name = fields.Char(compute='_compute_name',string='名称',store=True)
    timing_id = fields.Many2one(
        'lxb.timing', '时间轴', required=True, track_visibility="onchange")
    start_datetime = fields.Datetime('开始时间', required=True,
                                 default=lambda self:fields.Datetime.now())
    end_datetime = fields.Datetime('结束时间', required=True)
    teacher_id = fields.Many2one('lxb.teacher','教师',required=True,
                                 help="请选择教师")
    schedule_id = fields.Many2one('lxb.schedule', '排约课计划',
                                  required=True)
    company_id = fields.Many2one('res.company', '公司', required=True,
                                 related='schedule_id.company_id')
    subject_id = fields.Many2one('lxb.subject','科目',required=True,
                                 help="请选择科目")
    color=fields.Integer('颜色索引')
    type=fields.Char(compute='_compute_day',string='天',store=True)
    state = fields.Selection(
        [('draft', '草稿'), ('confirm', '已确认'),
         ('done', '已完成'), ('cancel', '已取消')],
        'Status', default='draft')
    user_ids = fields.Many2many(
        'res.users', compute='_compute_schedule_users',
        store=True, string='Users')
    course_id = fields.Many2one('lxb.course',related='schedule_id.course_id')
    #class_ids = fields.One2many(related='schedule_id.class_ids',string='班级',store=True)
    # For record rule on student and faculty dashboard
    @api.multi
    @api.depends('schedule_id', 'teacher_id', 'user_ids.child_ids')
    def _compute_schedule_users(self):
        student_obj = self.env['lxb.student']
        users_obj = self.env['res.users']
        for line in self:
            student_ids = student_obj.search(
                [('course_detail_ids.schedule_id', '=', line.schedule_id.id)])
            user_list = [student_id.user_id.id for student_id
                         in student_ids if student_id.user_id]
            if line.teacher_id.user_id:
                user_list.append(line.teacher_id.user_id.id)
            user_ids = users_obj.search([('child_ids', 'in', user_list)])
            if user_ids:
                user_list.extend(user_ids.ids)
            line.user_ids = user_list

    @api.multi
    def lecture_draft(self):
        self.state = 'draft'

    @api.multi
    def lecture_confirm(self):
        self.state = 'confirm'

    @api.multi
    def lecture_done(self):
        self.state = 'done'

    @api.multi
    def lecture_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, values):
        res = super(LxbScheduleLine, self).create(values)
        mfids = res.message_follower_ids
        partner_val = []
        partner_ids = []
        for val in mfids:
            partner_val.append(val.partner_id.id)
        if res.teacher_id and res.teacher_id.user_id:
            partner_ids.append(res.teacher_id.user_id.partner_id.id)
        if res.schedule_id and res.course_id:
            course_val = self.env['lxb.student.course'].search([
                ('schedule_id', '=', res.schedule_id.id),
                ('course_id', '=', res.course_id.id)
            ])
            for val in course_val:
                if val.student_id.user_id:
                    partner_ids.append(val.student_id.user_id.partner_id.id)
        subtype_id = self.env['mail.message.subtype'].sudo().search([
            ('name', '=', 'Discussions')])
        if partner_ids and subtype_id:
            for partner in partner_ids:
                if partner in partner_val:
                    continue
                val = self.env['mail.followers'].sudo().create({
                    'res_model': res._name,
                    'res_id': res.id,
                    'partner_id': partner,
                    'subtype_ids': [[6, 0, [subtype_id[0].id]]]
                })
        return res

    @api.onchange('course_id')
    def onchange_course(self):
        self.schedule_id = False

    @api.multi
    def notify_user(self):
        for session in self:
            template = self.env.ref(
                'lxb-core.session_details_changes',
                raise_if_not_found=False)
            template.send_mail(session.id)

    @api.multi
    def get_emails(self, follower_ids):
        email_ids = ''
        for user in follower_ids:
            if email_ids:
                email_ids = email_ids + ',' + str(user.sudo().partner_id.email)
            else:
                email_ids = str(user.sudo().partner_id.email)
        return email_ids

    @api.multi
    def get_subject(self):
        return 'lacture of ' + self.teacher_id.name + \
               ' for ' + self.subject_id.name + ' is ' + self.state

    @api.multi
    @api.model
    def write(self, vals):
        data = super(LxbScheduleLine,
                     self.with_context(check_move_validity=False)).write(vals)
        if self.state not in ('draft', 'done'):
            self.notify_user()
        return data