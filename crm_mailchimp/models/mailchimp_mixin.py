# Copyright 2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MailchimpMixin(models.AbstractModel):
    _name = "mailchimp.mixin"
    _description = "Can be added to models that contain email to enable subscriptions"

    def _compute_subscription_count(self):
        """Compute number of lists to which email is subscribed."""
        subscriber_model = self.env["mailchimp.subscriber"]
        for this in self:
            this.subscription_count = subscriber_model.search_count(
                [("res_model", "=", this._name), ("res_id", "=", this.id)]
            )

    subscription_count = fields.Integer(
        "Number of subscriptions", readonly=True, compute="_compute_subscription_count",
    )

    def _trigger_changes(self, vals):
        """If object changes some values, a push to Mailchimp might be needed."""
        subscriber_model = self.env["mailchimp.subscriber"]
        for this in self:
            if this.subscription_count == 0:
                continue
            subscriptions = subscriber_model.get_subscriptions(this)
            email = vals.get("email", False)
            if email:
                subscriptions.ensure_one()
                subscriptions.write({"email": email})
            elif "email" in vals:
                # This means email is set to False / NULL: remove subscriptions.
                subscriptions.write({"state": "pending_removal"})
            subscriptions._push_to_mailchimp(vals=vals)

    def write(self, vals):
        """Make sure changes are written to mailchimp if resource is subscribed."""
        res = super().write(vals)
        self._trigger_changes(vals)
        return res

    def unlink(self):
        """Make sure subscriber is unsubscribed from Mailchimp."""
        subscriber_model = self.env["mailchimp.subscriber"]
        for this in self:
            if this.subscription_count == 0:
                continue
            subscriptions = subscriber_model.get_subscriptions(this)
            subscriptions.write({"state": "pending_removal"})
            subscriptions._push_to_mailchimp()
        super().unlink()

    def button_open_subscriptions(self):
        """Show list with the subscriptions."""
        self.ensure_one()
        action_record = self.env.ref("crm_mailchimp.action_mailchimp_subscriber")
        action = action_record.sudo().read([])[0]
        action["context"] = {
            "search_default_res_model": self._name,
            "search_default_res_id": self.id,
            "default_res_model": self._name,
            "default_res_id": self.id,
            "default_email": self.email,
        }
        action["domain"] = [
            ("res_model", "=", self._name),
            ("res_id", "=", self.id),
        ]
        return action
