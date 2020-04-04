# Copyright 2015-2017 Odoo S.A.
# Copyright 2017 Tecnativa - Vicent Cubells
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class CrmClaimStage(models.Model):
    """ Model for claim stages. This models the main stages of a claim
        management flow. Main CRM objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """

    _name = "crm.claim.stage"
    _description = "Claim stages"
    _order = "sequence"

    name = fields.Char(string="Stage Name", required=True, translate=True)
    sequence = fields.Integer(default=1, help="Used to order stages. Lower is better.")
    team_ids = fields.Many2many(
        comodel_name="crm.team",
        relation="crm_team_claim_stage_rel",
        column1="stage_id",
        column2="team_id",
        string="Teams",
        help="Link between stages and sales teams. When set, this limitate "
        "the current stage to the selected sales teams.",
    )
    case_default = fields.Boolean(
        string="Common to All Teams",
        help="If you check this field, this stage will be proposed by default "
        "on each sales team. It will not assign this stage to existing "
        "teams.",
    )
