import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-crm_action',
        'odoo8-addon-crm_autoalias',
        'odoo8-addon-crm_claim_code',
        'odoo8-addon-crm_claim_type',
        'odoo8-addon-crm_deduplicate_acl',
        'odoo8-addon-crm_deduplicate_by_website',
        'odoo8-addon-crm_deduplicate_filter',
        'odoo8-addon-crm_lead_address_street3',
        'odoo8-addon-crm_lead_code',
        'odoo8-addon-crm_lead_firstname',
        'odoo8-addon-crm_lead_invoice_address',
        'odoo8-addon-crm_lead_lost_reason',
        'odoo8-addon-crm_lead_sale_link',
        'odoo8-addon-crm_lead_second_lastname',
        'odoo8-addon-crm_lead_supplier',
        'odoo8-addon-crm_lead_vat',
        'odoo8-addon-crm_lead_website',
        'odoo8-addon-crm_location',
        'odoo8-addon-crm_phonecall_category',
        'odoo8-addon-crm_phonecall_summary_predefined',
        'odoo8-addon-crm_sale_marketing',
        'odoo8-addon-crm_sector',
        'odoo8-addon-crm_track_next_action',
        'odoo8-addon-lettermgmt',
        'odoo8-addon-marketing_crm_partner',
        'odoo8-addon-mass_mailing_partner',
        'odoo8-addon-newsletter',
        'odoo8-addon-newsletter_email_template_qweb',
        'odoo8-addon-partner_withdrawal',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
