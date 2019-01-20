# -*- coding: utf-8 -*-
###############################################################################
#
#
#
#
#
#
#
#
#
###############################################################################

from odoo import models, fields, api


class FeesDetailReportWizard(models.TransientModel):

    """ Admission Analysis Wizard """
    _name = 'fees.detail.report.wizard'

    fees_filter = fields.Selection(
        [('student', 'Student'), ('course', 'Course')], 'Fees Filter',
        required=True)
    student_id = fields.Many2one('lxb.student', 'Student')
    course_id = fields.Many2one('lxb.course', 'Course')

    @api.multi
    def print_report(self):
        data = {}
        if self.fees_filter == 'student':
            data['fees_filter'] = self.fees_filter
            data['student'] = self.student_id.id
        else:
            data['fees_filter'] = self.fees_filter
            data['course'] = self.course_id.id

        report = self.env.ref(
            'lxb-fees.action_report_fees_detail_analysis')
        return report.report_action(self, data=data)
