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

class FMSBudget(models.Model):
    _name = 'fms.budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'FMS Budget'
    _rec_name = 'project_id'

    project_id = fields.Many2one('project.project',string="Project",track_visibility='onchange')
    amount = fields.Float(string="Amount",track_visibility='onchange')
    state = fields.Selection([
        ('draft','Draft'),
        ('level_1_approval','Level 1 Approval'),
        ('level_2_approval','Level 2 Approval'),
        ('budget_approved','Budget Approved'),
        ('rejected','Rejected')],
        readonly=True,string='State',default='draft',track_visibility='onchange')
    is_group_fms_budget_level = fields.Boolean(compute="_compute_group_fms_budget",readonly=False)

    #Compute method for project manager and access rights.
    @api.depends('is_group_fms_budget_level')
    def _compute_group_fms_budget(self):
        level_1 = self.env.user.has_group('abs_odoo_fms.group_fms_budget_level_1')
        level_2 = self.env.user.has_group('abs_odoo_fms.group_fms_budget_level_2')
        if (level_1 == False and level_2 == False) and (self.env.user == self.project_id.user_id):
            self.is_group_fms_budget_level = True
        else:
            self.is_group_fms_budget_level = False

    def action_budget_request(self):
        if self.state == 'draft':
            self.state = 'level_1_approval'
        if self.state == 'rejected':
            self.state = 'draft'

    def action_budget_rejected(self):
        self.state = 'rejected'

    def action_level_1_approve(self):
        if self.state == 'level_1_approval':
            self.state = 'level_2_approval'

    def action_level_2_approve(self):
        if self.state == 'level_2_approval':
            self.state = 'budget_approved'

    def action_reset_to_draft(self):
        self.state = 'draft'
