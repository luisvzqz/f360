# -*- coding: utf-8 -*-

from odoo import api, fields, models

import datetime

class ProductTemplate(models.Model):
    _inherit = "product.template"

    z_riesgo_pro = fields.Float(string="Producto",  required=False, help="Riesgo por Producto")
    z_riesgo_mto = fields.Float(string="Monto", required=False, help="Riesgo por Monto")
    z_riesgo_mon = fields.Float(string="Moneda", required=False, help="Riesgo por Moneda")
    z_riesgo = fields.Float(string="Total", required=False, help="Riesgo Total")
    z_riesgo_rie = fields.Selection([('1','Bajo'),
                                     ('2','Medio'),
                                     ('3','Alto'),],
                                      string="Nivel", required=False, help="Nivel de Riesgo")

    z_moneda_imp = fields.Integer(related='currency_id.x_impacto', string="Moneda", readonly=1)

    z_credito_is = fields.Boolean(string="Es un crédito?", required=False)
    z_credito_tip = fields.Many2one(comodel_name="x_360fin.creditos", string="Tipo de Crédito", required=False, help="Tipo de Crédito")
    z_credito_cod = fields.Char(related='z_credito_tip.x_codigo', string="Código de Crédito", readonly=1)

    z_credito = fields.Float(string="Crédito", required=False, help="Crédito a pedir")
    z_monto_min = fields.Float(string="Monto mínimo", required=False, help="Monto mínimo")
    z_monto_max = fields.Float(string="Monto máximo", required=False, help="Monto máximo")

    z_monto_imp = fields.Integer(string="Monto", required=False, help="Monto impacto de acuerdo a la compañia")

    z_plazo = fields.Integer(string="Plazo", required=False, help="Plazo de pago")
    z_plazo_max = fields.Integer(string="Plazo Máximo", required=False, help="Plazo de pago")
    z_plazo_imp = fields.Integer(string="Plazo", required=False, help="Plazo impacto de acuerdo a la compañia")

    z_periodo = fields.Selection([('1','Anual '),
                                     ('2','Semestral'),
                                     ('3','Cuatrimestral'),
                                     ('4','Trimestral'),
                                     ('12','Mensual'),
                                     ('24', 'Catorcenal'),
                                     ('26', 'Quincenal'),],
                                      string="Periodo", required=False, help="Periodos de pago")
    z_tasa_min = fields.Float(string="Tasa anual mínima", required=False, help="Tasa anual mínima")
    z_tasa_max = fields.Float(string="Tasa anual máxima", required=False, help="Tasa anual máxima")

    z_tasa = fields.Float(string="Tasa", required=False, help="Tasa")
    z_pago = fields.Float(string="Pago", required=False, help="Pago", readonly=1)
    z_vr = fields.Float(string="VR", required=False, help="Valor Residual")
    z_n = fields.Float(string="Número de Pagos", required=False, help="Cantidad de pagos de acuerdo al número de periodos")
    z_interes = fields.Float(string="Interes", required=False, help="Interes")
    z_capital = fields.Float(string="Capital", required=False, help="Capital")
    z_enganche = fields.Float(string="Enganche", required=False, help="Deposito Inicial")
    z_iva = fields.Float(string="IVA", required=False, help="IVA")


    z_aval_is = fields.Boolean(string="Requiere Aval?", required=False)
    z_aval = fields.Many2one(comodel_name="x_360fin.aval", string="Aval", required=False, help="Aval")
    z_aval_imp = fields.Integer(related='z_aval.x_impacto', string="Aval", readonly=1)

    z_cartera = fields.Many2one(comodel_name="x_360fin.cartera", string="Cartera", required=False, help="Cartera")
    z_cartera_imp = fields.Integer(related='z_cartera.x_impacto', string="Cartera", readonly=1)

    z_mercado = fields.Many2one(comodel_name="x_360fin.mercado", string="Mercado", required=False, help="Mercado")
    z_mercado_imp = fields.Integer(related='z_mercado.x_impacto', string="Mercado", readonly=1)


    z_garantia_is = fields.Boolean(string="Requiere Garantía?", required=False)
    z_garantia = fields.Many2one(comodel_name="x_360fin.garantia", string="Garantías", required=False, help="Tipo de garantía")
    z_garantia_imp = fields.Integer(related='z_garantia.x_impacto', string="Garantía", readonly=1)
    z_impacto = fields.Integer(string="Producto", required=False, help="Producto")


    @api.onchange('z_riesgo_pro','z_riesgo_mto','z_riesgo_mon')
    def promedio_change(self):
        self.z_riesgo = (self.z_riesgo_pro + self.z_riesgo_mto + self.z_riesgo_mon ) / 3
        if self.z_riesgo <= 5:
            self.z_riesgo_rie = '1'
        elif self.z_riesgo <= 20:
            self.z_riesgo_rie = '2'
        elif self.z_riesgo > 20:
            self.z_riesgo_rie = '3'

    @api.onchange('z_monto_max')
    def is_monto_change(self):

        montos_num = self.env['x_360fin.monto'].search_count([('x_company_id', '=', self.company_id.id)])

        if montos_num != 0:
            monto = self.env['x_360fin.monto'].search([('x_company_id', '=', self.company_id.id)])

            for each in monto:
                if self.z_monto_max >= each['x_min']:
                    if self.z_monto_max <= each['x_max']:
                        self.z_monto_imp = each['x_impacto']
                        return

    @api.onchange('z_plazo_max')
    def is_plazo_change(self):

        plazos_num = self.env['x_360fin.plazo'].search_count([('x_company_id', '=', self.company_id.id)])

        if plazos_num != 0:
            plazo = self.env['x_360fin.plazo'].search([('x_company_id', '=', self.company_id.id)])

            for each in plazo:
                if self.z_plazo_max >= each['x_min']:
                    if self.z_plazo_max <= each['x_max']:
                        self.z_plazo_imp = each['x_impacto']
                        return

    @api.onchange('z_plazo_imp','z_monto_imp','z_aval_imp','z_garantia_imp','z_cartera_imp','z_mercado_imp','z_moneda_imp')
    def is_impacto_change(self):
        self.z_impacto = int((self.z_plazo_imp + self.z_monto_imp + self.z_aval_imp + self.z_garantia_imp + self.z_cartera_imp + self.z_mercado_imp + self.z_moneda_imp )/7)
        return