# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import email_re, email_split
from odoo.exceptions import UserError, AccessError


_logger = logging.getLogger(__name__)


class F360Escrituras(models.Model):
    _name = "x_360fin.escrituras"
    _description = "360fin.escrituras"

    x_name = fields.Char('Nombre', required=True, index=True)
    x_company_id = fields.Many2one(comodel_name="res.company", string="Compañía", required=False, help="Compañía")
    x_partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, help="Asociado/Cliente")
    x_doc = fields.Binary(string="Documento", help="Copia documento")
    x_fedatario = fields.Char(string="Fedatario", required=False, help="Fedatario")
    x_folio = fields.Char(string="Folio", required=False, help="Folio")
    x_tipo = fields.Selection([('1','Acta Constitutiva'),
                                     ('2','Poder Legal'),
                                     ('3','Cambio denominación'),
                                     ('4','Reforma Estatutos'),],
                                      string="Tipo documento", required=False, help="Tipo de documento a registrar")
