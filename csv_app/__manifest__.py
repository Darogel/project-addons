{
    "name": "CSV APP",
    "description":"Aplicacion WEB para registrar docentes automaticamente por csv",
    "author": "Darwin Rogel - Robin Cordova",

    "summary": """
        Este es un modulo de prueba del curso de Odoo 13
        Permite registrar los ingresos y egresos de los clientes
        """,

    "website": "https://escuelafullstack.com",

    "category": "Ventas",

    "version": "1.0",
    "depends": ["base"],
    "data": [
        "data/quotation_expiration_cron.xml",
        "security/res_groups.xml",
        "security/ir_rule.xml",
        "security/ir_model_access.xml",
        "views/views.xml"

    ]
}