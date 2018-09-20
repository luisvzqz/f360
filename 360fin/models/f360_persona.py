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


class F360Persona(models.Model):
    _name = "x_360fin.persona"
    _description = "360fin.persona"

    x_codigo = fields.Char('Codigo', required=True, index=True)
    x_grupo = fields.Integer('Grupo de personas', default=1, help="Grupo de personas")
    x_impacto = fields.Integer('Impacto PLD', default=1, help="Impacto PLD")
    x_is_company = fields.Boolean('Es compañía', default=True)
    x_name = fields.Char('Persona', required=True, index=True)