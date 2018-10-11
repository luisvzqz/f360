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

    create_date = fields.datetime(string="Created on", store=True, copy=True)
    create_uid = fields.Many2one(string="Created by", store=True, copy=True, comodel_name="res.users")
    display_name = fields.Char(string="Display", readonly=True, size=0)
    id = fields.Integer(string="ID", readonly=True, store=True, copy=True)
    write_date = fields.datetime(string="Last Updated on", store=True, copy=True)
    write_uid = fields.Many2one(string="Last Updated by", store=True, copy=True, comodel_name="res.users")

    x_company_id = fields.Many2one(string="Compañía id", store=True, copy=True, comodel_name="res.company", on_delete=NULL, help="Company id")
    x_contagio = fields.Integer(string="Impacto Contagio", store=True, copy=True, default=1, help="Impacto contagio")
    x_legal = fields.Integer(string="Impacto legal", store=True, copy=True, default=1, help="Impacto legal")
    x_name = fields.Char(string="Evento", store=True, size=0)
    x_oper = fields.Integer(string="Impacto Operativo", store=True, copy=True, default=1, help="Impacto Operativo")
    x_partner_id = fields.Many2one(string="Partner id", store=True, copy=True, comodel_name="res.partner", on_delete=NULL, help="Partner id")
    x_prob = fields.Integer(string="Nivel de Probabilidad", store=True, copy=True, default=1, help="Nivel de Probabilidad")
    x_promedio = fields.Float(string='Promedio Impacto', compute='_compute_x_promedio', readonly=True, store=True, help="Promedio Impacto")
    x_reput = fields.Integer(string="Impacto Reputacional", ,store=True, copy=True, default=1, help="Impacto Reputacional")
    x_riesgo = fields.Float(string='Riesgo',  readonly=True, store=True, compute='_compute_x_riesgo')
