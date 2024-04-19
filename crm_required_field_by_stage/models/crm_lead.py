# Copyright 2024 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        stages = self.env["crm.stage"].search([("required_field_ids", "!=", False)])
        if view.type == "form" and stages:
            for field in stages.mapped("required_field_ids"):
                stages_with_field = stages.filtered(
                    lambda stage, field=field: field in stage.required_field_ids
                )
                for node in arch.xpath("//field[@name='%s']" % field.name):
                    node.attrib["required"] = "stage_id  in [%s]" % ",".join(
                        [str(id) for id in stages_with_field.ids]
                    )
        return arch, view

    @api.model
    def _get_view_cache_key(self, view_id=None, view_type="form", **options):
        """The override of _get_view changing the required fields labels according
        to the stage makes the view cache dependent on the stages with required fields."""
        key = super()._get_view_cache_key(view_id, view_type, **options)
        return key + tuple(
            self.env["crm.stage"]
            .search([("required_field_ids", "!=", False)])
            .mapped("required_field_ids.name")
        )
