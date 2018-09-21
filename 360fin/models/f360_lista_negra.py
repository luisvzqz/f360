# -*- coding: utf-8 -*-

from odoo import api, fields, models

import datetime

class ListaNegra(models.Model):
    _name = "x_360fin.lista_negra"
    _description = "360fin.lista_negra"

    x_name = fields.Char('Nombre', required=True, index=True)
    x_company_id = fields.Many2one(comodel_name="res.company", string="Compañía", required=False, help="Compañía")
    x_partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=False, help="Asociado/Cliente")
    x_employee_id = fields.Many2one(comodel_name="hr.employee", string="Empleado", required=False, help="Empleado")
    x_user_id = fields.Many2one(comodel_name="res.users", string="Usuario", required=False, help="Usuario")
