# 2025 Moval Agroingeniería
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime
import json
from odoo import models, fields, api


class ResRegistry(models.Model):
    _name = 'res.registry'
    _description = "Log of Entry Movements"
    _inherit = 'mail.thread'
    _order = 'number desc'

    number = fields.Char(
        help="Auto Generated Number of registry.",
        default="/")

    name = fields.Text(
        string='Subject',
        help="Subject of registry.")

    move = fields.Selection(
        [('in', 'IN'), ('out', 'OUT')],
        help="Incoming or Outgoing registry.",
        readonly=True,
        default=lambda self: self.env.context.get('move', 'in'))

    state = fields.Selection(
        [('draft', 'Draft'),
         ('validated', 'Validated'),
         ],
        default='draft',
        readonly=True,
        copy=False,
        tracking=True,
    )

    date = fields.Date(
        string='Registry Date',
        help='The registry\'s date.',
        default=fields.Date.today,
    )

    snd_date = fields.Date(
        string='Sent Date',
        help='The date the registry was sent.',
    )

    rec_date = fields.Date(
        string='Received Date',
        help='The date the registry was received.',
    )

    document_date = fields.Date(
        string='Document Date',
        help='The date of the document itself.',
    )

    def default_recipient(self):
        move_type = self.env.context.get('move', False)
        if move_type == 'in':
            return self.env.user.company_id.partner_id

    def default_sender(self):
        move_type = self.env.context.get('move', False)
        if move_type == 'out':
            return self.env.user.company_id.partner_id

    recipient_partner_id = fields.Many2one(
        'res.partner',
        string='Recipient',
        tracking=True,
        default=default_recipient,
    )

    sender_partner_id = fields.Many2one(
        'res.partner',
        string='Sender',
        tracking=True,
        default=default_sender,
    )

    notes = fields.Html(
        string='Notes',
    )

    channel_id = fields.Many2one(
        'registry.channel',
        string="Channel",
    )

    category_ids = fields.Many2many(
        'registry.category',
        string="Tags",
    )

    type_id = fields.Many2one(
        'registry.type',
        string="Type",
    )

    track_ref = fields.Char(
        string='Tracking Reference',
    )

    orig_ref = fields.Char(
        string='Original Reference',
    )

    expeditor_ref = fields.Char(
        string='Expeditor Reference',
    )

    parent_id = fields.Many2one(
        'res.registry',
        string='Parent',
        groups='res_registrymgmt.group_res_registrymgmt_manager')

    child_line = fields.One2many(
        'res.registry',
        'parent_id',
        string='registry Lines',
        groups='res_registrymgmt.group_res_registrymgmt_manager')

    res_registry_attachment_ids = fields.One2many(
        string="Attachments",
        comodel_name="ir.attachment",
        compute="_compute_res_registry_attachment_ids")

    def _compute_res_registry_attachment_ids(self):
        self.res_registry_attachment_ids = \
            self.env['ir.attachment'].search(
                [('res_model', '=', self._name), ('res_id', '=', self.id)])

    def write(self, vals):
        if 'date' in vals and str(vals['date']) != fields.Date.today():
            move_type = self.move
            date_obj = datetime.datetime.strptime(
                str(vals['date']), '%Y-%m-%d')
            sequence_obj = self.env['ir.sequence'].search(
                [('code', '=', ('%s.registry' % move_type))])
            seq_len = sequence_obj.padding
            prefix_raw = str(sequence_obj.prefix)
            normal_prefix = prefix_raw.split('/')[0]
            current_prefix = self.number.split('/')[0]
            if normal_prefix == current_prefix:
                prefix = self._recompute_prefix(prefix_raw, date_obj)
                current_seq_number = self.number[-seq_len:]
                number = prefix + current_seq_number
            else:
                number = self.number
            vals.update({'number': number})
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            date = vals.get('date')
            if date and str(date) != fields.Date.today():
                move_type_context = \
                    self.env.context.get('default_move') or \
                    self.env.context.get('move') or 'in'
                move_type = vals.get('move') or move_type_context
                date_obj = datetime.datetime.strptime(
                    str(date), '%Y-%m-%d')
                sequence_obj = self.env['ir.sequence'].search(
                    [('code', '=', ('%s.registry' % move_type))])
                next_num = str(sequence_obj.sudo().number_next_actual).zfill(
                    sequence_obj.padding)
                increased_seq_num = sequence_obj.sudo().number_next_actual + 1
                sequence_obj.sudo().write(
                    {'number_next_actual': increased_seq_num})
                if sequence_obj.use_date_range:
                    for date_range in sequence_obj.date_range_ids:
                        date_from = datetime.datetime.strptime(
                            date_range.date_from, '%Y-%m-%d')
                        date_to = datetime.datetime.strptime(
                            date_range.date_to, '%Y-%m-%d')
                        if date_from <= date_obj <= date_to:
                            next_num = \
                                str(date_range.number_next_actual).zfill(
                                    sequence_obj.padding)
                            increased_seq_num = \
                                date_range.number_next_actual + 1
                            date_range.sudo().write(
                                {'number_next_actual': increased_seq_num})
                            break
                prefix_raw = str(sequence_obj.prefix)
                prefix = self._recompute_prefix(prefix_raw, date_obj)
                number = prefix + next_num
                vals['number'] = number
            elif ('number' not in vals) or (
                    vals.get('number') in ('/', False)):
                sequence = self.env['ir.sequence']
                move_type_context = \
                    self.env.context.get('default_move') or \
                    self.env.context.get('move') or 'in'
                move_type = vals.get('move') or move_type_context
                vals['number'] = sequence.sudo().next_by_code(
                    '%s.registry' % move_type)
            elif ('number' in vals):
                pass
        return super().create(vals_list)

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == 'form':
            config = self.env['ir.config_parameter'].sudo()
            allow_number_edition = \
                config.get_param(
                    'res_registry_config.allow_number_edition', False)

            for node in arch.xpath("//field[@name='number']"):
                if allow_number_edition:
                    node.attrib.pop("readonly", None)
                    node.attrib.pop("invisible", None)
                    modifiers = json.loads(node.get("modifiers", "{}"))
                    modifiers['readonly'] = False
                    node.set("modifiers", json.dumps(modifiers))
                else:
                    node.attrib['readonly'] = '1'
                    node.attrib['invisible'] = '1'
                    modifiers = json.loads(node.get("modifiers", "{}"))
                    modifiers['readonly'] = True
                    modifiers['invisible'] = True
                    node.set("modifiers", json.dumps(modifiers))

        return arch, view

    def _recompute_prefix(self, prefix_raw, date_obj):
        prefix = prefix_raw.replace(
            '%(year)s', str(date_obj.year)).replace(
            '%(y)s', '{:02d}'.format(int(date_obj.strftime("%y")))).replace(
            '%(month)s', '{:02d}'.format(date_obj.month)).replace(
            '%(day)s', '{:02d}'.format(date_obj.day)).replace(
            '%(weekday)s', '{:02d}'.format(date_obj.weekday())).replace(
            '%(woy)s', '{:02d}'.format(int(date_obj.strftime("%W")))).replace(
            '%(doy)s', '{:02d}'.format(int(date_obj.strftime("%j")))).replace(
            '%(h24)s', '00').replace('%(h12)s', '00').replace(
            '%(min)s', '00').replace('%(sec)s', '00')
        return prefix

    def action_draft(self):
        self.write({'state': 'draft'})
        return True

    def action_validate(self):
        vals = {'state': 'validated'}
        if self.move == 'out':
            vals['snd_date'] = self.snd_date or fields.Date.today()
        elif self.move == 'in':
            vals['rec_date'] = self.rec_date or fields.Date.today()
        self.write(vals)
        return True
