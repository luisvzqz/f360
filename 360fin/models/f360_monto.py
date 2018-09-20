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


class F360Monto(models.Model):
    _name = "x_360fin.monto"
    _description = "360fin.monto"

    x_company_id = fields.Many2one(comodel_name="res.company", string="Company id", required=False,
                                     help="Company id")
    x_impacto = fields.Integer('Impacto PLD', default=1, help="Impacto PLD")
    x_max = fields.Float(compute='_compute_x_max', string='Máximo', store=True)
    x_min = fields.Float(compute='_compute_x_min', string='Mínimo', store=True)
    x_name = fields.Char('Monto', required=True, index=True)
    x_partner_id = fields.Many2one(comodel_name="res.partner", string="Partner id", required=False,
                                   help="Partner id")


