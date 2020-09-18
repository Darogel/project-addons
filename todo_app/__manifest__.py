# -*- coding: utf-8 -*-
{
    'name': "Todo App",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        Modulo de Prueba del curso de Odoo Full Stack   
        """,

    'description': """
        Long description of module's purpose
        Escuela FullStack Odoo 13
    """,

    'author': "Darwin Rogel",
    'website': "http://www.google.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localizacion',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
