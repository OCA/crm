# 2025 Moval Agroingeniería
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Entry Registry Management',
    'summary': 'Tracking for entry registry',
    'version': '16.0.1.1.0',
    'category': 'Customer Relationship Management',
    'website': 'https://odoo-community.org/',
    'author': 'Moval Agroingeniería',
    'license': 'AGPL-3',
    'depends': [
        'mail'
    ],
    'data': [
        'data/registry_sequence.xml',
        'data/res_registry_mail.xml',
        'views/res_registry_view.xml',
        'views/registry_category_view.xml',
        'views/registry_type_view.xml',
        'views/registry_channel_view.xml',
        'reports/res_registry_report.xml',
        'views/res_registry_config_settings_view.xml',
        'views/res_partner_view.xml',
        'wizards/res_registry_mail_wizard.xml',
        'security/registrymgmt_security.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
    'installable': True,
}
