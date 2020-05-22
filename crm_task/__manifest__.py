# Copyright 2020 Adgensee - Vincent Garcies
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Project tasks from CRM opportunities',
    'version': '12.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Create related tasks from your opportunities',

    'author': 'Adgensee,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/crm',

    'license': 'AGPL-3',

    'depends': [
        'crm',
        'project',
        'hr_timesheet',
    ],
    'data': [
        'views/project_task.xml',
        'views/crm_lead.xml',
    ],
    'demo': [],

    'installable': True,
}
