
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

    x_balance = fields.Float(compute='_compute_x_balance', required=True, index=True, store=True)
    x_balance_tax = fields.Float(compute='_compute_x_balance_tax', required=True, index=True, store=True)
    x_capital = fields.Float(compute='_compute_x_capital', required=True, index=True, store=True)
    x_company_id = fields.Many2one(comodel_name="res.company", string="Código company id", required=False,
                                   help="Company id")
    x_date = fields.Datetime('Date')
    x_loan_fin = fields.Float(compute='_compute_x_loan_fin', required=True, index=True, store=True)
    x_loan_ini = fields.Float(compute='_compute_x_loan_ini', required=True, index=True, store=True)
    x_n = fields.Integer('Number of Payment', default=1, help="Number of payment")
    x_name = fields.Char('Amortiza', required=True, index=True)
    x_opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Código opportunity id", required=False,
                                   help="Opportunity id")
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
