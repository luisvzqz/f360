# -*- coding: utf-8 -*-

from odoo import api, fields, models

import urllib.parse
import requests
import datetime

class ResPartner(models.Model):
    _inherit = "res.partner"

    z_persona = fields.Many2one(comodel_name="x_360fin.persona", string="Persona", required=False, help="Persona a identificar")
    z_persona_cod = fields.Char(string="Código Persona", required=False, related="z_persona.x_codigo")
    z_persona_gpo = fields.Integer(string="Grupo Personas", required=False, related="z_persona.x_grupo")
    z_persona_imp = fields.Integer(string="Personas", required=False, related="z_persona.x_impacto", readonly=1)

    z_socio_is = fields.Boolean(string="Es accionista ?")
    z_socio_per = fields.Float(string="Porcentaje Accionario",  required=False, help="Porcentaje Accionario del Socio")
    z_socio_mon = fields.Float(string="Monto Accionario",  required=False, help="MontoAccionario del Socio")
    z_socio = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Socios", required=False, help="Socios de la empresa", domain=[('z_socio_is', '=', True)])

    z_fin_is = fields.Boolean(string="Miembro Sociedad Financiera", compute='_calcula_fin_is', readonly=1)
    z_fin_consejo_is = fields.Boolean(string="Miembro del Consejo?")
    z_fin_ccc_is = fields.Boolean(string="Miembro del CCC?")
    z_fin_ctl_is = fields.Boolean(string="Persona que ejerce el control?")

    z_provreal_is = fields.Boolean(string="Proveedor Real?")
    z_provreal = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Proveedor Real",
                                     required=False,
                                     help="Proveedor Real", domain=[('z_provreal_is', '=', True)])

    z_fin_is_is = fields.Boolean(string="Sociedad Financiera", compute='_calcula_fin_is_is', readonly=1)
    z_fin_consejo = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Consejo", required=False, help="Consejo de Administración", domain=[('z_fin_consejo_is', '=', True)])
    z_fin_ccc = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="CCC", required=False, help="Cómite de Comunicación y Control", domain=[('z_fin_ccc_is', '=', True)])
    z_fin_ctl = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Control", required=False, help="Personas que ejercen el Control", domain=[('z_fin_ctl_is', '=', True)])

    z_fideicomitente_is = fields.Boolean(string="Es fideicomitente ?")
    z_fideicomitente_per = fields.Float(string="Porcentaje Fideicomitente", required=False, help="Porcentaje Fideicomitente")
    z_fideicomitente_mon = fields.Float(string="Monto del Fideicomitente", required=False, help="Monto del Fideicomitente")
    z_fideicomitente_pat = fields.Char(string="Patrimonio fideicomitido", required=False, help="Monto del Fideicomitente")

    z_fideicomitente = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Fideicomitentes", required=False,
                              help="Fidecomitentes de la empresa", domain=[('z_fideicomitente_is', '=', True)])

    z_fideicomisario_is = fields.Boolean(string="Es fideicomisario ?")
    z_fideicomisario = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Fideicomisario", required=False,
                              help="Fideicomisario del fideicomiso", domain=[('z_fideicomisario_is', '=', True)])

    z_delegado_is = fields.Boolean(string="Es Delegado ?")
    z_delegado = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Delegados", required=False,
                              help="Delegados del fideicomiso", domain=[('z_delegado_is', '=', True)])

    z_comite_is = fields.Boolean(string="Miembro Cómite Técnico ?")
    z_comite = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Cómite Técnico", required=False,
                              help="Cómite Técnico del fideicomiso", domain=[('z_comite_is', '=', True)])


    z_com_nombre = fields.Char(string="Compañía", required=False, help="Nombre de la compañía")

    z_com_nacionalidad = fields.Many2one(comodel_name="res.country", string="Nacionalidad", required=False, help="País de nacionalidad")
    z_com_nacionalidad_imp = fields.Integer(related='z_com_nacionalidad.x_impacto', string="Nacionalidad", readonly=1)

    z_com_ocupacion = fields.Many2one(comodel_name="res.partner.industry", string="Actividad", required=False, help="Ocupación, Profesión, Actividad ó giro del negocio al que se dedique el cliente")
    z_com_ocupacion_imp = fields.Integer(related='z_com_ocupacion.x_impacto', string="Actividad", readonly=1)
    z_com_ocupacion_cnbv = fields.Char(related='z_com_ocupacion.x_cnbv', string="CNBV", help="Actividad CNBV", readonly=1)

    z_com_estado = fields.Many2one(comodel_name="res.country.state", string="Estado", required=False, help="Entidad Federativa de nacionalidad")
    z_com_estado_imp = fields.Integer(related='z_com_estado.x_impacto', string="Estado", readonly=1)

    z_com_constitucion = fields.Date(string="Fecha de Constitución", required=False, help="Introduzca Fecha de Constitución")
    z_com_socio_parent = fields.Many2one(comodel_name="res.partner", string="Socio Padre", required=False, help="Socio Padre")
    z_com_socio_child = fields.One2many(comodel_name="res.partner", inverse_name="z_com_socio_parent", string="Socios", required=False, help="Nombres de los socios")
    z_com_socio_porcentaje = fields.Float(string="Porcentaje Accionario",  required=False, help="Porcentaje Accionario del Socio")
    z_com_acta = fields.Binary(string="Acta Constitutiva o Contrato", help="Copia de Acta Constitutiva o Contrato Fideicomiso")
    z_com_aviso = fields.Binary(string="Aviso de Inscripción", help="Copia de Aviso de Inscripción")
    z_com_entidad_is = fields.Boolean(string="Es Entidad Gobierno")
    z_com_entidad = fields.Binary(string="Nombramiento Entidad", help="Copia de Nombramiento Entidad de Gobierno")
    z_com_entidad_reg = fields.Char(string="Registro Entidad", required=False, help="Registro CNVB o similar que sea centro cambiario, transmisor de dinero u otra Entidad" )
    z_com_estr_acc = fields.Binary(string="Estructura Accionaria", help="Copia de documento de Estructura Accionaria")
    z_com_org = fields.Binary(string="Organigrama", help="Copia de documento de Organigrama")

    z_com_fid_is = fields.Boolean(string="Es Fideicomiso")
    z_com_fid_num = fields.Char(string="Número de Fideicomiso", required=False, help="Entre el Número de Fideicomiso")

    z_com_fid_act_is = fields.Boolean(string="El fidecomiso se dedica a las Actividades Vulnerables")
    z_com_fid_act = fields.Many2one(comodel_name="res.partner.industry", string="Actividad", required=False, help="Actividades Vulnerables")
    z_com_fid_act_imp = fields.Integer(related='z_com_fid_act.x_impacto', string="Actividad Fideicomiso", readonly=1)
    z_com_fid_act_cnbv = fields.Char(related='z_com_fid_act.x_cnbv', string="CNBV", help="Actividad CNBV", readonly=1)

    z_com_fid_parent = fields.Many2one(comodel_name="res.partner", string="Fideicomitente Padre", required=False, help="Fideicomitente Padre")
    z_com_fid_child = fields.One2many(comodel_name="res.partner", inverse_name="z_com_fid_parent", string="Fideicomitentes", required=False, help="Nombres de los Fideicomitentes")
    z_com_fid_aportacion = fields.Float(string="Aportación de Fideicomitentes",  required=False, help="Aportación de Fideicomitentes")
    z_com_fid_patrim = fields.Char(string="Patrimonio fideicomitido", required=False, help="Patrimonio fideicomitido (bienes y derechos)")
    z_com_fid_fid_parent = fields.Many2one(comodel_name="res.partner", string="Fideicomisiarios", required=False, help="Fideicomisiarios Padre")
    z_com_fid_fid_child = fields.One2many(comodel_name="res.partner", inverse_name="z_com_fid_fid_parent", string="Fideicomisiarios", required=False, help="Nombres de los Fideicomisiarios")
    z_com_fid_del_parent = fields.Many2one(comodel_name="res.partner", string="Delegados", required=False, help="Delegados Padre")
    z_com_fid_del_child = fields.One2many(comodel_name="res.partner", inverse_name="z_com_fid_del_parent", string="Delegados", required=False, help="Nombres de los Delegados")
    z_com_fid_cte_parent = fields.Many2one(comodel_name="res.partner", string="Comite Técnico", required=False, help="Comite Técnico Padre")
    z_com_fid_cte_child = fields.One2many(comodel_name="res.partner", inverse_name="z_com_fid_cte_parent", string="Comite Técnico", required=False, help="Nombres de los Comite Técnico")
    z_com_fid_noint_prest_is = fields.Boolean(string="El fideicomiso sirve para prestaciones laborales o sociales?")
    z_com_fid_noint_prest_gob_is = fields.Boolean(string="El fideicomitente es una entidad pública?")
    z_com_fid_noint_prest_cnt_is = fields.Boolean(string="Existe un contrato para que la info de Fideicomisiario la tenga el cliente?")
    z_com_fid_noint_prest_cla_is = fields.Boolean(string="Existe un contrato para que la info de Fideicomisiario la conserve el fideicomiso?")
    z_com_fid_noint_prest_ent_is = fields.Boolean(string="Entidad actua como fideicomiso?")

    z_com_fid_noint_prest_exp_is = fields.Boolean(string="Excepción para no integración ?")

    z_ind_nombre = fields.Char(string="Nombres(s)", required=False, help="Nombres de la persona física" )
    z_ind_paterno = fields.Char(string="Apellido Paterno", required=False, help="Introduzca Apellido Paterno")
    z_ind_materno = fields.Char(string="Apellido Materno", required=False, help="Introduzca Apellido Materno")
    z_ind_nacimiento = fields.Date(string="Fecha de Nacimiento", required=False, help="Introduzca Fecha de Nacimiento")
    z_ind_genero = fields.Many2one(comodel_name="x_360fin.genero", string="Genero", required=False, help="Femenino o Masculino")

    z_ind_nac_pais = fields.Many2one(comodel_name="res.country", string="País", required=False, help="País de nacimiento")
    z_ind_nac_pais_imp = fields.Integer(related='z_ind_nac_pais.x_impacto', string="País Origen", readonly=1)

    z_ind_nac_estado = fields.Many2one(comodel_name="res.country.state", string="Estado", required=False, help="Entidad Federativa de nacimiento")
    z_ind_nac_estado_imp = fields.Integer(related='z_ind_nac_estado.x_impacto', string="Estado Origen", readonly=1)

    z_ind_nacionalidad = fields.Many2one(comodel_name="res.country", string="Nacionalidad", required=False, help="País de nacionalidad")
    z_ind_nacionalidad_imp = fields.Integer(related='z_ind_nacionalidad.x_impacto', string="Nacionalidad", readonly=1)

    z_ind_ocupacion = fields.Many2one(comodel_name="res.partner.industry", string="Ocupación", required=False, help="Ocupación, Profesión, Actividad ó giro del negocio al que se dedique el cliente")
    z_ind_ocupacion_imp = fields.Integer(related='z_ind_ocupacion.x_impacto', string="Actividad", readonly=1)
    z_ind_ocupacion_cnbv = fields.Char(related='z_ind_ocupacion.x_cnbv', string="CNBV", help="Actividad CNBV", readonly=1)

    z_ind_curp = fields.Char(string="CURP", required=False, help="Código Único de Registro de Población (CURP)")
    z_ind_curp_doc = fields.Binary(string="Doc CURP", help="Copia de CURP")
    z_ind_id = fields.Many2one(comodel_name="x_360fin.id", string="Identificación", required=False, help="Tipo de Identificación")
    z_ind_id_doc = fields.Binary(string="Doc Id", help="Copia de Identificación")

    z_rfc_doc = fields.Binary(string="Doc RFC", help="Copia de RFC")

    z_fea = fields.Char(string="FEA", required=False, help="Firma Electrónica Avanzada del SAT (FEA)")
    z_fea_doc = fields.Binary(string="Doc FEA", help="Copia de FEA")


    z_dom = fields.Many2one(comodel_name="x_360fin.domicilio", string="Comprobante de domicilio", required=False, help="Comprobante de domicilio")
    z_dom_doc = fields.Binary(string="Doc Domicilio", help="Copia de Identificación")

    z_contrato_doc = fields.Binary(string="Contrato", help="Copia de Contrato ó solicitud firmado")

    z_eval_riesgo_per = fields.Boolean(string="Tiene Evaluación de Riesgo Periodicas", help="El auditor responderá si el cliente CUENTA con evaluaciones semestrales de riesgo")
    z_entrevista = fields.Boolean(string="Tiene Entrevista Personal", help="El auditor responderá si se realizó la entrevista personal")

    z_portercero_is = fields.Boolean(string="Actua por tercero",  )
    z_portercero = fields.Many2one(comodel_name="res.partner", string="Por tercero", required=False, help="Nombre del tercero")

    z_apoderado_is = fields.Boolean(string="Actua como apoderado", )
    z_apoderado = fields.Many2one(comodel_name="res.partner", string="Apoderado", required=False, help="Nombre del apoderado")
    z_apoderado_doc = fields.Binary(string="Poder", help="Poder apoderado")

    z_coacreditado_is = fields.Boolean(string="Es coacreditado ?", )
    z_coacreditado = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Coacreditados", required=False,
                              help="Coacreditados", domain=[('z_coacreditado_is', '=', True)])

    z_beneficiario_is = fields.Boolean(string="Es beneficiario ?", )
    z_beneficiario = fields.One2many(comodel_name="res.partner", inverse_name="parent_id", string="Beneficiarios", required=False,
                              help="Beneficiarios", domain=[('z_beneficiario_is', '=', True)])

    z_coacreditados_parent = fields.Many2one(comodel_name="res.partner", string="Coacreditado Padre", required=False, help="Coacreditado Padre")
    z_coacreditados_child = fields.One2many(comodel_name="res.partner", inverse_name="z_coacreditados_parent", string="Coacreditados", required=False, help="Nombres de los coacreditados")
    z_beneficiarios_parent = fields.Many2one(comodel_name="res.partner", string="Beneficiario Padre", required=False, help="Beneficiario Padre")
    z_beneficiarios_child = fields.One2many(comodel_name="res.partner", inverse_name="z_beneficiarios_parent", string="Beneficiarios", required=False, help="Nombres de los beneficiarios")

    z_provrecursos_is = fields.Boolean(string="Tiene Proveedor de Recursos", )
    z_provrecursos = fields.Many2one(comodel_name="res.partner", string="Proveedor de recursos", required=False, help="Nombre del proveedor de recursos")

    z_monto_men = fields.Float(string="Monto mensual máximo a pagar", required=False, help="Monto mensual máximo a pagar")
    z_monto_efe = fields.Float(string="Monto mensual efectivo a pagar", required=False, help="Monto mensual máximo a pagar")

    z_lista_negra = fields.One2many(comodel_name="x_360fin.lista_negra", inverse_name="x_partner_id", string="Listas", required=False, help="Listas Negras")

    z_riesgo_pro = fields.Float(string="Producto",  required=False, help="Riesgo por Producto", readonly=1)
    z_riesgo_loc = fields.Float(string="Localidad", required=False, help="Riesgo por Localidad", readonly=1)
    z_riesgo_mto = fields.Float(string="Monto", required=False, help="Riesgo por Monto", readonly=1)
    z_riesgo_act = fields.Float(string="Actividad", required=False, help="Riesgo por Actividad", readonly=1)
    z_riesgo_mon = fields.Float(string="Moneda", required=False, help="Riesgo por Moneda", readonly=1)
    z_riesgo_per = fields.Float(string="Persona", required=False, help="Riesgo por Tipo de Persona", readonly=1)
    z_riesgo_nac = fields.Float(string="Nacionalidad", required=False, help="Riesgo por Nacionalidad", readonly=1)
    z_riesgo_mer = fields.Float(string="Mercado", required=False, help="Riesgo por Mercado", readonly=1)
    z_riesgo_ins = fields.Float(string="Instrumento Monetario", required=False, help="Riesgo por Instrumento Monetario", readonly=1)
    z_riesgo = fields.Float(string="Total", required=False, help="Riesgo Total", readonly=1)
    z_riesgo_rie = fields.Selection([('1','Bajo'),
                                     ('2','Medio'),
                                     ('3','Alto'),],
                                      string="Nivel", required=False, help="Nivel de Riesgo")

    z_riesgo_neg = fields.Selection([('1','No Encontrado'),
                                     ('2','PEP'),
                                     ('3','Alto'),],
                                      string="Nivel de Lista Negra", required=False, help="Nivel de Lista Negra")

    z_zip_id = fields.Many2one(comodel_name="x_360fin.zipcode", string="Código Postal", required=False, help="Código Postal")
    z_colonia_id = fields.Many2one(comodel_name="x_360fin.colonia", string="Colonia", required=False, help="Colonia")
    z_municipio_id = fields.Many2one(comodel_name="x_360fin.municipio", string="Municipio", required=False, help="Municipio")
    z_localidad_id = fields.Many2one(comodel_name="x_360fin.localidad", string="Localidad", required=False, help="Localidad/Ciudad")
    z_cnbv = fields.Char(related='z_zip_id.x_cnbv', string="CNBV", help="Código de localidad CNBV", readonly=1)
    z_localidad_imp = fields.Integer(related='z_zip_id.x_impacto', string="Localidad", readonly=1)

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

            if self.name != False:
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

    @api.depends('parent_id','company_id')
    def _calcula_fin_is(self):
        for record in self:
            if (record.parent_id.name != record.company_id.name):
                record.z_fin_is = False
            else:
                record.z_fin_is = True


    @api.depends('name','company_id')
    def _calcula_fin_is_is(self):
        for record in self:
            if (record.name != record.company_id.name):
                record.z_fin_is_is = False
            else:
                record.z_fin_is_is = True

    @api.onchange('name')
    def check_change(self):
        if self.is_company:
            self.z_com_nombre = self.name
            self.z_ind_nombre = ""
            self.z_ind_materno = ""
            self.z_ind_paterno = ""
        else:
            self.z_com_nombre = ""
            self.z_ind_nombre = ""
            self.z_ind_materno = ""
            self.z_ind_paterno = self.name

    @api.onchange('company_type')
    def company_type_change(self):
        if self.company_type == 'company':
            self.z_com_nombre = self.name
            self.z_ind_nombre = ""
            self.z_ind_materno = ""
            self.z_ind_paterno = ""
        else:
            self.z_com_nombre = ""
            self.z_ind_nombre = ""
            self.z_ind_materno = ""
            self.z_ind_paterno = self.name

    @api.onchange('z_riesgo_pro','z_riesgo_loc','z_riesgo_mto','z_riesgo_act', 'z_riesgo_mon','z_riesgo_per','z_riesgo_nac','z_riesgo_mer','z_riesgo_ins')
    def promedio_change(self):
        self.z_riesgo = (self.z_riesgo_pro + self.z_riesgo_loc + self.z_riesgo_mto + self.z_riesgo_act + self.z_riesgo_mon + self.z_riesgo_per + self.z_riesgo_nac + self.z_riesgo_mer + self.z_riesgo_ins) / 9
        if self.z_riesgo <= 5:
            self.z_riesgo_rie = '1'
        elif self.z_riesgo <= 20:
            self.z_riesgo_rie = '2'
        elif self.z_riesgo > 20:
            self.z_riesgo_rie = '3'


    @api.onchange('is_company')
    def is_company_change(self):
        v_persona = self.env['x_360fin.persona']
        v_res = {}
        if self.is_company :
            v_res['domain'] = {'z_persona': [('x_is_company', '=', True)]}
            self.z_persona = v_persona.browse(2)
        else:
            v_res['domain'] = {'z_persona': [('x_is_company', '=', False)]}
            self.z_persona = v_persona.browse(1)
        return v_res


    @api.multi
    def verifica_pld(self):
       for record in self:
        self.ensure_one()

        pld_site = self.env['x_360fin.pld'].browse(1)

        apellidos = ""
        nombres = ""

        if (self.vat != False):
            rfc = self.vat
        else:
            rfc = ""

        if self.is_company:
            apellidos = self.z_com_nombre
        else:
            apellidos = self.z_ind_paterno
            if (self.z_ind_materno != False):
                apellidos += " "
                apellidos += self.z_ind_materno
            if (self.z_ind_nombre != False):
                nombres = self.z_ind_nombre

        j_param = {"Apellido": apellidos, "Nombre": nombres, "Identificacion": rfc, "PEPS_otros_paises" : "S", "Usuario": pld_site.x_name, "Password": pld_site.x_password}
        json_data = requests.post(pld_site.x_url, data=j_param)

        j_data = json_data.json()
        j_status = json_data.status_code
        j_headers = json_data.headers

        if j_status == 200:
            lista_negra = self.env['x_360fin.lista_negra']
            self.write({'z_riesgo_neg': '1'})

            if j_headers['Content-Length'] == '78':
                lista_negra.create({'x_name': self.name,
                                    'x_partner_id': self.id,
                                    'x_fecha': datetime.datetime.now(),
                                    'x_status': "No",
                                    'x_mensaje': j_data['Message'],
                                    'x_denominacion': "No disponible",
                                    'x_user_id': self.env.uid,
                                    'x_company_id': self.company_id.id,
                                    })
                self.write({'z_riesgo_neg': '1'})
            else:
                self.write({'z_riesgo_neg': '2'})
                for each in j_data:
                    lista_negra.create({'x_name': self.name,
                                        'x_partner_id': self.id,
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
                                        'x_exactitud_id': each['Exactitud_Identificacion'],
                                        'x_user_id': self.env.uid,
                                        'x_company_id': self.company_id.id,
                                        })
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
                                           'partner_id': record.id,
                                           'company_id': record.company_id.id,
                                           'state': '1',
                                           'stage_id': alerta_stage.id,
                                           'user_det_id': self.env.uid,
                                           'message': riesgo_text,
                                           })


    @api.multi
    def evalua_impacto(self):
        self.ensure_one()
        if self.is_company:
            riesgo_per = self.company_id.z_probabilidad * ((self.z_persona_imp + self.company_id.z_evento) /2)
            self.z_riesgo_per = (self.company_id.z_riesgo_per + riesgo_per)/2

            riesgo_loc = self.company_id.z_probabilidad * ((self.z_localidad_imp + self.company_id.z_evento) / 2)
            self.z_riesgo_loc = (self.company_id.z_riesgo_loc + riesgo_loc)/2

            riesgo_nac = self.company_id.z_probabilidad * ((self.z_com_nacionalidad_imp + self.company_id.z_evento) /2)
            self.z_riesgo_nac = (self.company_id.z_riesgo_nac + riesgo_nac)/2

            riesgo_act = self.company_id.z_probabilidad * ((self.z_com_ocupacion_imp + self.company_id.z_evento)/2)
            self.z_riesgo_act = (self.company_id.z_riesgo_act + riesgo_act)/2

            self.z_riesgo_pro = self.company_id.z_riesgo_pro
            self.z_riesgo_mto = self.company_id.z_riesgo_mto
            self.z_riesgo_mon = self.company_id.z_riesgo_mon
            self.z_riesgo_mer = self.company_id.z_riesgo_mer
            self.z_riesgo_ins = self.company_id.z_riesgo_ins
        else:
            riesgo_per = self.company_id.z_probabilidad * ((self.z_persona_imp + self.company_id.z_evento) / 2)
            self.z_riesgo_per = (self.company_id.z_riesgo_per + riesgo_per) / 2

            riesgo_loc = self.company_id.z_probabilidad * ((self.z_localidad_imp + self.company_id.z_evento) /2)
            self.z_riesgo_loc = (self.company_id.z_riesgo_loc + riesgo_loc) / 2

            riesgo_nac = self.company_id.z_probabilidad * ((self.z_ind_nacionalidad_imp + self.company_id.z_evento) /2)
            self.z_riesgo_nac = (self.company_id.z_riesgo_nac + riesgo_nac) / 2

            riesgo_act = self.company_id.z_probabilidad * ((self.z_ind_ocupacion_imp + self.company_id.z_evento) / 2)
            self.z_riesgo_act = (self.company_id.z_riesgo_act + riesgo_act) / 2

            self.z_riesgo_pro = self.company_id.z_riesgo_pro
            self.z_riesgo_mto = self.company_id.z_riesgo_mto
            self.z_riesgo_mon = self.company_id.z_riesgo_mon
            self.z_riesgo_mer = self.company_id.z_riesgo_mer
            self.z_riesgo_ins = self.company_id.z_riesgo_ins

        self.z_riesgo = (self.z_riesgo_pro + self.z_riesgo_loc + self.z_riesgo_mto + self.z_riesgo_act + self.z_riesgo_mon + self.z_riesgo_per + self.z_riesgo_nac + self.z_riesgo_mer + self.z_riesgo_ins) / 9
        if self.z_riesgo <= 5:
            self.z_riesgo_rie = '1'
        elif self.z_riesgo <= 20:
            self.z_riesgo_rie = '2'
        elif self.z_riesgo > 20:
            self.z_riesgo_rie = '3'



    @api.multi
    def add_pld(self):
       for record in self:

            lista_negra = self.env['res.partner'].search([('z_riesgo_neg', '!=', '1')],)

            for each in lista_negra:

                if each.z_riesgo_neg == '2':
                    riesgo_text = "Riesgo PEP coincidencia encontrada: " + each.name
                else:
                    riesgo_text = "Riesgo Alto coincidencia encontrada: " + each.name

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
                                           'partner_id': each.id,
                                           'company_id': each.company_id.id,
                                           'state': '1',
                                           'stage_id': alerta_stage.id,
                                           'user_det_id': each.user_id.id,
                                           'message': riesgo_text,
                                           })




