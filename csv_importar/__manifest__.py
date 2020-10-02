{
    "name":"CSV Importar Docentes",
    "description":"Aplicacion para el registro de docentes mediante csv",
    "author":"Darwin Rogel - Robin Cordova",

    "summary": """
        Este es un modulo de prueba del curso de Odoo 13
        Permite el registro de usuarios mediante csv
        """,

    "website": "https://www.google.com",

    "category": 'Prueba',

    "version":"1.0",
    "depends":["base"],
    "data":[
        "security/res_groups.xml",
        "security/ir_rule.xml",
        "security/ir_model_access.xml",
        "views/views.xml",
    ]
}