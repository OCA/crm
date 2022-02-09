import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-crm_claim',
        'odoo14-addon-crm_claim_code',
        'odoo14-addon-crm_industry',
        'odoo14-addon-crm_l10n_eu_nace',
        'odoo14-addon-crm_lead_code',
        'odoo14-addon-crm_lead_firstname',
        'odoo14-addon-crm_lead_vat',
        'odoo14-addon-crm_location',
        'odoo14-addon-crm_location_nuts',
        'odoo14-addon-crm_phone_extension',
        'odoo14-addon-crm_phonecall',
        'odoo14-addon-crm_project',
        'odoo14-addon-crm_security_group',
        'odoo14-addon-crm_stage_probability',
        'odoo14-addon-marketing_crm_partner',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
