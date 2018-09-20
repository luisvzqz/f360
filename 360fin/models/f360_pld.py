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

    x_name = fields.Char('Pld', required=True, index=True)
    x_password = fields.Char('Pld', required=True, index=True, help= "Password")
    x_URL = fields.Char('Pld', required=True, index=True)

