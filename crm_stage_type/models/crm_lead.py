# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, SUPERUSER_ID


class Lead(models.Model):
    _inherit = 'crm.lead'

    stage_id = fields.Many2one(
        domain="[('team_id', 'in', [team_id, False]), "
               "('lead_type', 'in', [type, 'both'])]")

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        ctx_type = self.env.context.get('default_type')
        stages = super(Lead, self)._read_group_stage_ids(stages, domain, order)
        search_domain = [('id', 'in', stages.ids)]
        if ctx_type:
            search_domain += [('lead_type', 'in', [ctx_type, 'both'])]
        stage_ids = stages._search(
            search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def _stage_find(self, team_id=False, domain=None, order='sequence'):
        ctx_type = self.env.context.get('default_type')
        types = ['both']
        if ctx_type:
            types += [ctx_type]
        # check whether we should try to add a condition on type
        avoid_add_type_term = domain and any([
            term for term in domain if len(term) == 3 if term[0] == 'lead_type'
        ])
        if avoid_add_type_term:
            return super(Lead, self)._stage_find(team_id, domain, order)
        # collect all team_ids by adding given one,
        # and the ones related to the current leads
        team_ids = set()
        if team_id:
            team_ids.add(team_id)
        for lead in self:
            if lead.team_id:
                team_ids.add(lead.team_id.id)
        # generate the domain
        if team_ids:
            search_domain = ['|', ('team_id', '=', False),
                             ('team_id', 'in', list(team_ids))]
        else:
            search_domain = [('team_id', '=', False)]
        search_domain.append(('lead_type', 'in', types))
        # AND with the domain in parameter
        if domain:
            search_domain += list(domain)
        # perform search, return the first found
        return self.env['crm.stage'].search(
            search_domain, order=order, limit=1)

    @api.multi
    def merge_opportunity(self, user_id=False, team_id=False):
        opportunities_head = super(Lead, self).merge_opportunity(
            user_id, team_id)
        if opportunities_head.team_id:
            team_stage_ids = self.env['crm.stage'].search(
                [('team_id', 'in', [opportunities_head.team_id.id, False]),
                 ('lead_type', 'in', [opportunities_head.type, 'both'])],
                order='sequence')
            if opportunities_head.stage_id not in team_stage_ids:
                opportunities_head.write({
                    'stage_id': team_stage_ids[0] if team_stage_ids else False
                })
        return opportunities_head

    @api.multi
    def _convert_opportunity_data(self, customer, team_id=False):
        value = super(Lead, self)._convert_opportunity_data(customer, team_id)
        if not self.stage_id or self.stage_id.lead_type == 'lead':
            stage = self._stage_find(
                team_id=team_id, domain=[('lead_type', 'in',
                                          ['opportunity', 'both'])])
            value['stage_id'] = stage.id
            if stage:
                value['probability'] = stage.probability
        return value
