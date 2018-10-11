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


class F360Creditos(models.Model):
    _name = "x_360fin.creditos"
    _description = "360fin.creditos"

    create_date = fields.datetime(string="Created on", store=True, copy=True)
    create_uid = fields.Many2one(string="Created by", store=True, copy=True, comodel_name="res.users")
    display_name = fields.Char(string="Display", readonly=True, size=0)
    id = fields.Integer(string="ID", readonly=True, store=True, copy=True)
    write_date = fields.datetime(string="Last Updated on", store=True, copy=True)
    write_uid = fields.Many2one(string="Last Updated by", store=True, copy=True, comodel_name="res.users")

    x_codigo = fields.Char(string="Código", store=True, copy=True, help="Código", size=5)
    x_descripcion = fields.Char(string="Descripción", store=True, copy=True, help="Descripción", size=0)
    x_impacto = fields.Integer(string="Impacto PLD", store=True, copy=True, help="Impacto PLD")
    x_name = fields.Char(string="Nombre", store=True, size=0)
