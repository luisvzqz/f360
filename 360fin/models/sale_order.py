# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import math

class SaleOrder(models.Model):
    _inherit = "sale.order"

    z_moneda_imp = fields.Integer(related='currency_id.x_impacto', string="Moneda", readonly=1)

    z_credito_is = fields.Boolean(related='product_id.z_credito_is', string="Es un Crédito?", readonly=1)
    z_credito_cod = fields.Char(related='product_id.z_credito_cod', string="Código", readonly=1)

    z_credito = fields.Float(string="Crédito", required=False, help="Crédito a financiar", compute='_calcula_credito', readonly=1)
    z_monto = fields.Float(string="Monto", required=False, help="Monto de crédito")
    z_monto_min = fields.Float(related='product_id.z_monto_min', string="Monto mínimo", help="Monto mínimo")
    z_monto_max = fields.Float(related='product_id.z_monto_max', string="Monto máximo", help="Monto máximo")
    z_monto_iva = fields.Float(string="Monto con IVA", required=False, help="Monto a financiar con IVA", compute='_calcula_monto_iva', readonly=1)

    z_monto_men = fields.Float(related='partner_id.z_monto_men', string="Monto mensual máximo a pagar", required=False, help="Monto mensual máximo a pagar")
    z_monto_efe = fields.Float(related='partner_id.z_monto_efe', string="Monto mensual máximo a pagar en efectivo ", required=False, help="Monto mensual máximo a pagar en efectivo")


    z_tax_id = fields.Many2one(comodel_name="account.tax", string="Impuestos", required=False, help="Impuesto al Valor Agregado")
    z_date = fields.Date(string="Fecha Inicial", help="Fecha inicial de la amortización", default=datetime.now())
    z_plazo = fields.Integer(string="Plazo (meses)", required=False, help="Plazo de pago")

    z_periodo = fields.Selection([('1','Anual'),
                                     ('2','Semestral'),
                                     ('3','Cuatrimestral'),
                                     ('4','Trimestral'),
                                     ('12','Mensual'),
                                     ('24', 'Quincenal'),
                                     ('26', 'Catorcenal'),
                                     ('52', 'Semanal'),],
                                      string="Periodo", required=False, help="Periodos de pago", default='12')
    z_tax_mode = fields.Selection([('0','Impuesto sobre pagos'),
                                   ('1','Impuesto sobre intereses')],
                                    string="Modo pago IVA", required=False, help="Modo del pago de los impuestos", default='0')
    z_tasa_anual = fields.Float(string="Tasa anual", required=False, help="Tasa anual")

    z_tasa = fields.Float(string="Tasa periodo", required=False, help="Tasa del periodo", compute='_calcula_tasa', readonly=1)
    z_pago = fields.Float(string="Pago", required=False, help="Pago", compute='_calcula_pago', readonly=1)
    z_vr = fields.Float(string="Valor Residual", required=False, help="Valor Residual")
    z_n = fields.Float(string="Número de Pagos", required=False, help="Cantidad de pagos de acuerdo al número de periodos", compute='_calcula_n', readonly=1)
    z_interes = fields.Float(string="Interes", required=False, help="Interes", readonly=1)
    z_capital = fields.Float(string="Capital", required=False, help="Capital", readonly=1)
    z_enganche = fields.Float(string="Enganche", required=False, help="Deposito Inicial")
    z_iva = fields.Float(string="IVA", required=False, help="IVA", readonly=1)
    z_operacion = fields.Float(string="Operación", required=False, help="Monto de la operación", compute='_calcula_opera', readonly=1)
    z_operacion_iva = fields.Float(string="Operación c/IVA", required=False, help="Monto de la operación c/IVA", compute='_calcula_opera_iva', readonly=1)
    z_impacto = fields.Integer(related='product_id.z_impacto', string="Producto", required=False, help="Producto")

    z_amortiza = fields.One2many(comodel_name="x_360fin.amortiza", inverse_name="x_order_id", string="Amortización", required=False, help="Amortización")

    @api.depends('z_monto','z_tax_id')
    def _calcula_monto_iva(self):
        for record in self:
            if record.z_tax_id != False:
                iva = record.z_tax_id.amount / 100
            else:
                iva = 0
            record.z_monto_iva = record.z_monto * (1 + iva)

            return record

    @api.depends('z_pago','z_n')
    def _calcula_opera(self):
        for record in self:
            record.z_operacion = (record.z_pago * record.z_n) + record.z_enganche + record.z_vr
            return record

    @api.depends('z_operacion')
    def _calcula_opera_iva(self):
        for record in self:
            if record.z_tax_id != False:
                iva = record.z_tax_id.amount / 100
            else:
                iva = 0
            record.z_operacion_iva = record.z_operacion * (1 + iva)
            return record


    @api.depends('z_monto','z_enganche')
    def _calcula_credito(self):
        for record in self:
            record.z_credito = record.z_monto - record.z_enganche
            return record

    @api.depends('z_plazo','z_periodo')
    def _calcula_n(self):
        for record in self:
            dias = (record.z_plazo * 360) / 12
            periodo = 1
            if record.z_periodo != False:
                periodo = 360 / int(record.z_periodo)
                periodo = math.floor(periodo)
                record.z_n = int(dias / periodo)
                return record
            else:
                record.z_n = record.z_plazo
                return record

    @api.depends('z_credito','z_tasa', 'z_vr','z_n','z_credito_cod')
    def _calcula_pago(self):
        for record in self:
            if self.z_credito_cod == "ARRE":
                credito = self.z_credito
                tasa = self.z_tasa / 100
                num = self.z_n
                if tasa > 0:
                    pago = (credito * tasa * ((1+ tasa)**num) - self.z_vr * tasa) / (((1 + tasa) ** num)-1)
                else:
                    pago = 0
                record.z_pago = pago
                if record.z_pago != False:
                    record.order_line.price_unit = record.z_pago


            return record

    @api.depends('z_tasa_anual','z_periodo','z_tax_id')
    def _calcula_tasa(self):
        for record in self:
            if record.z_periodo != False:
                if record.z_tax_id != False:
                    if record.z_tax_mode == '0':
                        record.z_tasa = (record.z_tasa_anual) / int(record.z_periodo)
                    else:
                        record.z_tasa = (record.z_tasa_anual * (1+(record.z_tax_id.amount / 100))) / int(record.z_periodo)
                else:
                    record.z_tasa = (record.z_tasa_anual) / int(record.z_periodo)
            return record


    @api.multi
    def amortiza(self):
        self.ensure_one()
        for record in self:
            if record.z_date == False:
                record.z_date = datetime.now()

            n = record.z_n
            fecha = record.z_date

            tax_mode = int(record.z_tax_mode)

            periodo = int(record.z_periodo)

            capital_total = 0
            record.z_capital = capital_total

            iva_total = 0
            record.z_iva = iva_total

            interes_total = 0
            record.z_interes = interes_total

            if record.z_tax_id != False:
                iva = record.z_tax_id.amount / 100
            else:
                iva = 0

            amortiza_tabla = self.env['x_360fin.amortiza']

            amortiza_count = 0

            amortiza_count = amortiza_tabla.search_count([('x_order_id', '=', record.id)])

            if amortiza_count > 0:
                amortiza_ele = amortiza_tabla.search([('x_order_id', '=', record.id)])
                for each in amortiza_ele:
                    each.unlink()
            else:
                fecha_ini = datetime.strptime(record.z_date, '%Y-%m-%d')
                saldo_inicial = record.z_monto

                count = 0
                fecha = fecha_ini
                while count <= (n + 1):

                    if periodo == 1:
                        fecha = fecha_ini + relativedelta(years=count)
                    if periodo == 2:
                        fecha = fecha_ini + relativedelta(months=count * 6)
                    if periodo == 3:
                        fecha = fecha_ini + relativedelta(months=count * 4)
                    if periodo == 4:
                        fecha = fecha_ini + relativedelta(months=count * 3)
                    if periodo == 12:
                        fecha = fecha_ini + relativedelta(months=count)
                    if periodo == 24:
                        fecha = fecha_ini + relativedelta(days=count * 15)
                    if periodo == 26:
                        fecha = fecha_ini + relativedelta(weeks=count * 2)
                    if periodo == 52:
                        fecha = fecha_ini + relativedelta(weeks=count)

                    if count == 0:
                        if record.z_enganche != False:
                            pago = record.z_enganche
                            saldo_inicial = record.z_monto
                            interes = 0
                            if tax_mode == 0:
                                    tax = pago * iva
                                    pay_tax = pago + tax
                                    balance_tax = saldo_inicial * (1 + iva)
                                    capital = pago - interes
                            else:
                                    tax = interes * iva
                                    pay_tax = pago
                                    balance_tax = saldo_inicial
                                    capital = pago - interes - tax


                            saldo_final = saldo_inicial - capital
                            balance = saldo_final
                        else:
                            pago = 0
                            saldo_inicial = record.z_monto
                            interes = 0
                            if tax_mode == 0:
                                tax = pago * iva
                                pay_tax = pago + tax
                                balance_tax = saldo_inicial * (1 + iva)
                                capital = pago - interes
                            else:
                                tax = interes * iva
                                pay_tax = pago
                                balance_tax = saldo_inicial
                                capital = pago - interes - tax

                            saldo_final = saldo_inicial - capital
                            balance = saldo_final
                    else:
                        if (count > 0) & (count < (n+1)):
                            pago = record.z_pago

                            if tax_mode == 0:
                                interes = saldo_inicial * (record.z_tasa / 100)
                                tax = pago * iva
                                pay_tax = pago + tax
                                balance_tax = saldo_inicial * (1 + iva)
                                capital = pago - interes
                            else:
                                interes = (saldo_inicial * (record.z_tasa / 100))/(1+iva)
                                tax = interes * iva
                                pay_tax = pago
                                balance_tax = saldo_inicial
                                capital = pago - interes - tax

                            saldo_final = saldo_inicial - capital
                            balance = saldo_final

                            capital_total = capital_total + capital
                            iva_total = iva_total + tax
                            interes_total = interes_total + interes
                        else:
                            pago = 0
                            interes = 0

                            if tax_mode == 0:
                                tax = pago * iva
                                pay_tax = pago + tax
                                balance_tax = saldo_inicial * (1 + iva)
                                capital = pago - interes
                            else:
                                tax = interes * iva
                                pay_tax = pago
                                balance_tax = saldo_inicial
                                capital = pago - interes - tax

                            saldo_final = saldo_inicial
                            balance = saldo_final

                    amortiza_id = amortiza_tabla.create({'x_name': record.client_order_ref,
                                                            'x_order_id': record.id,
                                                            'x_company_id': record.company_id.id,
                                                            'x_partner_id': record.partner_id.id,
                                                            'x_product_id': record.product_id.id,
                                                            'x_opportunity_id': record.opportunity_id.id,
                                                            'x_n': count,
                                                            'x_date': fecha,
                                                            'x_pay': pago,
                                                            'x_loan_ini': saldo_inicial,
                                                            'x_rate': interes ,
                                                            'x_tax': tax,
                                                            'x_capital': capital,
                                                            'x_loan_fin': saldo_final,
                                                            'x_balance': balance,
                                                            'x_pay_tax': pay_tax,
                                                            'x_balance_tax': balance_tax,
                                                            })


                    saldo_inicial = saldo_final
                    count += 1

                record.z_capital = capital_total
                record.z_iva = iva_total
                record.z_interes = interes_total



            return record







