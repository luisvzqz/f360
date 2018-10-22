# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

AVAILABLE_PRIORITIES = [
    ('0', 'Normal'),
    ('1', 'Low'),
    ('2', 'High'),
    ('3', 'Very High'),
]


class Stage(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Main 360fin objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _name = "x_360fin.alerta.stage"
    _description = "360fin.alerta.stage"
    _rec_name = 'name'
    _order = "sequence, name, id"

    create_date = fields.datetime(string="Created on", store=True, copy=True)
    create_uid = fields.Many2one(string="Created by", store=True, copy=True, comodel_name='res.users')
    display_name = fields.Char(string="Display", readonly=True, size=0)
    id = fields.Integer(string="ID", readonly=True, store=True, copy=True)
    write_date = fields.datetime(string="Last Updated on", store=True, copy=True)
    write_uid = fields.Many2one(string="Last Updated by", store=True, copy=True, comodel_name='res.users')

    fold = fields.Boolean(string="Folded in Pipeline", store=True, copy=True, help="This stage is folded in the kanban view when there are no records in that stage to display."")
    legend_priority = fields.Text(string="Priority Management Explanation", store=True, copy=True, translate=True,
        help="Explanation text to help users using the star and priority mechanism on stages or issues that are in this stage.")
    name = fields.Char(string="Stage Name", required=True, store=True, copy=True, translate=True, size=0)
    sequence = fields.Integer(string="Sequence", store=True, copy=True, default=1, help="Used to order stages. Lower is better.")
    requirements = fields.Text(string="Requirements", store=True, copy=True,
        help="Enter here the internal requirements for this stage. It will appear as a tooltip over the stage's name.")
