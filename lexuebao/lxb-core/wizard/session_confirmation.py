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

from odoo import models, api


class SessionConfirmation(models.TransientModel):
    _name = 'session.confirmation'
    _description = 'Wizard for Multiple Session Confirmation'

    @api.multi
    def state_confirmation(self):
        active_ids = self.env.context['active_ids']
        lines = self.env['lxb.schedule.line'].search([('id', 'in', active_ids),
                                               ('state', '=', 'draft')])
        for line in lines:
            line.lecture_confirm()
