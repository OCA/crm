# -*- coding: utf-8 -*-
# 2025 Moval Agroingeniería
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
import base64
import logging

_logger = logging.getLogger(__name__)

class ResRegistryMailWizard(models.TransientModel):
    _name = 'res.registry.mail.wizard'
    _description = 'Res Registry Mail Wizard'

    def _default_optional_text(self):
        return _('Notice of registration. Report attached.')

    optional_text = fields.Text(
        string='Optional Text',
        default=_default_optional_text,
        help='Text that will be included in the email.',
    )

    def action_send_mails(self, **kwargs):
        self.ensure_one()
        active_ids = self.env.context.get('active_ids', [])
        registries = self.env['res.registry'].browse(active_ids)
        template = self.env.ref('crm_registrymgmt.email_template_res_registry', False)

        if not template:
            return True

        report = self.env['ir.actions.report']._get_report_from_name('crm_registrymgmt.template_res_registry_report')

        for registry in registries:
            sender = registry.sender_partner_id
            recipient = registry.recipient_partner_id
            sender_email = sender.email
            recipient_email = recipient.email

            # Generate PDF
            pdf_content, _ = report._render_qweb_pdf(report.report_name, res_ids=[registry.id])
            document_name = '{}.pdf'.format(registry.number.replace('/', '_'))
            pdf_base64 = base64.b64encode(pdf_content)

            attachment = self.env['ir.attachment'].create({
                'res_model': 'res.registry',
                'res_id': registry.id,
                'name': document_name,
                'datas': pdf_base64,
                'mimetype': 'application/pdf',
            })

            ctx = {
                'default_model': 'res.registry',
                'default_res_id': registry.id,
                'optional_text': self.optional_text or '',
                'sender_email': sender_email,
                'recipient_email': recipient_email,
                'partner_lang': sender.lang or 'es_ES',
                'registry_number': registry.number,
                'company_name': sender.company_name,
                'default_attachment_ids': [(4, attachment.id)],
            }

            mail_id = template.with_context(ctx).send_mail(
                registry.id,
                force_send=True,
                email_values={
                    'attachment_ids': [(4, attachment.id)],
                    'body_html': self.optional_text or '',
                    'subject': registry.name,
                }
            )

            if not mail_id:
                _logger.error("Failed to send email for registry %s", registry.number)
        return True