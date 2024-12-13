import random

import datetime
import uuid

from odoo.addons.account_invoice_megaprint import numero_a_texto
import base64
import requests
from ast import literal_eval

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_compare, date_utils, email_split, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from collections import defaultdict
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import ast
import json
import re
import warnings

#XML libraries
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, fromstring
from xml.dom import minidom
from odoo.addons.account_invoice_megaprint import cdata
import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'sale.subscription'

    def validate_and_send_invoice(self, invoice):
        self.ensure_one()
        if invoice.state != 'posted':
            invoice._post(False)
        if invoice.move_type in ('out_invoice', 'out_refund') and invoice.journal_id.is_fel == True:
            if not invoice.fel_serie and not invoice.fel_no and not invoice.uuid:
                xml = invoice.generate_xml()
                #raise UserError(('%s') %(xml))
                xml_request = invoice.dte_request(xml_string=xml.decode('utf-8'), type_request='FirmaDocumentoRequest')
                xml_sing = invoice.get_signature(xml_request.decode('utf-8'))
                xml_signed = invoice.dte_request(xml_string=xml_sing, type_request='RegistraDocumentoXMLRequest')
                invoice.register_dte(xml_signed.decode('utf-8'))

        email_context = self.env.context.copy()
        email_context.update({
            'total_amount': invoice.amount_total,
            'email_to': self.partner_id.email,
            'code': self.code,
            'currency': self.pricelist_id.currency_id.name,
            'date_end': self.date,
        })
        _logger.debug("Sending Invoice Mail to %s for subscription %s", self.partner_id.email, self.id)
        self.template_id.invoice_mail_template_id.with_context(email_context).send_mail(invoice.id)
        invoice.is_move_sent = True
        if hasattr(invoice, "attachment_ids") and invoice.attachment_ids:
            invoice._message_set_main_attachment_id([(4, id) for id in invoice.attachment_ids.ids])