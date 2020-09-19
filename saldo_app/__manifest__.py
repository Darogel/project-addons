{
    "name":"Saldo APP",
    "description":"Aplicacion WEB para registrar ingresos y egresos",
    "author":"Darwin Rogel - Robin Cordova",

    "summary": """
        Este es un modulo de prueba del curso de Odoo 13
        Permite registrar los ingresos y egresos de los clientes
        """,

    "website": "https://escuelafullstack.com",

    "category": 'Ventas',

    "version":"1.0",
    "depends":["base"],
    "data":[
        "security/ir_model_access.xml",
        "views/views.xml"
    ]
}