import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-crm_claim>=15.0dev,<15.1dev',
        'odoo-addon-crm_industry>=15.0dev,<15.1dev',
        'odoo-addon-crm_lead_code>=15.0dev,<15.1dev',
        'odoo-addon-crm_location>=15.0dev,<15.1dev',
        'odoo-addon-crm_phonecall>=15.0dev,<15.1dev',
        'odoo-addon-crm_phonecall_planner>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
