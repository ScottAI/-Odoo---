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
from odoo import models, api, fields, exceptions, _


class LxbFeesTermsLine(models.Model):
    _name = 'lxb.fees.terms.line'
    _rec_name = 'due_days'

    due_days = fields.Integer('Due Days')
    class_hour = fields.Integer('学时数')
    value = fields.Float('Value (%)')
    fees_id = fields.Many2one('lxb.fees.terms', 'Fees')


class LxbFeesTerms(models.Model):
    _name = 'lxb.fees.terms'

    name = fields.Char('Fees Terms', required=True)
    active = fields.Boolean('Active', default=True)
    note = fields.Text('Description')
    company_id = fields.Many2one('res.company', '公司', required=True,
                                 default=lambda self: self.env.user.company_id)
    no_days = fields.Integer('No of Days')
    day_type = fields.Selection([('before', 'Before'), ('after', 'After')],
                                'Type')
    line_ids = fields.One2many('lxb.fees.terms.line', 'fees_id', 'Terms')

    @api.model
    def create(self, vals):
        res = super(LxbFeesTerms, self).create(vals)
        if not res.line_ids:
            raise exceptions.AccessError(_("Fees Terms must be Required!"))
        total = 0.0
        for line in res.line_ids:
            if line.value:
                total += line.value
        if total != 100.0:
            raise exceptions.AccessError(_("Fees terms must be divided \
            as such sum up in 100%"))
        return res
