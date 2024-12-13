# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2022-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
from odoo import api, fields, models, _
# Inherited Class Project
class Project(models.Model):
    _inherit = 'project.project'

    total_budget = fields.Float(string="Total Budget",compute="_amount_all")
    budget_request_count = fields.Integer(compute="get_budget_request_count")
    total_payment = fields.Float(string="Total Payment",compute="_payment_amount_all")
    payment_request_count = fields.Integer(compute="get_payment_request_count")

    @api.depends('total_payment')
    def _payment_amount_all(self):
        for record in self:
            record.total_payment = False
            fms_payment_id = self.env['payment.management'].search([('project_id','=',self.id),('state','in',['payment_approved','level_1_approval','level_2_approval'])])
            if fms_payment_id:
                total = 0.0
                for line in fms_payment_id:
                    total += line.amount_claimed
                record.total_payment += total

    @api.depends('total_budget')
    def _amount_all(self):
        for record in self:
            record.total_budget = False
            fms_budget_id = self.env['fms.budget'].search([('project_id','=',self.id),('state','in',['budget_approved'])])
            if fms_budget_id:
                total = 0.0
                for line in fms_budget_id:
                    total += line.amount
                record.total_budget += total

    def action_view_fms_budget(self):
        budget_request_list = []
        fms_budget_ids = self.env['fms.budget'].search([('project_id','=',self.id),('state','in',['draft','level_1_approval','level_2_approval','budget_approved','rejected'])])
        for fms_budget_id in fms_budget_ids:
            budget_request_list += fms_budget_id.ids
        return {
                 'name': 'Budget Request',
                 'domain': [('id', 'in', budget_request_list)],
                 'view_type': 'list,form',
                 'res_model': 'fms.budget',
                 'view_id': False,
                 'view_mode': 'list,form',
                 'type': 'ir.actions.act_window'
               }

    def action_view_fms_payment(self):
        payment_request_list = []
        fms_payment_ids = self.env['payment.management'].search([('project_id','=',self.id),('state','in',['draft','level_1_approval','level_2_approval','payment_approved','rejected'])])
        for fms_payment_id in fms_payment_ids:
            payment_request_list += fms_payment_id.ids
        return {
                 'name': 'Payment Request',
                 'domain': [('id', 'in', payment_request_list)],
                 'view_type': 'list,form',
                 'res_model': 'payment.management',
                 'view_id': False,
                 'view_mode': 'list,form',
                 'type': 'ir.actions.act_window'
               }

    def get_payment_request_count(self):
        count = self.env['payment.management'].search_count([('project_id','=',self.id),('state','in',['draft','level_1_approval','level_2_approval','payment_approved','rejected'])])
        if count:
            self.payment_request_count = count
        else:
            self.payment_request_count = False

    def get_budget_request_count(self):
        count = self.env['fms.budget'].search_count([('project_id','=',self.id),('state','in',['draft','level_1_approval','level_2_approval','budget_approved','rejected'])])
        if count:
            self.budget_request_count = count
        else:
            self.budget_request_count = False
