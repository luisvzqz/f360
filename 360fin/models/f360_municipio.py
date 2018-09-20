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


class F360Municipio(models.Model):
    _name = "x_360fin.municipio"
    _description = "360fin.municipio"

    x_codigo = fields.Char('codigo', required=True, index=True)
    x_municipio = fields.Char('Municipio', required=True, index=True)
    x_name = fields.Char('Municipio', required=True, index=True)
    x_state_id = fields.Many2one(comodel_name="res.country.state", string="State id", required=False,
                                     help="State id")

