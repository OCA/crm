import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-crm_lead_firstname',
        'odoo13-addon-crm_lead_product',
        'odoo13-addon-crm_lead_vat',
        'odoo13-addon-crm_location',
        'odoo13-addon-crm_meeting_commercial_partner',
        'odoo13-addon-crm_phonecall',
        'odoo13-addon-crm_stage_probability',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
