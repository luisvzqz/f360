# -*- coding: utf-8 -*-

from odoo import api, fields, models

import datetime
import math

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    z_moneda_imp = fields.Integer(related='currency_id.x_impacto', string="Moneda", readonly=1)

    z_credito_is = fields.Boolean(related='product_id.z_credito_is', string="Es un Crédito?", readonly=1)
    z_credito_cod = fields.Char(related='product_id.z_credito_cod', string="Código", readonly=1)

    z_credito = fields.Float(string="Crédito", required=False, help="Crédito a pedir")

    z_plazo = fields.Integer(string="Plazo", required=False, help="Plazo de pago")

    z_periodo = fields.Selection([('1','Anual'),
                                     ('2','Semestral'),
                                     ('3','Cuatrimestral'),
                                     ('4','Trimestral'),
                                     ('12','Mensual'),
                                     ('24', 'Catorcenal'),
                                     ('26', 'Quincenal'),],
                                      string="Periodo", required=False, help="Periodos de pago")
    z_tasa = fields.Float(string="Tasa", required=False, help="Tasa")
    z_pago = fields.Float(string="Pago", required=False, help="Pago", readonly=1)
    z_vr = fields.Float(string="VR", required=False, help="Valor Residual")
    z_n = fields.Float(string="Número de Pagos", required=False, help="Cantidad de pagos de acuerdo al número de periodos")
    z_interes = fields.Float(string="Interes", required=False, help="Interes")
    z_capital = fields.Float(string="Capital", required=False, help="Capital")
    z_enganche = fields.Float(string="Enganche", required=False, help="Deposito Inicial")
    z_iva = fields.Float(string="IVA", required=False, help="IVA")

    z_impacto = fields.Integer(related='product_id.z_impacto', string="Producto", required=False, help="Producto")






