# -*- coding: utf-8 -*-
{
    'name': "Integrated Employee Appraisal",

    'summary': """
        This module is meant to be an addon to the employees module to allow for appraisal through the employee app""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Streamline technology Ltd",
    'website': "http://www.streamline.com.ly",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',
    'license':'LGPL-3',
    'application': True,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/employee_appraisal_security.xml',
        'wizard/hr_appraisal_reports_by_employees_views.xml',
        'views/actions.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/res_config_settings_views.xml',
        'data/hr_appraisal_report_sequence.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
