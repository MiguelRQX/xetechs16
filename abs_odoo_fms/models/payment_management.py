# -- coding: utf-8 --
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2022-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License ascost_per_hour
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
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from datetime import date
import datetime

#Payment Management Class.
class PaymentManagement(models.Model):
    _name = "payment.management"
    _description = "Payment Management"
    _rec_name = 'name'

    name = fields.Char(string="Payment Management",copy="False",readonly="True",index="True",default="New")
    fms_id = fields.Many2one("res.partner",string='Freelancer Name')
    project_id = fields.Many2one("project.project",string ="Project")
    move_id = fields.Many2one("account.move",string ="Bill Reference")
    amount_claimed = fields.Float(string = "Amount Claimed")
    total_of_hours = fields.Float(string = "Total of Hours")
    actual_amount =  fields.Float(string = "Actual Amount",compute='_compute_actual_amount')
    fms_rating = fields.Selection(selection=[
            ('0', 'Low'),
            ('1', 'Medium'),
            ('2', 'High'),
            ('3', 'Highest'),
        ], string="FMS Rating")
    supporting_documentation_ids = fields.One2many("supporting.documentation",'payment_id',string ="Supporting Documentation")
    bill_count = fields.Integer(string="Vendor Bill",compute='open_vendor_bill_count')
    contract_type = fields.Selection([
        ('fix_cost','Fix Cost'),
        ('hourly_basis','Hourly Basis')],
        string='Contract Type')
    state = fields.Selection([
        ('draft','Draft'),
        ('level_1_approval','Level 1 Approval'),
        ('level_2_approval','Level 2 Approval'),
        ('payment_approved','Payment Approved'),
        ('rejected','Rejected')],
        readonly=True,string='State',default='draft')
    is_fms_budget_level = fields.Boolean(compute="_compute_group_fms_budget_level",readonly=False)

    #compute method for project manager and access rights.
    @api.depends('is_fms_budget_level')
    def _compute_group_fms_budget_level(self):
        level_1 = self.env.user.has_group('abs_odoo_fms.group_fms_budget_level_1')
        level_2 = self.env.user.has_group('abs_odoo_fms.group_fms_budget_level_2')
        if (level_1 == False and level_2 == False) and (self.env.user == self.project_id.user_id):
            self.is_fms_budget_level = True
        else:
            self.is_fms_budget_level = False

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('payment.management')
        return super(PaymentManagement, self).create(vals) 
 
    #compute method for Actual Amount Field. 
    @api.depends('contract_type','total_of_hours','fms_id.cost')
    def _compute_actual_amount(self):
        self.actual_amount = 0.0
        for record in self:
            if record.contract_type == 'hourly_basis' and record.total_of_hours and record.fms_id.cost:
                record.actual_amount = record.total_of_hours * record.fms_id.cost

    @api.constrains('contract_type','amount_claimed')
    def _check_actual_amount(self):
        if self.amount_claimed != self.actual_amount and self.contract_type == 'hourly_basis':
            raise ValidationError("The Amount claimed and actual amount must be equal.")

    #Create a vendor bill.
    def action_create_vendor_bill(self):
        current_date =  date.today()
        product_demo_id = self.env.ref('abs_odoo_fms.product_product_demo')
        vendor_dict = {
                       'payment_management_id':   self.id,
                       'partner_id'           :   self.fms_id.id,
                       'invoice_date'         :   current_date,
                       'move_type'            :   "in_invoice",
                       'invoice_line_ids'     :   [(0, 0, {
                                                           'product_id' : product_demo_id,
                                                            'price_unit' :  self.amount_claimed,
                                                            'analytic_account_id': self.project_id.analytic_account_id.id
                                                  })],
                      }
        if vendor_dict:
            vendor_bill_id = self.env['account.move'].sudo().create(vendor_dict)

    def open_vendor_bill_count(self):
        count = self.env['account.move'].search_count([('payment_management_id','=',self.id),('partner_id','=',self.fms_id.id),('move_type','=',"in_invoice")])
        self.bill_count = count

    def open_vendor_bill(self):
        return {
                'type': 'ir.actions.act_window',
                'name': 'Bills',
                'view_mode': 'tree,form',
                'view-id' : False,
                'res_model':'account.move',
                'domain': [('move_type','=',"in_invoice"),('payment_management_id','=',self.id),('partner_id','=',self.fms_id.id)],
                'context': "{'create': True}"
               }

    def action_reset_to_draft(self):
        self.state = 'draft'

    def action_payment_rejected(self):
        self.state = 'rejected'

    def check_payment_validation(self):
        partner_id = self.env['res.partner'].search([('id','=',self.fms_id.id)])
        if partner_id:
            for record in partner_id:
                if (record.nda_attachment_expiry_date and record.nda_attachment_expiry_date < datetime.date.today()) or (record.non_compete_attachment_expiry_date and record.non_compete_attachment_expiry_date < datetime.date.today()):
                    raise ValidationError("Your FMS Legal Documentation expired, Please renewed.")

        project_id = self.env['project.project'].search([('id','=',self.project_id.id)])
        if project_id:
            for rec in project_id:
                total_amount = (rec.total_payment - self.amount_claimed) + self.amount_claimed
                if rec.total_budget < total_amount:
                    raise ValidationError("You can not pay more than budget.")
                if rec.total_budget == 0.0:
                    raise ValidationError("You do not have budget value.")

    def action_payment_request(self):
        if self.state == 'draft':
            self.check_payment_validation()
            self.state = 'level_1_approval'
        if self.state == 'rejected':
            self.state = 'draft'

    def action_level_1_approve(self):
        if self.state == 'level_1_approval':
            self.check_payment_validation()
            self.state = 'level_2_approval'

    def action_level_2_approve(self):
        if self.state == 'level_2_approval':
            self.check_payment_validation()
            self.state = 'payment_approved'
