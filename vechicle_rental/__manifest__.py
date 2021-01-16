# -*- coding: utf-8 -*-
{
    'name': 'Vehicle Rental',

    'summary': """
        Vehicle Rental module """,

    'author': "Dino Varghese",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet','account'],
    'images': ['static/description/icon.png'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/product_demo.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/sequence.xml',
        'views/rent_request.xml',
        'views/rent_vehicle.xml',
        'views/registration_date_fleet.xml',
    ],
    # only loaded in demonstration mode

    'installable': True,
    'application': True,
    'auto_install': False,
}
