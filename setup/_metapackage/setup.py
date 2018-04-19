import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-crm_action',
        'odoo9-addon-crm_claim_code',
        'odoo9-addon-crm_claim_type',
        'odoo9-addon-crm_deduplicate_acl',
        'odoo9-addon-crm_deduplicate_by_ref',
        'odoo9-addon-crm_deduplicate_by_website',
        'odoo9-addon-crm_deduplicate_filter',
        'odoo9-addon-crm_lead_website',
        'odoo9-addon-crm_phonecall',
        'odoo9-addon-crm_phonecall_planner',
        'odoo9-addon-crm_phonecall_summary_predefined',
        'odoo9-addon-crm_sale_marketing',
        'odoo9-addon-marketing_crm_partner',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
