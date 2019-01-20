# -*- coding: utf-8 -*-
###############################################################################
#
#    继承修改account.invoice类，开票收款
#
#
#
#
###############################################################################

from odoo import models, fields,api

class LxbInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    @api.depends('invoice_course_line_ids.class_hours','invoice_course_line_ids.course_id')
    def _compute_total_no(self):
        #按照课程行项目计算总课时数
        self.no_sessions = sum(line.class_hours for line in self.invoice_course_line_ids)

    @api.one
    @api.depends('invoice_course_line_ids.course_id','invoice_course_line_ids.amount_ex',
                 'invoice_course_line_ids.price_subtotal','invoice_course_line_ids.discount',
                 'invoice_course_line_ids.invoice_line_tax_ids', 'company_id')
    def _compute_course_amount(self):
        #计算课程相关的总金额
        round_curr = self.currency_id.round
        self.course_amount_untaxed = sum(line.amount_ex_af for line in self.invoice_course_line_ids)
        self.course_amount_total = sum(line.price_subtotal for line in self.invoice_course_line_ids)
        self.course_amount_tax = sum(line.course_tax for line in self.invoice_course_line_ids)

    @api.one
    @api.depends('invoice_course_line_ids.course_id', 'invoice_course_line_ids.amount_ex',
                 'invoice_course_line_ids.price_subtotal', 'invoice_course_line_ids.discount',
                 'invoice_course_line_ids.invoice_line_tax_ids', 'company_id',
                 'course_amount_untaxed','course_amount_tax','course_amount_total',
                 'invoice_line_ids.discount','invoice_line_ids.invoice_line_tax_ids',
                 'amount_untaxed','amount_tax','amount_total')
    def _compute_lxb_amount(self):
        # 计算本开票的各总金额
        self.lxb_amount_untaxed = self.course_amount_untaxed + self.amount_untaxed
        self.lxb_amount_tax = self.course_amount_tax + self.amount_tax
        self.lxb_amount_total = self.course_amount_total + self.amount_total

    no_sessions = fields.Integer(string='总课时数',compute='_compute_total_no')
    reference_contract = fields.Char(string='参考线下合同编号',size=20)
    invoice_course_line_ids = fields.One2many('lxb.invoice.course.line','invoice_id',sting='课程明细',
                                              readonly=True,states={'draft':[('readonly',False)]},copy=True)

    course_amount_untaxed = fields.Monetary(string='不含税金额',store=True,readonly=True,
                                            compute='_compute_course_amount',track_visibility='always')
    course_amount_tax = fields.Monetary(string='税额',store=True,readonly=True,
                                        compute='_compute_course_amount')
    course_amount_total = fields.Monetary(string='合计',store=True,readonly=True,
                                          compute='_compute_course_amount')

    lxb_amount_untaxed = fields.Monetary(string='不含税总金额', store=True, readonly=True,
                                            compute='_compute_lxb_amount', track_visibility='always')
    lxb_amount_tax = fields.Monetary(string='总税额', store=True, readonly=True,
                                        compute='_compute_lxb_amount')
    lxb_amount_total = fields.Monetary(string='总合计', store=True, readonly=True,
                                          compute='_compute_lxb_amount')

class LxbInvoiceCourseLine(models.Model):
    _name = "lxb.invoice.course.line"
    _inherit = 'account.invoice.line'

    course_id = fields.Many2one('lxb.course',string='课程',ondelete='restrict')
    class_hours = fields.Integer(string='课时数')
    amount_ex = fields.Monetary(string='不含税金额')
    amount_ex_af = fields.Monetary(string='不含税折后金额',store=True,readonly=True,
                                     compute='_compute_subtotal')
    course_desc = fields.Char(string='备注')
    price_subtotal = fields.Monetary(string='含税折后金额',store=True,readonly=True,
                                     compute='_compute_subtotal')
    course_tax = fields.Monetary(string='税额',store=True,readonly=True,
                                 compute='_compute_subtotal')

    @api.one
    @api.depends('course_id','amount_ex','discount','invoice_line_tax_ids')
    def _compute_subtotal(self):
        #计算税后金额
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = self.amount_ex * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, None, 1, None,
                                                          None)
        self.price_subtotal = taxes['total_included'] if taxes else price
        self.course_tax = ((self.price_subtotal-price) if taxes else 0)
        self.amount_ex_af = price

