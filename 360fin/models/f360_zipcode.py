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


class F360Zipcode(models.Model):
    _name = "x_360fin.zipcode"
    _description = "360fin.zipcode"

    x_cnbv = fields.Char('codigo CNBV', required=True, index=True)
    x_impacto = fields.Integer('Impacto PLD', default=1, help="impacto PLD")
    x_localidad = fields.Many2one(comodel_name="x_360fin.localidad", string="Localidad", required=False,
                                 help="Localidad")
    x_municipio = fields.Many2one(comodel_name="x_360fin.municipio", string="Municipio", required=False,
                                 help="Municipio")
    x_name = fields.Char('Zipcode', required=True, index=True)
    x_state_id = fields.Many2one(comodel_name="res.country.state", string="State id", required=False,
                                     help="State id")

