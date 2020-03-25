{
    'name': "Newsletter subscription via Sendy",
    'version': '12.0.1.0.0',
    'depends': ['mail'],
    'data': [
        'data/ir_config.xml',
        'views/res_partner_views.xml',
    ],
    'author': "Nitrokey GmbH, Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'website': "https://github.com/OCA/base_newsletter_sendy",
    'external_dependencies': {
        'python': ['pysendy'],
    }
}
