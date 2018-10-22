# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import email_re, email_split
from odoo.exceptions import UserError, AccessError

from . import f360_alerta_stage

_logger = logging.getLogger(__name__)

class F360Alerta(models.Model):
    _name = "x_360fin.alerta"
    _inherit = ['mail.thread']
    _description = "360fin.alerta"
    _order = "priority desc,date_deadline,id desc"

    def _default_probability(self):
        stage_id = self._default_stage_id()
        if stage_id:
            return self.env['x_360fin.alerta.stage'].browse(stage_id).probability
        return 10

    def _default_stage_id(self):
        return self._stage_find(domain=[('fold', '=', False)]).id

    create_date = fields.datetime(string="Created on", store=True, copy=True)
    create_uid = fields.Many2one(string="Created by", store=True, copy=True, comodel_name='res.users')
    display_name = fields.Char(string="Display", readonly=True, size=0)
    id = fields.Integer(string="ID", readonly=True, store=True, copy=True)
    write_date = fields.datetime(string="Last Updated on", store=True, copy=True)
    write_uid = fields.Many2one(string="Last Updated by", store=True, copy=True, comodel_name='res.users')

    active = fields.Boolean(string="Active", store=True, copy=True)
    name = fields.Char(string="Alerta", required=True, index=True, readonly=True, store=True, copy=True, size=0)
    date_action_last = fields.Datetime(string="Last Action", readonly=True, store=True, copy=True)
    kanban_state = fields.Selection([('grey', 'Pendiente'), ('red', 'Bloqueado'), ('green', 'Validado'), ('blue','Reportado')], string="Activity State", readonly=True)
    description = fields.Text(string="Notes", store=True, copy=True)
    priority = fields.Selection(f360_alerta_stage.AVAILABLE_PRIORITIES, string="Priority", store=True, index=True, copy=True, default=f360_alerta_stage.AVAILABLE_PRIORITIES[0][0])
    date_closed = fields.Datetime(string="Closed Date", readonly=True, store=True)
    stage_id = fields.Many2one(string="Stage", track_visibility="onchange", store=True, copy=True, index=True,
        group_expand="_read_group_stage_ids", default=lambda self: self._default_stage_id(), comodel_name="x_360fin.alerta.stage")
    user_id = fields.Many2one(string="Compliance Officer", index=True, track_visibility="onchange", comodel_name="res.users", default=lambda self: self.env.user)
    date_open = fields.Datetime(string="Assigned", readonly=True, store=True, copy=True, default=fields.Datetime.now)
    day_open = fields.Float(string="Days to Assign", readonly=True, store=True)
    day_close = fields.Float(string="Days to Close", readonly=True, store=True)
    date_last_stage_update = fields.Datetime(string="Last Stage Update", store=True, index=True, copy=True, default=fields.Datetime.now)
    date_conversion = fields.Datetime(string="Conversion Date", readonly=True, store=True, copy=True)

    # Only used for type opportunity
    date_deadline = fields.Date(string="Expected Closing", store=True, copy=True, help="Estimate of the date on which the alert will be late.")
    color = fields.Integer(string="Color Index", store=True, copy=True, default=0)

    # Alerts
    alert_id = fields.Many2one(string="Alerta id", readonly=True, store=True, copy=True, comodel_name="x_360fin.alerta.catalogo", help="Alerta id")
    employee_id = fields.Many2one(string="Employee id", readonly=True, store=True, copy=True, help="Employee id", comodel_name="hr.employee")
    partner_id = fields.Many2one(string="Partner id", readonly=True, store=True, copy=True, help="Partner id", comodel_name="res.partner")
    company_id = fields.Many2one(string="Company id", readonly=True, store=True, copy=True, help="Company id", comodel_name="res.company")
    invoice_id = fields.Many2one(string="Invoice id", readonly=True, store=True, copy=True, help="Invoice id", comodel_name="account.invoice")
    payment_id = fields.Many2one(string="Payment id", readonly=True, store=True, copy=True, help="Payment id", comodel_name="account.payment")
    user_det_id = fields.Many2one(string="User Detect", track_visibility="onchange", readonly=True, store=True, copy=True, index=True, comodel_name="res.user")
    message = fields.Text(string="Message of Alert", readonly=True, store=True, copy=True, help="Enter here the message of the alert")
    message_ids = fields.one2many(string="Messages ids", store=True, comodel_name="mail.message", relation_field="res_id")
    message_channel_ids = fields.Many2one(string="Followers (Channels)", readonly=True, comodel_name="mail.channel")
    message_follower_ids = fields.one2many(string="Followers", store=True, comodel_name="mail.followers", relation_field="res_id")
    message_last_post = fields.datetime(string="Last Message Date", store=True, copy=True, help="Date of the last message posted on the record")
    message_needaction = fields.Boolean(string="Action Needed", readonly=True, help="If checked, new messages require your attention.If checked,")
    message_needaction_counter = fields.Integer(string="Number of actions", readonly=True, help="Number of messages which requires an action")
    message_partner_ids = fields.Many2many(string="Follower (Partners)", readonly=True, comodel_name="res.partner")
    message_unread = fields.Boolean(string="Unread Messages", readonly=True, help="If checked new messages require your attention")
    message_is_follower = fields.Boolean(string="Is Follower", readonly=True)
    message_is_needaction = fields.Boolean(string="Followers (Partners)", readonly=True)
    message_is_needaction_counter = fields.Integer(string="Number of actions", readonly=True)
    message_is_partner_ids = fields.Many2many(string="Follower (Partners)", readonly=True)
    analysis = fields.Text(string="Analysis of Alert", store=True, copy=True, help="Enter the analysis of the alert")
    message_unread_counter = fields.Integer(string="Unread Messages counter", readonly=True, help="Number of unread messages")
    state = fields.Selection([('1', 'Pendiente'), ('2', 'Validado'), ('3', 'Bloqueado'), ('4','Reportado')], string="State", store=True, copy=True)

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
