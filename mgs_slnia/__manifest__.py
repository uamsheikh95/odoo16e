# -*- coding: utf-8 -*-
{
    'name': "MGS SLNIA System",

    'summary': """
    """,

    'description': """
    """,

    'author': "Meisour GS",
    'website': "http://www.meisour.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Insurance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/config.xml',
        'views/partner.xml',
        'views/registeration.xml',
        'views/mgs_slnia_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
