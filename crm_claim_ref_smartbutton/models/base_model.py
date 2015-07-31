# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields, api, _
from openerp.models import BaseModel
from lxml import etree


base_fields_view_get = BaseModel.fields_view_get


@api.model
def fields_view_get_crm_claim(
        self, view_id=None, view_type='form', toolbar=False, submenu=False):
    """This method should have old API signature because keyword arguments
    doesn't respect expected order (context argument at the end).
    """
    res = base_fields_view_get(
        self, view_id=view_id, view_type=view_type, toolbar=toolbar,
        submenu=submenu)
    if view_type != 'form':
        return res
    has_model = self.env['res.request.link'].search(
        [('object', '=', res['model'])])
    if has_model:
        eview = etree.fromstring(res['arch'])
        button_boxes = eview.xpath("//div[contains(@class,'oe_button_box')]")
        if not button_boxes:
            # Create a container for the smartbutton
            button_box = etree.Element(
                'div', {'class': 'oe_right oe_button_box'})
            # Append it to the view
            sheets = eview.xpath("//sheet")
            if sheets:
                sheets[0].insert(0, button_box)
            else:
                forms = eview.xpath("//form")
                if forms:
                    forms[0].insert(0, button_box)
        else:
            button_box = button_boxes[0]
        field_name = 'crm_claim_linked_count_tech'
        new_field = etree.Element(
            'field', {'string': _('Linked claims'),
                      'name': field_name,
                      'widget': 'statinfo'})
        new_button = etree.Element(
            'button', {'class': 'oe_inline oe_stat_button',
                       'type': 'object',
                       'name': 'action_open_linked_claims_tech',
                       'icon': 'fa-comments',
                       'groups': 'base.group_sale_salesman'})
        new_button.append(new_field)
        button_box.append(new_button)
        res['arch'] = etree.tostring(eview)
        res['fields'][field_name] = self.fields_get([field_name])
    return res


@api.multi
def _open_related_claims(self):
    claim_obj = self.env['crm.claim']
    act_window_obj = self.env['ir.actions.act_window']
    search_term = '%s,%i' % (self._model, self.id)
    claims = claim_obj.search([('ref', '=', search_term)])
    result = act_window_obj.for_xml_id('crm_claim', 'crm_case_categ_claim0')
    result['context'] = {'default_ref': search_term}
    result['domain'] = [('id', 'in', claims.ids)]
    return result


def _add_magic_fields_wrapper(wrapped_func):
    wrapped_func = wrapped_func.__func__

    def _w(*args, **kwargs):
        """Inject field in each model."""
        cls = args[0]
        name = 'crm_claim_linked_count_tech'
        if name not in cls._fields:
            cls._add_field(
                name, fields.Integer(compute='count_linked_claim_tech',
                                     automatic=True))
        wrapped_func(*args, **kwargs)

    return classmethod(_w)
BaseModel._add_magic_fields = _add_magic_fields_wrapper(
    BaseModel._add_magic_fields)


@api.one
def count_linked_claim_tech(self):
    self.crm_claim_linked_count_tech = self.env['crm.claim'].search_count(
        [('ref', '=', '%s,%i' % (self._model, self.id))])


# Monkey patch functions
BaseModel.action_open_linked_claims_tech = _open_related_claims
BaseModel.fields_view_get = fields_view_get_crm_claim
BaseModel.count_linked_claim_tech = count_linked_claim_tech
