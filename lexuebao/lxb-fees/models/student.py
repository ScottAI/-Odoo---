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

from odoo import models, api


class LxbStudent(models.Model):
    _inherit = 'lxb.student'

    @api.multi
    def action_view_invoice(self):
        '''
        This function returns an action that
        display existing invoices of given student ids and show a invoice"
        '''
        result = self.env.ref('account.action_invoice_tree1')
        id = result and result.id or False
        result = self.env['ir.actions.act_window'].browse(id).read()[0]
        inv_ids = []
        for student in self:
            inv_ids += [invoice.id for invoice in student.invoice_ids]
            result['context'] = {'default_partner_id': student.partner_id.id}
        if len(inv_ids) > 1:
            result['domain'] = \
                "[('id','in',[" + ','.join(map(str, inv_ids)) + "])]"
        else:
            res = self.env.ref('account.invoice_form')
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result
