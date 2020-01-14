import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-crm",
    description="Meta package for oca-crm Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-crm_stage_probability',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
