from odoo import models, fields, api

class subscription_category(models.Model):
    _name = 'subscription.category'
    _description = 'Subscription Category'


    name = fields.Char('Name',required=True)
    description = fields.Text('Description')
    active = fields.Boolean('Active', default=True)

    
    

class subscription(models.Model):
    _inherit = 'sale.subscription'
    category_id = fields.Many2one('subscription.category', string='Categoria',store=True)