import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-crm_claim>=16.0dev,<16.1dev',
        'odoo-addon-crm_claim_code>=16.0dev,<16.1dev',
        'odoo-addon-crm_claim_type>=16.0dev,<16.1dev',
        'odoo-addon-crm_industry>=16.0dev,<16.1dev',
        'odoo-addon-crm_lead_code>=16.0dev,<16.1dev',
        'odoo-addon-crm_lead_currency>=16.0dev,<16.1dev',
        'odoo-addon-crm_lead_firstname>=16.0dev,<16.1dev',
        'odoo-addon-crm_lead_search_archive>=16.0dev,<16.1dev',
        'odoo-addon-crm_lead_to_task>=16.0dev,<16.1dev',
        'odoo-addon-crm_lead_vat>=16.0dev,<16.1dev',
        'odoo-addon-crm_location>=16.0dev,<16.1dev',
        'odoo-addon-crm_partner_assign>=16.0dev,<16.1dev',
        'odoo-addon-crm_phonecall>=16.0dev,<16.1dev',
        'odoo-addon-crm_project_task>=16.0dev,<16.1dev',
        'odoo-addon-crm_salesperson_planner>=16.0dev,<16.1dev',
        'odoo-addon-crm_salesperson_planner_sale>=16.0dev,<16.1dev',
        'odoo-addon-crm_security_group>=16.0dev,<16.1dev',
        'odoo-addon-crm_stage_probability>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
