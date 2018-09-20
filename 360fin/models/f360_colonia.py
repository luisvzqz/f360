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


class F360Colonia(models.Model):
    _name = "x_360fin.colonia"
    _description = "360fin.colonia"


    x_name = fields.Char('Name', required=True, index=True)
    x_zipcode_id = fields.Many2one(comodel_name="x_360fin.zipcode", string="Código zip id", required=False,
                                     help="Código zip id")
    x_colonia = fields.Char('Colonia', required=True, index=True)
    x_codigo = fields.Char('Codigo', required=True, index=True)

