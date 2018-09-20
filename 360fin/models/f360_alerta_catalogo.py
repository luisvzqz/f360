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

    _name = "x_360fin.alerta.catalogo"
    _description = "360fin.alerta.catalogo"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Catálogo Alerta', required=True, translate=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    recommend = fields.Text('Recommendation', translate=True,
        help='Recommendation')
    rule = fields.Text('Rule', translate=True,
        help='Rule')
    color = fields.Integer('Color Index', default=0)
    color_type = fields.Selection([('0', 'ND'), ('1', 'Verde'), ('2', 'Amarilla'),('3','Roja') ],
        string='Color de alerta')
    type =  fields.Selection([('0', 'ND'), ('1', 'Inusual'), ('2', 'Relevante'),('3','Inusual/Relevante'), ('4','Listas Negras') ],
        string='Tipo de alerta')
    count = fields.Integer('Cuenta', default=0)


