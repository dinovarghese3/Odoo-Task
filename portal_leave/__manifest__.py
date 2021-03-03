# -*- coding: utf-8 -*-
{
    'name': "Leave Request From Website",
    'summary': """
            Leave Request From Website for  Portal  users""",

    'author': "Dino Varghese",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website/Website',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'hr_holidays'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/leave_request_template.xml',
        'views/leave_request_sucess.xml',
        'views/link_js_website.xml',
    ],
    # only loaded in demonstration mode

}
