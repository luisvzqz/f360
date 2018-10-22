# -*- coding: utf-8 -*-

from odoo import api, fields, models

import datetime

class ListaNegra(models.Model):
    _name = "x_360fin.lista_negra"
    _description = "360fin.lista_negra"

    create_date = fields.datetime(string="Created on", store=True, copy=True)
    create_uid = fields.Many2one(string="Created by", store=True, copy=True, comodel_name="res.users")
    display_name = fields.Char(string="Display", readonly=True, size=0)
    id = fields.Integer(string="ID", readonly=True, store=True, copy=True)
    write_date = fields.datetime(string="Last Updated on", store=True, copy=True)
    write_uid = fields.Many2one(string="Last Updated by", store=True, copy=True, comodel_name="res.users")

    x_cargo = fields.Char(string="Cargo", store=True, copy=True, size=0, help="Cargo")
    x_cod_individuo = fields.Char(string="Código Individuo", store=True, copy=True, size=0, help="Código Individuo")

    x_denominacion = fields.Char(string="Denominación", store=True, copy=True, size=0, help="Denominación")
    x_direccion = fields.Char(string="Dirección", store=True, copy=True, size=0, help="Dirección")

    x_enlace = fields.Char(string="Enlace", store=True, copy=True, size=0, help="Enlace")
    x_exactitud_denominacion = fields.Char(string="Exactidud Denominación", store=True, copy=True, size=0, help="Exactitud Denominación")
    x_exactitud_id = fields.Char(string="Exactitud Identificación", store=True, copy=True, size=0, help="Exactitud id")
    x_fecha = fields.datetime(string="Fecha Consulta", store=True, copy=True, help="Fecha Consulta")
    x_id_tributaria = fields.Char(string="Id Tributaria", store=True, copy=True, size=0, help="Id Tributaria")
    x_identificacion = fields.Char(string="Identificación", store=True, copy=True, size=0, help="Identificación")
    x_lista = fields.Char(string="Lista", store=True, copy=True, size=0, help="Lista")
    x_lugar_trabajo = fields.Char(string="Lugar de trabajo", store=True, copy=True, size=0, help="Lugar de trabajo")
    x_mensaje = fields.Char(string="Mensajes", store=True, copy=True, size=0, help="Mensaje")
    x_otra_id =  fields.Char(string="Otra Identificación", store=True, copy=True, size=0, help="Otra Identificación")
    x_pais_lista = fields.Char(string="País Lista", store=True, copy=True, size=0, help="País Lista")
    x_status = fields.Char(string="Estado de Búsqueda", store=True, copy=True, size=0, help="Estado de Búsqueda")

    x_name = fields.Char(string="Name", store=True, size=0)
    x_company_id = fields.Many2one(string="Compañía	id", store=True, copy=True, comodel_name="res.company", on_delete=NULL, help="Company id")
    x_employee_id = fields.Many2one(string="Employee id", store=True, copy=True, comodel_name="hr.employee", on_delete=NULL, help="Employee id")
    x_partner_id = fields.Many2one(string="Socio id", store=True, copy=True, comodel_name="res.partner", on_delete=NULL, help="Partner id")
