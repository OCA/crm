//-*- coding: utf-8 -*-
//© 2017 Therp BV <http://therp.nl>
//License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

openerp.newsletter_email_template_qweb = function(instance)
{
    instance.newsletter.FieldEmailHTML.include({
        init: function()
        {
            this.ckeditor_filter.allow('t[*]');
            this.ckeditor_config.extraAllowedContent = 't[*]';
            return this._super.apply(this, arguments);
        }
    });
};
