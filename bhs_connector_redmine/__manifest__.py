# -*- coding: utf-8 -*-
{
    'name': 'Redmine Integration',
    'version': '1.0',
    'author': 'Bac Ha Software',
    'website': 'https://bachasoftware.com',
    'maintainer': 'Bac Ha Software',
    'category': 'Extra Tools',
    'summary': "You can sync data spent time from redmine to time sheet odoo.",
    'description': "You can syns data spent time from redmine to time sheet odoo",
    'depends': ['hr_timesheet', 'bhs_odoo_slack'],
    'data': [
        'security/ir.model.access.csv',
        'data/redmine_api_data.xml',
        'data/redmine_spent_time_email_template.xml',
        'views/res_config_settings_views.xml',
        'views/hr_department_view.xml',
        'views/bh_api_logs_views.xml',
    ],
    'external_dependencies': {
        'python': ['python-redmine'],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}