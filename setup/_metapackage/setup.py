import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-crm_claim>=16.0dev,<16.1dev',
        'odoo-addon-crm_lead_code>=16.0dev,<16.1dev',
        'odoo-addon-crm_lead_firstname>=16.0dev,<16.1dev',
        'odoo-addon-crm_lead_search_archive>=16.0dev,<16.1dev',
        'odoo-addon-crm_location>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
