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


class F360Genero(models.Model):
    _name = "x_360fin.genero"
    _description = "360fin.genero"

    x_codigo = fields.Char('Codigo de sexo', required=True, index=True)
    x_name = fields.Char('Genero', required=True, index=True)