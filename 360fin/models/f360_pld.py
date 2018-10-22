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


class F360PLD(models.Model):
    _name = "x_360fin.pld"
    _description = "360fin.pld"

    x_name = fields.Char(string="Nombre", required=True, store=True, index=True, size=0)
    x_password = fields.Char(string="Contraseña", required=True, store=True, copy=True, index=True, size=0, help="Password para https://www.prevenciondelavado.comPassword")
    x_URL = fields.Char(string="URL", store=True, copy=True, index=True, help="URL de prevenciondelavado.com")
