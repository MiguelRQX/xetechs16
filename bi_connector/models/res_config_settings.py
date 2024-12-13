# -*- coding: utf-8 -*-

import requests
from odoo import api, models, fields
from odoo.http import request, db_list, db_monodb


class XetechsBISettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # databases = [(db, db) for db in db_list()]

    xetechs_bi_connector_enable = fields.Boolean(string="Enable Xetechs BI Connector", default=False)
    xetechs_bi_uuid = fields.Char(string="Source ID")
    xetechs_bi_secret = fields.Char(string="Secret")
    # xetechs_bi_database = fields.Selection(databases, default=lambda y: db_monodb(), string='Database')
    xetechs_bi_test = fields.Char('Test connection', default='Not tested')

    def test_connection(self, uuid, secret):
        base_url = 'http://localhost:8000'
        params = '/api/sources/connector'
        headers = {'SECRET': secret, 'SOURCEID': uuid}
        db = db_monodb()
        payload = {
            'db': db
        }
        r = requests.post(base_url + params, data=payload, headers=headers)
        return r.json() == db

    @api.model
    def set_values(self):
        res = super(XetechsBISettings, self).set_values()
        uuid = self.xetechs_bi_uuid.strip()
        secret = self.xetechs_bi_secret.strip()
        self.env['ir.config_parameter'].set_param('bi_connector.xetechs_bi_connector_enable',
                                                  self.xetechs_bi_connector_enable)
        self.env['ir.config_parameter'].set_param('bi_connector.xetechs_bi_uuid', uuid)
        self.env['ir.config_parameter'].set_param('bi_connector.xetechs_bi_secret', secret)
        # self.env['ir.config_parameter'].set_param('bi_connector.xetechs_bi_database', self.xetechs_bi_database)
        # self.env['ir.config_parameter'].set_param('bi_connector.xetechs_bi_database', db_monodb())
        # if self.test_connection(uuid, secret):
        #     self.env['ir.config_parameter'].set_param('bi_connector.xetechs_bi_test', 'Connection success')
        # else:
        #     self.env['ir.config_parameter'].set_param('bi_connector.xetechs_bi_test', 'Connection failed')
        return res

    @api.model
    def get_values(self):
        res = super(XetechsBISettings, self).get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        connector_enable = icp_sudo.get_param('bi_connector.xetechs_bi_connector_enable')
        uuid = icp_sudo.get_param('bi_connector.xetechs_bi_uuid')
        secret = icp_sudo.get_param('bi_connector.xetechs_bi_secret')
        # database = icp_sudo.get_param('bi_connector.xetechs_bi_database')
        test = icp_sudo.get_param('bi_connector.xetechs_bi_test')
        res.update(
            xetechs_bi_connector_enable=connector_enable,
            xetechs_bi_uuid=uuid,
            xetechs_bi_secret=secret,
            # xetechs_bi_database=database,
            xetechs_bi_test=test,
        )
        return res

