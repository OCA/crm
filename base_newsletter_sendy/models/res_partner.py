import logging

from odoo import api, fields, models
from pysendy import (AlreadySubscribedException, InvalidEmailAddressException,
                     Sendy)

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    newsletter_sendy = fields.Boolean(string='Newsletter (via Sendy)')

    @api.multi
    def change_newsletter_sendy(self, email, subscribe):
        if not email:
            return
        sendy_url = self.env['ir.config_parameter'].get_param('sendy_url')
        sendy_list = self.env['ir.config_parameter'].get_param('sendy_list')
        sendy_api_key = self.env['ir.config_parameter'].get_param('sendy_api_key')
        
        if not sendy_url or not sendy_list or not sendy_api_key:
            _logger.info('Sandy is not configured')
            return False

        _logger.debug('Using Sendy at %s for list %s', sendy_url, sendy_list)
        _logger.info(
            'Changing status for %(name)s <%(email)s> to %(action)s' % {
                'name': self.name, 'email': email, 'action': subscribe})

        sendy = Sendy(sendy_url)
        try:
            if subscribe:
                sendy.subscribe(
                    name=self.name, email=email, list_id=sendy_list,api_key=sendy_api_key)
            else:
                sendy.unsubscribe(email=email, list_id=sendy_list)
        except AlreadySubscribedException as e:
            # If the user is already subscribed, this is not a fatal error.
            _logger.exception(e)
        except InvalidEmailAddressException as e:
            # If the user is already unsubscribed, this is not a fatal error.
            _logger.exception(e)
        except Exception as e:
            _logger.exception(e)

    @api.multi
    def write(self, vals):
        if 'email' in vals:
            for partner in self:
                if partner.newsletter_sendy:
                    # If the old address is subscribed, we have to unsubscribe
                    partner.change_newsletter_sendy(partner.email, False)
                    # If the new address is subscribed or
                    # the old address was subscribed and the subscription
                    # has not changed, we subscribe it.
                    if vals.get('newsletter_sendy', partner.newsletter_sendy):
                        partner.change_newsletter_sendy(
                            vals.get('email'), True)
                elif vals.get('newsletter_sendy'):
                    partner.change_newsletter_sendy(vals.get('email'), True)
            return super(Partner, self).write(vals)

        if 'newsletter_sendy' in vals:
            for partner in self:
                partner.change_newsletter_sendy(
                    partner.email, vals.get('newsletter_sendy'))
        return super(Partner, self).write(vals)

    @api.multi
    def unlink(self):
        for partner in self:
            if partner.newsletter_sendy:
                partner.change_newsletter_sendy(partner.email, False)
        return super(Partner, self).unlink()

    @api.model
    def create(self, vals):
        res = super(Partner, self).create(vals)
        if vals.get('newsletter_sendy') and vals.get('email'):
            res.change_newsletter_sendy(vals.get('email'), True)
        return res

    @api.multi
    def copy(self, default=None):
        # Deactivate newsletter subscription immediately after copying
        #  in order to avoid accidentally removing an existing email address.
        default = default or {}
        default['newsletter_sendy'] = False
        return super(Partner, self).copy(default=default)
