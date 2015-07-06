# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Antonio Espinosa <antonioea@antiun.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import urlparse
import urllib

from openerp import models
from openerp.tools.translate import _


class MailMail(models.Model):
    _inherit = 'mail.mail'

    def _get_unsubscribe_url(self, cr, uid, mail, email_to,
                             msg=None, context=None):
        m_config = self.pool.get('ir.config_parameter')
        base_url = m_config.get_param(cr, uid, 'web.base.url')
        config_msg = m_config.get_param(cr, uid,
                                        'mass_mailing.unsubscribe.label')
        url = urlparse.urljoin(
            base_url, 'mail/mailing/%(mailing_id)s/unsubscribe?%(params)s' % {
                'mailing_id': mail.mailing_id.id,
                'params': urllib.urlencode({
                    'db': cr.dbname,
                    'res_id': mail.res_id,
                    'email': email_to
                })
            }
        )
        html = ''
        if config_msg is False:
            html = '<small><a href="%(url)s">%(label)s</a></small>' % {
                'url': url,
                'label': msg or _('Click to unsubscribe'),
            }
        elif config_msg.lower() != 'false':
            html = config_msg % {
                'url': url,
            }
        return html
