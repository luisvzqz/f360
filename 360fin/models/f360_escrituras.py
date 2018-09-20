# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import email_re, email_split
from odoo.exceptions import UserError, AccessError


_logger = logging.getLogger(__name__)


class F360Escrituras(models.Model):
    _name = "x_360fin.escrituras"
    _description = "360fin.escrituras"


    name = fields.Char('Alerta', required=True, index=True, readonly=True)
    active = fields.Boolean('Active', default=True)
    date_action_last = fields.Datetime('Last Action', readonly=True)
    kanban_state = fields.Selection([('grey', 'Pendiente'), ('red', 'Bloqueado'), ('green', 'Validado'), ('blue','Reportado')],
        string='Activity State', compute='_compute_kanban_state')
    description = fields.Text('Notes')
    create_date = fields.Datetime('Create Date', readonly=True)
    write_date = fields.Datetime('Update Date', readonly=True)
    priority = fields.Selection(f360_alerta_stage.AVAILABLE_PRIORITIES, string='Priority', index=True, default=f360_alerta_stage.AVAILABLE_PRIORITIES[0][0])
    date_closed = fields.Datetime('Closed Date', readonly=True, copy=False)

    stage_id = fields.Many2one('x_360fin.alerta.stage', string='Stage', track_visibility='onchange', index=True,
        group_expand='_read_group_stage_ids', default=lambda self: self._default_stage_id())
    user_id = fields.Many2one('res.users', string='Compliance Officer', index=True, track_visibility='onchange', default=lambda self: self.env.user)

    date_open = fields.Datetime('Assigned', readonly=True, default=fields.Datetime.now)
    day_open = fields.Float(compute='_compute_day_open', string='Days to Assign', store=True)
    day_close = fields.Float(compute='_compute_day_close', string='Days to Close', store=True)
    date_last_stage_update = fields.Datetime(string='Last Stage Update', index=True, default=fields.Datetime.now)
    date_conversion = fields.Datetime('Conversion Date', readonly=True)

    # Only used for type opportunity
    date_deadline = fields.Date('Expected Closing', help="Estimate of the date on which the alert will be late.")
    color = fields.Integer('Color Index', default=0)

    # Alerts
    alert_id = fields.Many2one(comodel_name="x_360fin.alerta.catalogo", string="Alerta id", required=False,
                                     help="Alerta id", readonly=True)
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee id", required=False,
                                     help="Employee id", readonly=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner id", required=False,
                                     help="Partner id", readonly=True)
    company_id = fields.Many2one(comodel_name="res.company", string="Company id", required=False,
                                 help="Company id", readonly=True)
    invoice_id = fields.Many2one(comodel_name="account.invoice", string="Invoice id", required=False,
                                 help="Invoice id", readonly=True)
    payment_id = fields.Many2one(comodel_name="account.payment", string="Payment id", required=False,
                                 help="Payment id", readonly=True)
    user_det_id = fields.Many2one('res.users', string='User Detect', index=True, track_visibility='onchange', readonly=True)

    message = fields.Text('Message of Alert', help="Enter here the message of the alert", readonly=True)

    analysis = fields.Text('Analysis of Alert', help="Enter the analysis of the alert")

    state = fields.Selection([('1', 'Pendiente'), ('2', 'Validado'), ('3', 'Bloqueado'), ('4','Reportado')],
        string='State')



    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # retrieve team_id from the context and write the domain
        # - ('id', 'in', stages.ids): add columns that should be present
        # - OR ('fold', '=', False): add default columns that are not folded

        # search_domain = [('id', 'in', stages.ids)]

        # perform search
        # stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        stage_ids = self.env['x_360fin.alerta.stage'].search([])
        return stage_ids
        #return stages.browse(stage_ids)

    @api.multi
    def _compute_kanban_state(self):
        today = date.today()
        for alerta in self:
            kanban_state = 'grey'
            if alerta.date_deadline:
                alerta_date = fields.Date.from_string(alerta.date_deadline)
                if alerta_date >= today:
                    kanban_state = 'green'
                else:
                    kanban_state = 'red'
            alerta.kanban_state = kanban_state

    @api.depends('date_open')
    def _compute_day_open(self):
        """ Compute difference between create date and open date """
        for alerta in self.filtered(lambda l: l.date_open):
            date_create = fields.Datetime.from_string(alerta.create_date)
            date_open = fields.Datetime.from_string(alerta.date_open)
            alerta.day_open = abs((date_open - date_create).days)

    @api.depends('date_closed')
    def _compute_day_close(self):
        """ Compute difference between current date and log date """
        for alerta in self.filtered(lambda l: l.date_closed):
            date_create = fields.Datetime.from_string(alerta.create_date)
            date_close = fields.Datetime.from_string(alerta.date_closed)
            alerta.day_close = abs((date_close - date_create).days)

    @api.model
    def _onchange_stage_id_values(self, stage_id):
        """ returns the new values when stage_id has changed """
        if not stage_id:
            return {}
        stage = self.env['x_360fin.alerta.stage'].browse(stage_id)
        return {}

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        values = self._onchange_stage_id_values(self.stage_id.id)
        self.update(values)

    def _onchange_partner_id_values(self, partner_id):
        """ returns the new values when partner_id has changed """

        return {}


    @api.model
    def _onchange_user_values(self, user_id):
        """ returns new values when user_id has changed """
        return {}

    @api.onchange('user_id')
    def _onchange_user_id(self):
        """ When changing the user, also set a team_id or restrict team id to the ones user_id is member of. """
        values = self._onchange_user_values(self.user_id.id)
        self.update(values)


    @api.multi
    def action_set_active(self):
        return self.write({'active': True})

    @api.multi
    def action_set_unactive(self):
        return self.write({'active': False})


    def _stage_find(self, domain=None, order='sequence'):
        """ Determine the stage of the current lead with its teams, the given domain and the given team_id
            :param domain : base search domain for stage
            :returns 360fin.alerta.stage recordset
        """
        # AND with the domain in parameter
        # if domain:
        #    search_domain += list(domain)
        # perform search, return the first found
        return self.env['x_360fin.alerta.stage'].search([], limit=1)
