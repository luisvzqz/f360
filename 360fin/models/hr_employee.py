# -*- coding: utf-8 -*-

from odoo import api, fields, models

import urllib.parse
import requests
import datetime

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    z_nombre = fields.Char(string="Nombres(s)", required=False, help="Nombres de la persona física" )
    z_paterno = fields.Char(string="Apellido Paterno", required=False, help="Introduzca Apellido Paterno")
    z_materno = fields.Char(string="Apellido Materno", required=False, help="Introduzca Apellido Materno")
    z_riesgo_neg = fields.Selection([('1', 'No Encontrado'),
                                     ('2', 'PEP'),
                                     ('3', 'Alto'), ],
                                    string="Nivel de Lista Negra", required=False, help="Nivel de Lista Negra")
    z_lista_negra = fields.One2many(comodel_name="x_360fin.lista_negra", inverse_name="x_employee_id", string="Listas",
                                    required=False, help="Listas Negras")

    z_capacitacion_fecha = fields.Date(string="Fecha última Capacitación", required=False, help="Introduzca Fecha de última capacitación")
    z_capacitacion_cal = fields.Float(string="Calificación de Capacitación", required=False, help="Introduzca calificación de la última capacitación")
    z_revisada_is = fields.Boolean(string="Carga revisada por el auditor")
    z_id_is = fields.Boolean(string="Identificación Oficial")
    z_id = fields.Binary(string="Id Oficial", help="Copia de Id Oficial")
    z_cv_is = fields.Boolean(string="Curriculum Vitae")
    z_cv = fields.Binary(string="CV", help="Copia de Curriculum Vitae")
    z_dom_is = fields.Boolean(string="Comprobante de Domicilio")
    z_dom = fields.Binary(string="Domicilio", help="Copia de Comprobante de Domicilio")
    z_pld_is = fields.Boolean(string="Constancia de Verificación listas negras y PEPs")
    z_pld = fields.Binary(string="Verifación Listas", help="Copia de Constancia de Verificación listas negras y PEPs")
    z_dec_is = fields.Boolean(string="Declaración firmada")
    z_dec = fields.Binary(string="Declaración", help="Copia de Declaración firmada")
    z_cap_is = fields.Boolean(string="Constancia de Capacitación")
    z_cap = fields.Binary(string="Capacitación", help="Copia de Constancia de Capacitación")
    z_eva_is = fields.Boolean(string="Evaluaciones PLD/FT")
    z_eva = fields.Binary(string="Evaluaciones", help="Copia de Evaluaciones PLD/FT")
    z_man_is = fields.Boolean(string="Constancia recepción de Manual")
    z_man = fields.Binary(string="Manual", help="Copia de Constancia recepción de Manual")
    z_cumple = fields.Float(string="% Cumplimiento", required=False, help="Porcentaje de Cumplimiento")


    @api.onchange('z_id_is','z_cv_is','z_dom_is','z_pld_is', 'z_dec_is','z_cap_is','z_eva_is','z_man_is')
    def cambia_promedio(self):
        id_val = 0
        cv_val = 0
        dom_val = 0
        pld_val = 0
        dec_val = 0
        cap_val = 0
        eva_val = 0
        man_val = 0

        if self.z_id_is:
            id_val = 100
        if self.z_cv_is:
            cv_val = 100
        if self.z_dom_is:
            dom_val = 100
        if self.z_pld_is:
            pld_val = 100
        if self.z_dec_is:
            dec_val = 100
        if self.z_cap_is:
            cap_val = 100
        if self.z_eva_is:
            eva_val = 100
        if self.z_man_is:
            man_val = 100

        self.z_cumple = (id_val + cv_val + dom_val + pld_val + dec_val + cap_val + eva_val + man_val) / 8






    @api.onchange('name')
    def cambia_name(self):
            self.z_nombre = ""
            self.z_materno = ""
            self.z_paterno = self.name

    @api.multi
    def verifica_empleado(self):
      for record in self:
        self.ensure_one()

        pld_site = self.env['x_360fin.pld'].browse(1)

        apellidos = ""
        nombres = ""

        if (self.identification_id != False):
            rfc = self.identification_id
        else:
            rfc = ""

        apellidos = self.z_paterno
        if (self.z_materno != False):
            apellidos += " "
            apellidos += self.z_materno
        if (self.z_nombre != False):
            nombres = self.z_nombre

        j_param = {"Apellido": apellidos, "Nombre": nombres, "Identificacion": rfc, "PEPS_otros_paises" : "S", "Usuario": pld_site.x_name, "Password": pld_site.x_password}
        json_data = requests.post(pld_site.x_url, data=j_param)

        j_data = json_data.json()
        j_status = json_data.status_code
        j_headers = json_data.headers

        if j_status == 200:
            lista_negra = self.env['x_360fin.lista_negra']

            if j_headers['Content-Length'] == '78':
                lista_negra.create({'x_name': self.name,
                                    'x_company_id': self.company_id.id,
                                    'x_employee_id': self.id,
                                    'x_fecha': datetime.datetime.now(),
                                    'x_status': "No",
                                    'x_mensaje': j_data['Message'],
                                    'x_denominacion': "No disponible"})
                self.write({'z_riesgo_neg': '1'})
            else:
                self.write({'z_riesgo_neg': '2'})
                for each in j_data:
                    lista_negra.create({'x_name': self.name,
                                        'x_company_id': self.company_id.id,
                                        'x_employee_id': self.id,
                                        'x_fecha': datetime.datetime.now(),
                                        'x_status': "Si",
                                        'x_mensaje': "Similitud Encontrada",
                                        'x_denominacion': each['Denominacion'],
                                        'x_identificacion': each['Identificacion'],
                                        'x_id_tributaria': each['Id_Tributaria'],
                                        'x_otra_id': each['Otra_Identificacion'],
                                        'x_cargo': each['Cargo'],
                                        'x_lugar_trabajo': each['Lugar_Trabajo'],
                                        'x_direccion': each['Direccion'],
                                        'x_enlace': each['Enlace'],
                                        'x_tipo': each['Tipo'],
                                        'x_lista': each['Lista'],
                                        'x_pais_lista': each['Pais_Lista'],
                                        'x_cod_individuo': each['Cod_Individuo'],
                                        'x_exactitud_denominacion': each['Exactitud_Denominacion'],
                                        'x_exactitud_id': each['Exactitud_Identificacion']})
                    if each['Tipo'] == "TER":
                        self.write({'z_riesgo_neg': '3'})

            if record.z_riesgo_neg == '1':
                return record
            else:
                if record.z_riesgo_neg == '2':
                    riesgo_text = "Riesgo PEP coincidencia encontrada: " + record.name
                else:
                    riesgo_text = "Riesgo Alto coincidencia encontrada: " + record.name

                alerta = self.env['x_360fin.alerta']

                alerta_cat = self.env['x_360fin.alerta.catalogo']

                alerta_stage = self.env['x_360fin.alerta.stage'].search([('sequence', '=', 1)], limit=1)

                a00 = alerta_cat.search([('name', '=', "A00")])

                if a00 != False:
                    alerta_cuenta =  a00.count + 1
                    a00.write({'count': alerta_cuenta})
                    alerta_codigo = 10000 + alerta_cuenta
                    fecha_now = datetime.datetime.now()
                    fecha_codigo = fecha_now.strftime('%Y%m%d')

                    name_id = "A00-"+ str(alerta_codigo) + "-" + fecha_codigo

                    alerta_id = alerta.create({'name': name_id,
                                           'alert_id': a00.id,
                                           'company_id': record.company_id.id,
                                           'employee_id': record.id,
                                           'state': '1',
                                           'stage_id': alerta_stage.id,
                                           'user_det_id': self.env.uid,
                                           'message': riesgo_text,
                                           })





