import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-crm_claim',
        'odoo11-addon-crm_deduplicate_acl',
        'odoo11-addon-crm_deduplicate_filter',
        'odoo11-addon-crm_lead_firstname',
        'odoo11-addon-crm_phonecall',
        'odoo11-addon-crm_phonecall_planner',
        'odoo11-addon-crm_phonecall_summary_predefined',
        'odoo11-addon-crm_sale_marketing',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
