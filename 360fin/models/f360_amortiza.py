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


class F360Amortiza(models.Model):
    _name = "x_360fin.amortiza"
    _description = "360fin.amortiza"

    create_date = fields.datetime(string='Created on', store=True, copy=True )
    create_uid = fields.many2one(string='Created by',store=True, copy=True, comodel_name="res.users")
    display_name = fields.Char(string='Display Name', readonly=True) #falta "tamaño"
    id = fields.Integer(string='ID', readonly=True, store=True, copy=True)
    write_date = fields.datetime(string='Last Updated on', store=True, copy=True)
    write_uid = fields.many2one(string='Last Updated by', store=True, copy=True, comodel_name="res.users")

    x_balance = fields.Float(string='Balance', store=True, copy=True, help="Balance")
    x_balance_tax = fields.Float(string='Balance with tax', store=True, copy=True)
    x_capital = fields.Float(string='Payments to Capital', store=True, copy=True)
    x_company_id = fields.Many2one(string='Company id', store=True, copy=True, help="Company id", comodel_name="res.company")
    x_date = fields.Datetime(string='Fecha', store=True, copy=True, help="Fecha")
    x_loan_fin = fields.Float(string='Loan Final', store=True, copy=True, help="Loan Final")
    x_loan_ini = fields.Float(string='Loan Initial', store=True, copy=True, help="Loan Initial")
    x_n = fields.Integer('Number of Payment', default=1, help="Number of payment")
    x_name = fields.Char('Amortiza', required=True, index=True)
    x_opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Código opportunity id", required=False, help="Opportunity id")
    x_order_id = fields.Many2one(comodel_name="sale.order", string="Código order id", required=False,
                                       help="Order id")
    x_partner_id = fields.Many2one(comodel_name="res.partner", string="Código partner id", required=False,
                                 help="Partner id")
    x_pay = fields.Float(compute='_compute_x_pay', required=True, index=True, store=True)
    x_pay_tax = fields.Float(compute='_compute_x_pay_tax', required=True, index=True, store=True)
    x_product_id = fields.Many2one(comodel_name="product.product", string="Código partner id", required=False,
                                 help="Product id")
    x_rate = fields.Float(compute='_compute_x_rate', required=True, index=True, store=True)
    x_tax = fields.Float(compute='_compute_x_tax', required=True, index=True, store=True)
