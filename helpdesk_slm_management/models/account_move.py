# -*- coding: utf-8 -*-


from odoo import fields, models, api
from odoo.exceptions import UserError, Warning
import time
from datetime import datetime
from dateutil import relativedelta


class AccountMove(models.Model):
    _inherit = "account.move"

    sla_id = fields.Many2one('sla.contract', 'Contrato FEL', required=False, copy=False)
