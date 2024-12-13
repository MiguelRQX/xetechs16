# -*- encoding: UTF-8 -*-
##############################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2015-Today Xetechs, S.A.
# (<http://www.xetechs.com>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from odoo import _, fields, models, SUPERUSER_ID


class WizardCustomerHours(models.TransientModel):
    _name = "wizard.customer.hours"

    date_from = fields.Date('Desde', required=True)
    date_to = fields.Date('Hasta', required=True)
    company_id = fields.Many2one('res.company', 'Empresa', default=lambda self: self.env.company.id)

    def action_generate_report(self):
        for rec in self:
            data = {
                'model': 'wizard.customer.hours',
                'form': self.read()[0],
                'date_from': rec.date_from,
                'date_to': rec.date_to,
            }
        return self.env.ref('helpdesk_tracker_hours.report_customer_support_pdf').with_context(landscape=True).report_action(self, data=data)

    def send_email(self):
        for rec in self:
            if rec.company_id:
                rec.company_id.send_email()
        return True

