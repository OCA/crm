# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


PRIORITIES = [
    ("0","Low"), 
    ("1","Normal"), 
    ("2","High"), 
]

ACTIONS = [
    ("correction","Corrective Action"), 
    ("prevention","Preventive Action"), 
]


class CRMClaimStage(models.Model):
    """ Model for claim stages. This models the main stages of a claim
        management flow. Main CRM objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _name = "crm.claim.stage"
    _description = "Claim stages"
    _rec_name = "name"
    _order = "sequence"

    name = fields.Char(string="Stage Name",
                       required=True,
                       translate=True)
    sequence = fields.Integer(string="Sequence",
                              index=True,
                              help="Used to order stages. Lower is better.",
                              default=1)
    team_ids = fields.Many2many("crm.team",
                                "crm_team_claim_stage_rel",
                                "stage_id",
                                "team_id",
                                string="Teams",
                                help="Link between stages and sales teams. \
                                When set, this limitate the current stage to \
                                the selected sales teams.")
    case_default = fields.Boolean(string="Common to All Teams",
                                  help="If you check this field, this stage \
                                  will be proposed by default on each sales \
                                  team. It will not assign this stage to \
                                  existing teams.")


class CRMClaim(models.Model):
    """ Crm claim
    """
    _name = "crm.claim"
    _description = "Claim"
    _order = "priority,date desc"
    _inherit = ["mail.thread"]

    def _get_request_reference(self):
        return [(link.object, link.name) for link in 
                    self.env['res.request.link'].search([])]

    def _default_stage_id(self):
        """ Gives default stage_id """
        team_id = self.env["crm.team"].\
                      _get_default_team_id(user_id=self.env.uid).id
        return self.stage_find([], team_id, [("sequence", "=", "1")])

    id = fields.Integer(string="ID",
                        readonly=True)
    name = fields.Char(string="Claim Subject",
                       required=True)
    active = fields.Boolean(string="Active", default=True)
    action_next = fields.Char(string="Next Action")
    date_action_next = fields.Datetime(string="Next Action Date")
    description = fields.Text(string="Description")
    resolution = fields.Text(string="Resolution")
    create_date = fields.Datetime(string="Creation Date",
                                  readonly=True)
    write_date = fields.Datetime(string="Update Date",
                                 readonly=True)
    date_deadline = fields.Date(string="Deadline")
    date_closed = fields.Datetime(string="Closed",
                                  readonly=True)
    date = fields.Datetime(string="Claim Date",
                           index=True,
                           default=fields.Datetime.now)
    ref = fields.Reference(string="Reference",
                           selection=_get_request_reference)
    categ_id = fields.Many2one("crm.claim.category",
                               string="Category")
    priority = fields.Selection(selection=PRIORITIES,
                                string="Priority",
                                default="1")
    type_action = fields.Selection(selection=ACTIONS,
                                   string="Action Type")
    user_id = fields.Many2one("res.users",
                              string="Responsible",
                              track_visibility="always",
                              default=lambda self: self.env.user)
    user_fault = fields.Char(string="Trouble Responsible")
    team_id = fields.Many2one("crm.team",
                              string="Sales Team",
                              index=True,
                              help="Responsible sales team."\
                              "Define Responsible user and Email account for"\
                              "mail gateway.",
                              default=lambda self: \
                              self.env['crm.team'].sudo()._get_default_team_id
                              (user_id=self.env.uid))
    company_id = fields.Many2one("res.company",
                                 string="Company",
                                 default=lambda self: self.env['res.company'].
                                 _company_default_get('crm.case'))
    partner_id = fields.Many2one("res.partner",
                                 string="Partner")
    email_cc = fields.Text(string="Watchers Emails",
                           size=252,
                           help="These email addresses will be added to the \
                           CC field of all inbound and outbound emails for \
                           this record before being sent. Separate multiple \
                           email addresses with a comma")
    email_from = fields.Char(string="Email",
                             size=128,
                             help="Destination email for email gateway.")
    partner_phone = fields.Char(string="Phone")
    stage_id = fields.Many2one("crm.claim.stage",
                               string='Stage',
                               track_visibility='onchange',
                               index=True,
                               domain="[('case_default', '=', True)]",
                               group_expand='_read_group_stage_ids',
                               default=lambda self: self._default_stage_id())
    cause = fields.Text(string="Root Cause")

    def stage_find(self, cases, team_id, domain=[], order='sequence'):
        """
          Determine the stage of the current lead with its teams,
          the given domain and the given team_id
            :param cases
            :param team_id
            :param domain : base search domain for stage
            :returns crm.claim.stage recordset
        """
        if isinstance(cases, (int, long)):
            cases = self.browse(cases)
        # collect all team_ids
        team_ids = []
        if team_id:
            team_ids.append(team_id)
        for claim in cases:
            if claim.team_id:
                team_ids.append(claim.team_id.id)
        # OR all team_ids and OR with case_default
        search_domain = []
        if team_ids:
            search_domain += [('|')] * len(team_ids)
            for team_id in team_ids:
                search_domain.append(('team_ids', '=', team_id))
        search_domain.append(('case_default', '=', True))
        # AND with the domain in parameter
        search_domain += list(domain)
        # perform search, return the first found
        return self.env['crm.claim.stage'].search(search_domain,
                                                  order=order,
                                                  limit=1)

    def _onchange_partner_id_values(self, partner_id):
        """ returns the new values when partner_id has changed """
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            return {
                'email_from': partner.email,
                'partner_phone': partner.phone,
            }
        return {}

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        values = self._onchange_partner_id_values(
            self.partner_id.id if self.partner_id else False
        )
        self.update(values)

    @api.model
    def create(self, vals):
        conText = dict(self._context or {})
        if vals.get("team_id") and not conText.get("default_team_id"):
            conText["default_team_id"] = vals.get("team_id")
        return super(CRMClaim, self).create(vals)

    @api.multi
    def copy(self, default=None):
        for claim in self:
            default = dict(default or {},
                           stage_id=self._default_stage_id(),
                           name=_("%s (copy)") % claim.name)
        return super(CRMClaim, self).copy(default=default)

    # -------------------------------------------------------
    # Mail gateway
    # -------------------------------------------------------

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        # remove default author when going through the mail gateway. Indeed we
        # do not want to explicitly set user_id to False; however we do not
        # want the gateway user to be responsible if no other responsible is
        # found.
        self = self.with_conText(default_user_id=False)

        if custom_values is None:
            custom_values = {}
        defaults = {
            'name':  msg_dict.get('subject') or _("No Subject"),
            'email_from': msg_dict.get('from'),
            'email_cc': msg_dict.get('cc'),
            'partner_id': msg_dict.get('author_id', False),
        }
        if msg_dict.get('author_id'):
            defaults.update(self._onchange_partner_id_values(
                msg_dict.get('author_id')))
        if msg_dict.get('priority') in dict(PRIORITIES):
            defaults['priority'] = msg_dict.get('priority')
        defaults.update(custom_values)
        return super(CRMClaim, self).message_new(msg_dict,
                                                 custom_values=defaults)


class CRMClaimCategory(models.Model):
    _name = "crm.claim.category"
    _description = "Category of claim"

    name = fields.Char(string="Name",
                       required=True,
                       translate=True)
    team_id = fields.Many2one("crm.team",
                              string="Sales Team")
