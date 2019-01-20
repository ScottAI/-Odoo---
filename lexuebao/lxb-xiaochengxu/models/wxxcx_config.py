# -*- coding: utf-8 -*-
###############################################################################
#
#
#
#
#
#
###############################################################################

from odoo import models,fields,api

class WxxcxConfig(models.Model):
    _name = 'wxxcx.config'
    _description = u'对接配置'
    _rec_name = 'org_name'

    sub_domain = fields.Char('小程序接口前缀', help='小程序访问的接口url前缀', index=True, required=True)
    org_name = fields.Char('机构名称', help='显示在小程序顶部')

    app_id = fields.Char('appid')
    secret = fields.Char('secret')

    wechat_pay_id = fields.Char('微信支付商户号')
    wechat_pay_secret = fields.Char('微信支付商户秘钥')

    team_id = fields.Many2one('crm.team', string='所属销售渠道', required=True)

    @api.model
    def get_config(self, key, uid=False, obj=False):
        config = self.search([('create_uid', '=', uid)])
        if obj:
            return config

        if config:
            config.ensure_one()
            return config.__getattribute__(key) if not isinstance(config.__getattribute__(key),models.Model) \
                else config.get_relative_field_val(key)
        else:
            return False

    @api.model
    def get_config_by_subdomain(self, key, sub_domain=False, obj=False):
        config = self.search([('sub_domain', '=', sub_domain)])
        if obj:
            return config

        if config:
            config.ensure_one()
            return config.__getattribute__(key) if not isinstance(config.__getattribute__(key), models.Model) \
                else config.get_relative_field_val(key)
        else:
            return False

    @api.model
    def get_from_team(self, team_id):
        config = self.search([('team_id', '=', team_id)])
        if config:
            config.ensure_one()
            return config
        else:
            return False