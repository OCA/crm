import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-crm_claim',
        'odoo12-addon-crm_claim_code',
        'odoo12-addon-crm_claim_type',
        'odoo12-addon-crm_industry',
        'odoo12-addon-crm_l10n_eu_nace',
        'odoo12-addon-crm_lead_code',
        'odoo12-addon-crm_lead_firstname',
        'odoo12-addon-crm_lead_product',
        'odoo12-addon-crm_lead_vat',
        'odoo12-addon-crm_location',
        'odoo12-addon-crm_location_nuts',
        'odoo12-addon-crm_meeting_commercial_partner',
        'odoo12-addon-crm_phonecall',
        'odoo12-addon-crm_phonecall_planner',
        'odoo12-addon-crm_phonecall_summary_predefined',
        'odoo12-addon-crm_sale_marketing',
        'odoo12-addon-crm_stage_type',
        'odoo12-addon-crm_team_parent',
        'odoo12-addon-marketing_crm_partner',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
