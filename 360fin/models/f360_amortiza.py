
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

    create_date = fields.datetime(string="Created on", store=True, copy=True)
    create_uid = fields.Many2one(string="Created by", store=True, copy=True, comodel_name='res.users')
    display_name = fields.Char(string="Display Name", readonly=True, size=0)
    id = fields.Integer(string="ID", readonly=True, store=True, copy=True)
    write_date = fields.datetime(string="Last Updated on", store=True, copy=True)
    write_uid = fields.Many2one(string="Last Updated by", store=True, copy=True, comodel_name='res.users')

    x_balance = fields.Float(string="Balance", compute='_compute_x_balance', store=True, copy=True)
    x_balance_tax = fields.Float(string="Balance with tax", compute='_compute_x_balance_tax', store=True, copy=True, help="Balance with tax")
    x_capital = fields.Float(string="Capital", compute='_compute_x_capital', index=True, store=True, copy=True, help="Payments to Capital")
    x_company_id = fields.Many2one(string="Company id", store=True, copy=True, help="Company id", comodel_name="res.company", on_delete=4)
    x_date = fields.Datetime(string="Date", store=True, copy=True, help="Fecha")
    x_loan_fin = fields.Float(string="Loan Final", compute='_compute_x_loan_fin', store=True, copy=True, help="Loan Final")
    x_loan_ini = fields.Float(string="Loan Initial", compute='_compute_x_loan_ini', store=True, copy=True, help="Loan Initial")
    x_n = fields.Integer(String="Number of Payment", store=True, copy=True, default=1, help="Number of payment")
    x_name = fields.Char(string="Name", store=True, size=0)
    x_opportunity_id = fields.Many2one(string="Opportunity id", store=True, copy=True, comodel_name='crm.lead', on_delete=False, help="Opportunity id")
    x_order_id = fields.Many2one(string="Order id", required=False, comodel_name="sale.order", on_delete=False, domain="[]", help="Order id")
    x_partner_id = fields.Many2one(string="Código partner id", store=True, copy=True, comodel_name="res.partner", domain="[]", on_delete=False, help="Partner id")
    x_pay = fields.Float(string="Payment", store=True, copy=True, compute='_compute_x_pay', help="Payment")
    x_pay_tax = fields.Float(string="Pay with Tax", compute='_compute_x_pay_tax', store=True, copy=True, help="pay with tax")
    x_product_id = fields.Many2one(string="Product id", store=True, copy=True, help="Product id", comodel_name='product.product', domain="[]", on_delete=False)
    x_rate = fields.Float(string="Rate", store=True, copy=True, compute='_compute_x_rate', help="Interest rate")
    x_tax = fields.Float(string="Tax", store=True, copy=True, compute='_compute_x_tax', help="Tax Amount")
