# -*- coding: utf-8 -*-

from odoo import api, fields, models

import urllib.parse
import requests
import datetime
import math

class ResCompany(models.Model):
    _inherit = "res.company"

    z_regulador = fields.Many2one(comodel_name="x_360fin.regulador", string="Organo Regulador", required=False,
                                      help="Organo Regulador de la empresa")
    z_siti_usuario = fields.Char(string="Usuario SITI", required=False, help="Entre el usuario SITI")
    z_siti_password = fields.Char(string="Password SITI", required=False, help="Entre el password SITI")
    z_gpo_fin_is = fields.Boolean(string="Es parte de un Grupo Financiero ?", required=False, help="La empresa pertenece a un grupo financiero ?")

    z_nacionalidad = fields.Many2one(comodel_name="res.country", string="Nacionalidad", required=False, help="País de nacionalidad")
    z_nacionalidad_imp = fields.Integer(related='z_nacionalidad.x_impacto', string="Impacto Nacionalidad", readonly=1)
    z_productos = fields.One2many(comodel_name="product.template", inverse_name="company_id", string="Productos", required=False, help="Productos que ofrece la compañía")
    z_productos_rie = fields.Float(string="Producto Promedio",  required=False, help="Riesgo Promedio de Productos")
    z_ocupacion = fields.Many2one(comodel_name="res.partner.industry", string="Actividad", required=False, help="Ocupación, Profesión, Actividad ó giro del negocio al que se dedique el cliente")
    z_ocupacion_imp = fields.Integer(related='z_ocupacion.x_impacto', string="Impacto Actividad", readonly=1)
    z_ocupacion_cnbv = fields.Char(related='z_ocupacion.x_cnbv', string="CNBV Actividad", readonly=1)
    z_estado_imp = fields.Integer(related='state_id.x_impacto', string="Impacto Estado", readonly=1)
    z_pais_imp = fields.Integer(related='country_id.x_impacto', string="Impacto País", readonly=1)
    z_moneda_imp = fields.Integer(related='currency_id.x_impacto', string="Impacto Moneda", readonly=1)

    z_inicio_ope = fields.Date(string="Inicio de Operaciones", required=False, help="Introduzca fecha del inicio de operaciones")

    z_escrituras = fields.One2many(comodel_name="x_360fin.escrituras", inverse_name="x_company_id", string="Escrituras", required=False, help="Escrituras de la compañía")
    z_monto = fields.One2many(comodel_name="x_360fin.monto", inverse_name="x_company_id", string="Montos", required=False, help="Monto Máximo y Mínimo")
    z_plazo = fields.One2many(comodel_name="x_360fin.plazo", inverse_name="x_company_id", string="Plazo", required=False, help="Plazo Máximo y Mínimo")
    z_prob = fields.One2many(comodel_name="x_360fin.probabilidad", inverse_name="x_company_id", string="Probabilidades", required=False, help="Probabilidad Máximo y Mínimo")
    z_impacto = fields.One2many(comodel_name="x_360fin.impacto", inverse_name="x_company_id", string="Impactos", required=False, help="Nivel de Impacto Máximo y Mínimo")
    z_event = fields.One2many(comodel_name="x_360fin.evento", inverse_name="x_company_id", string="Eventos", required=False, help="Eventos")

    z_empleados = fields.One2many(comodel_name="hr.employee", inverse_name="company_id", string="Empleados",
                              required=False, help="Empleados")
    z_no_employee = fields.Integer(string="Núm Empleados", required=False, help="Cantidad de Empleados", readonly=1)
    z_no_customer = fields.Integer(string="Núm Customers", required=False, help="Cantidad de Clientes", readonly=1)

    z_riesgo_pro = fields.Float(string="Producto",  required=False, help="Riesgo por Producto")
    z_riesgo_loc = fields.Float(string="Localidad", required=False, help="Riesgo por Localidad")
    z_riesgo_mto = fields.Float(string="Monto", required=False, help="Riesgo por Monto")
    z_riesgo_act = fields.Float(string="Actividad", required=False, help="Riesgo por Actividad")
    z_riesgo_mon = fields.Float(string="Moneda", required=False, help="Riesgo por Moneda")
    z_riesgo_per = fields.Float(string="Persona", required=False, help="Riesgo por Tipo de Persona")
    z_riesgo_nac = fields.Float(string="Nacionalidad", required=False, help="Riesgo por Nacionalidad")
    z_riesgo_pai = fields.Float(string="País", required=False, help="Riesgo por País")
    z_riesgo_mer = fields.Float(string="Mercado", required=False, help="Riesgo por Mercado")
    z_riesgo_ins = fields.Float(string="Instrumento Monetario", required=False, help="Riesgo por Instrumento Monetario")
    z_riesgo = fields.Float(string="Total", required=False, help="Riesgo Total", readonly=1)
    z_riesgo_rie = fields.Selection([('1','Bajo'),
                                     ('2','Medio'),
                                     ('3','Alto'),],
                                      string="Nivel", required=False, help="Nivel de Riesgo")

    z_imp_riesgo = fields.Float(string="Riesgo", readonly=1)
    z_imp_evento = fields.Float(string="Eventos", readonly=1)
    z_imp_oper = fields.Float(string="Operativo", readonly=1)
    z_imp_contagio = fields.Float(string="Contagio", readonly=1)
    z_imp_reput = fields.Float(string="Reputacional", readonly=1)
    z_imp_legal = fields.Float(string="Contagio", readonly=1)
    z_imp_prob = fields.Float(string="Probabilidad", readonly=1)


    z_probabilidad = fields.Float(string="Probabilidad", required=False, help="Probabilidad de eventos de riesgo", readonly=1)
    z_evento = fields.Float(string="Eventos", required=False, help="Impacto de eventos de riesgo", readonly=1)

    z_fin_cartera = fields.Float(string="Cartera vigente", required=False, help="Cartera vigente en último trimestre")
    z_fin_vencida = fields.Float(string="Cartera vencida", required=False, help="Cartera vencida en último trimestre")
    z_fin_activos = fields.Float(string="Activos", required=False, help="Total de activos en último trimestre")
    z_fin_pasivos = fields.Float(string="Pasivos", required=False, help="Total de pasivos en último trimestre")
    z_fin_capital = fields.Float(string="Capital", required=False, help="Total de capital contable en último trimestre")
    z_fin_ingreso = fields.Float(string="Ingreso", required=False, help="Total de ingresos en último trimestre")
    z_fin_credito = fields.Float(string="Crédito", required=False, help="Total de ingresos por crédito en último trimestre")
    z_fin_perdida_porc = fields.Float(string="% sobre activos", required=False, help="% sobre activos considerado impacto superior")
    z_fin_perdida = fields.Float(string="Perdida aceptable", required=False, help="Máximo aceptado de perdida", compute='_calcula_perdida', readonly=1)

    z_zip_id = fields.Many2one(comodel_name="x_360fin.zipcode", string="Código Postal", required=False, help="Código Postal")
    z_colonia_id = fields.Many2one(comodel_name="x_360fin.colonia", string="Colonia", required=False, help="Colonia")
    z_municipio_id = fields.Many2one(comodel_name="x_360fin.municipio", string="Municipio", required=False, help="Municipio")
    z_localidad_id = fields.Many2one(comodel_name="x_360fin.localidad", string="Localidad", required=False, help="Localidad/Ciudad")
    z_cnbv = fields.Char(related='z_zip_id.x_cnbv', string="CNBV", help="Código de localidad CNBV", readonly=1)
    z_localidad_imp = fields.Integer(related='z_zip_id.x_impacto', string="Localidad", readonly=1)

    @api.depends('z_fin_activos','z_fin_perdida_porc')
    def _calcula_perdida(self):
        for record in self:
            record.z_fin_perdida =  record.z_fin_activos * (record.z_fin_perdida_porc / 100)
            return record

    @api.multi
    def act_datos(self):
        self.ensure_one()

        employee = self.env['hr.employee']
        employee_num = 0
        employee_num = employee.search_count([('company_id', '=', self.id)])
        if employee_num != 0:
            self.z_no_employee = employee_num
            if employee_num > 1:
                empleados = self.env['x_360fin.probabilidad'].search([('x_company_id', '=', self.id)])
                x = 0
                for each in empleados:
                    each['x_min_employee'] = int(employee_num * x)
                    x = x + 0.2
                    each['x_max_employee'] = int(employee_num * x)
        else:
            self.z_no_employee = 0
        
        customer = self.env['res.partner']
        customer_num = 0
        customer_num = customer.search_count([('company_id', '=', self.id),('customer','=',True)])
        if customer_num != 0:
            self.z_no_customer = customer_num
            if customer_num > 1:
                clientes = self.env['x_360fin.probabilidad'].search([('x_company_id', '=', self.id)])
                x = 0
                for each in clientes:
                    each['x_min_customer'] = int(customer_num * x)
                    x = x + 0.2
                    each['x_max_customer'] = int(customer_num * x)
        else:
            self.z_no_customer = 0

        impacto = self.env['x_360fin.impacto'].search([('x_company_id', '=', self.id)])

        x = 0
        for each in impacto:
            each['x_min'] = self.z_fin_perdida * x
            x = x + 0.2
            each['x_max'] = self.z_fin_perdida * x

        eventos_num = self.env['x_360fin.evento'].search_count([('x_company_id', '=', self.id)])

        if eventos_num != 0:
            eventos = self.env['x_360fin.evento'].search([('x_company_id', '=', self.id)])

            self.z_imp_riesgo = 0
            self.z_imp_evento = 0
            self.z_imp_oper = 0
            self.z_imp_contagio = 0
            self.z_imp_reput = 0
            self.z_imp_legal = 0
            self.z_imp_prob = 0

            for each in eventos:
                self.z_imp_riesgo = self.z_imp_riesgo + each['x_riesgo']
                self.z_imp_evento = self.z_imp_evento + each['x_promedio']
                self.z_imp_oper = self.z_imp_oper + each['x_oper']
                self.z_imp_contagio = self.z_imp_contagio + each['x_contagio']
                self.z_imp_reput = self.z_imp_reput + each['x_reput']
                self.z_imp_legal = self.z_imp_legal + each['x_legal']
                self.z_imp_prob = self.z_imp_prob + each['x_prob']

            self.z_imp_riesgo = self.z_imp_riesgo / eventos_num
            self.z_imp_evento = self.z_imp_evento / eventos_num
            self.z_imp_oper = self.z_imp_oper / eventos_num
            self.z_imp_contagio = self.z_imp_contagio / eventos_num
            self.z_imp_reput = self.z_imp_reput / eventos_num
            self.z_imp_legal = self.z_imp_legal / eventos_num
            self.z_imp_prob = self.z_imp_prob / eventos_num

            self.z_evento = math.ceil(self.z_imp_evento)
            self.z_probabilidad = math.ceil(self.z_imp_prob)

    @api.onchange('z_colonia_id')
    def change_colonia(self):
        if self.z_colonia_id != False:
            self.l10n_mx_edi_colony = self.z_colonia_id.x_codigo

    @api.onchange('z_zip_id')
    def change_zip(self):
        if self.z_zip_id != False:
            self.zip = self.z_zip_id.x_name
            self.state_id = self.z_zip_id.x_state_id
            self.country_id = self.state_id.country_id
            self.z_localidad_id =  self.z_zip_id.x_localidad_id
            self.l10n_mx_edi_locality = self.z_zip_id.x_localidad_id.x_codigo
            self.z_municipio_id = self.z_zip_id.x_municipio_id

            localidad = self.env['res.city']
            loc_is = 0
            loc_is = localidad.search_count([('zipcode', '=', self.zip)])
            if loc_is == 0:
                self.city_id = localidad.create({'name': self.z_zip_id.x_localidad_id.x_name,
                                                 'country_id': self.country_id.id,
                                                 'state_id': self.state_id.id,
                                                 'zipcode': self.zip,
                                                 'x_zip_id': self.z_zip_id.id,
                                                 })
                self.city = self.city_id.name

            self.z_colonia_id = False
            self.l10n_mx_edi_colony = False
            colonia = {}
            colonia['domain'] = {'z_colonia_id': [('x_zipcode_id', '=', self.z_zip_id.x_name)]}
            return colonia

    @api.onchange('z_ind_nac_pais')
    def change_ind_nac_pais(self):
            estado = {}
            estado['domain'] = {'z_ind_nac_estado': [('country_id', '=', self.z_ind_nac_pais.name)]}
            return estado

    @api.onchange('z_com_nacionalidad')
    def change_com_nacionalidad(self):
            estado = {}
            estado['domain'] = {'z_com_estado': [('country_id', '=', self.z_com_nacionalidad.name)]}
            return estado

    @api.onchange('z_riesgo_pro','z_riesgo_loc','z_riesgo_mto','z_riesgo_act', 'z_riesgo_mon','z_riesgo_per','z_riesgo_nac','z_riesgo_mer','z_riesgo_ins')
    def promedio_change(self):
        self.z_riesgo = (self.z_riesgo_pro + self.z_riesgo_loc + self.z_riesgo_mto + self.z_riesgo_act + self.z_riesgo_mon + self.z_riesgo_per + self.z_riesgo_nac +  self.z_riesgo_mer + self.z_riesgo_ins) / 9
        if self.z_riesgo <= 5:
            self.z_riesgo_rie = '1'
        elif self.z_riesgo <= 20:
            self.z_riesgo_rie = '2'
        elif self.z_riesgo > 20:
            self.z_riesgo_rie = '3'



