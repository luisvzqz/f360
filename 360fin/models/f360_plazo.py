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


class F360Plazo(models.Model):
    _name = "x_360fin.plazo"
    _description = "360fin.plazo"

    x_company_id = fields.Many2one(comodel_name="res.company", string="Company id", required=False,
                                     help="Company id")
    x_impacto = fields.Integer('Impacto PLD', default=1, help="Impacto PLD")
    x_max = fields.Integer('Maximo', default=1, help="Máximo")
    x_min = fields.Integer('Minimo', default=1, help="Mínimo")
    x_name = fields.Char('Plazo', required=True, index=True)
    x_partner_id = fields.Many2one(comodel_name="res.partner", string="Partner id", required=False,
                                   help="Partner id")


