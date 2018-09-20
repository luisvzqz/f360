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


class F360Aval(models.Model):
    _name = "x_360fin.aval"
    _description = "360fin.aval"

    x_descripcion = fields.Char('Descripcion', required=True, index=True)
    x_impacto = fields.Integer('Impacto PLD', default=1, help="Impacto PLD")
    x_name = fields.Char('Aval', required=True, index=True)