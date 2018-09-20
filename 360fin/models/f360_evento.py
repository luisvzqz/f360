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


class F360Evento(models.Model):
    _name = "x_360fin.evento"
    _description = "360fin.evento"

    x_company_id = fields.Many2one(comodel_name="res.company", string="Company id", required=False,
                                     help="Company id")
    x_contagio = fields.Integer('Impacto Contagio', default=1, help="Impacto contagio")
    x_legal = fields.Integer('Impacto legal', default=1, help="Impacto legal")
    x_name = fields.Char('Evento', required=True, index=True)
    x_oper = fields.Integer('Impacto Operativo', default=1, help="Impacto Operativo")
    x_partner_id = fields.Many2one(comodel_name="res.partner", string="Partner id", required=False,
                                   help="Partner id")
    x_prob = fields.Integer('Nivel de Probabilidad', default=1, help="Nivel de Probabilidad")
    x_promedio = fields.Float(compute='_compute_x_promedio', string='Promedio Impacto', store=True)
    x_reput = fields.Integer('Impacto Reputacional', default=1, help="Impacto Reputacional")
    x_riesgo = fields.Float(compute='_compute_x_riesgo', string='Riesgo', store=True)

