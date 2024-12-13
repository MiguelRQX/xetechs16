# -*- coding: utf-8 -*-
import re
from odoo import api, models, fields
class Account_Invoice(models.Model):
    _inherit = 'account.move'
    partner_fel = fields.Char(string= '',compute= 'find_customer_fel')
    street_receptor = fields.Char(string= '',compute= 'find_street_fel')
    zip_code_receptor = fields.Char(string= '',compute= 'find_zip_code')
    country_receptor = fields.Char(string= '',compute= 'find_country_fel')
    partner_name_invoice = fields.Char(string= "Nombre Factura: ",help= '''
    Persona u Organización a quien se le esta facturando.
    Si no se coloca información en este campo,
    por defecto tomara el valor de la respuesta
    que envia FEL, al no existir ninguna de las
    anteriores, tomara el nombre del contacto 
    que se encuentra en Odoo.''')

    #Function Partner FEL, response of SAT.
    @api.depends("xml_response","partner_id","partner_name_invoice")
    def find_customer_fel(self):
        for invoice in self:
            if invoice.xml_response:
                text = str(invoice.xml_response)
                t = text.split("&lt;/dte:DireccionEmisor&gt;")
                match = re.search('W*NombreReceptor=*"*\D*""*',t[1])
                search = match.group()
                partner = search.split('=')
                partner_f = partner[1].strip('"')
                invoice.update({'partner_fel': partner_f})
            elif invoice.partner_name_invoice:
                 invoice.update({'partner_fel' : invoice.partner_name_invoice})
            else:
                invoice.update({'partner_fel': invoice.partner_id.name})

    #Function Partner Street
    @api.depends('xml_response','partner_id')
    def find_street_fel(self):
        for invoice in self:
            if invoice.xml_response:
                text = str(invoice.xml_response)
                t = text.split("&lt;/dte:DireccionEmisor&gt;")
                street_match = re.search('W*Direccion&gt;\W*\w.*<*',t[1])
                street = street_match.group()
                street = street.split('&lt')
                street = street[0].split(';')
                street = street[1].strip(' ,')
                street_fish = street
                invoice.update({'street_receptor': street_fish})
            else:
                invoice.update({'street_receptor' : invoice.partner_id.street})
    
    #Funcion Partner ZIP CODE
    @api.depends('partner_id')
    def find_zip_code(self):
        for invoice in self:
            if invoice.partner_id.zip:
               invoice.update({'zip_code_receptor' : invoice.partner_id.zip})
            else:
                invoice.update({'zip_code_receptor' : ''})
    #Funcion Partner Country
    @api.depends('partner_id')
    def find_country_fel(self):
        for invoice in self:      
            if invoice.partner_id.country_id:
                invoice.update({'country_receptor' : invoice.partner_id.country_id.name})
            else:
                invoice.update({'country_receptor' : ''})