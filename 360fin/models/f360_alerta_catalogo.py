# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Low'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class Catalogo(models.Model):

    _name = "x_360fin.alerta.catalogo"¿0
    _description = "360fin.alerta.catalogo"
    _rec_name = 'name'
    _order = "sequence, name, id"

    create_date = fields.datetime(string="Created on", store=True, copy=True)
    create_uid = fields.Many2one(string="Created by", store=True, copy=True, comodel_name='res.users')
    display_name = fields.Char(string="Display", readonly=True, size=0)
    id = fields.Integer(string="ID", readonly=True, store=True, copy=True)
    write_date = fields.datetime(string="Last Updated on", store=True, copy=True)
    write_uid = fields.Many2one(string="Last Updated by", store=True, copy=True, comodel_name='res.users')

    color = fields.Integer(string="Color Index", default=0, store=True, copy=True)
    color_type = fields.Selection([('0', 'ND'), ('1', 'Verde'), ('2', 'Amarilla'),('3','Roja') ],string="Color de alerta", store=True, copy=True)
    count = fields.Integer(string="Cuenta", default=0, store=True, copy=True)
    message = fields.Text(string="Message of Alert", store=True, copy=True, help="Enter the message of the alert")
    name = fields.Char(string="Catálogo Alerta", required=True, store=True, copy=True, translate=True, size=0)
    recommend = fields.Text(string="Recommendation", store=True, copy=True, translate=True, help="Recommendation")
    rule = fields.Text(string="Rule", store=True, copy=True, translate=True, help="Rule")
    sequence = fields.Integer(string="Sequence"+, store=True, copy=True, default=1, help="Used to order stages. Lower is better.")
    type =  fields.Selection([('0', 'ND'), ('1', 'Inusual'), ('2', 'Relevante'),('3','Inusual/Relevante'), ('4','Listas Negras') ], string="Tipo de alerta", store=True, copy=True)
