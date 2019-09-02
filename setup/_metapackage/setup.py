import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-calendar_resource',
        'odoo10-addon-crm_claim',
        'odoo10-addon-crm_claim_code',
        'odoo10-addon-crm_claim_type',
        'odoo10-addon-crm_deduplicate_acl',
        'odoo10-addon-crm_deduplicate_filter',
        'odoo10-addon-crm_lead_code',
        'odoo10-addon-crm_lead_partner_role',
        'odoo10-addon-crm_lead_website',
        'odoo10-addon-crm_location',
        'odoo10-addon-crm_location_nuts',
        'odoo10-addon-crm_meeting_commercial_partner',
        'odoo10-addon-crm_phonecall',
        'odoo10-addon-crm_phonecall_summary_predefined',
        'odoo10-addon-crm_sale_marketing',
        'odoo10-addon-crm_sector',
        'odoo10-addon-marketing_crm_partner',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
