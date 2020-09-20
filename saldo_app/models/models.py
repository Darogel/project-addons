from odoo import fields, models

class Movimiento(models.Model):
    _name = "sa.movimiento" #sa_movimiento
    _description = "Movimiento"

    name = fields.Char("Nombre")
    type_mov = fields.Selection(selection=[("ingreso","Ingreso"),("gasto","Gasto")])
    date = fields.Datetime("Fecha")
    amount = fields.Float("Monto")
    receipt_image = fields.Binary("Foto del recibo")
    #Relaciones
    user_id = fields.Many2one("res.users", string="Usuario")
    category_id = fields.Many2one("sa.categoria","Categoria")

class Category(models.Model):
    _name = "sa.categoria"
    _description = "Categoria"

    name = fields.Char("Nombre")

class Tag(models.Model):
    _name = "sa.tag"
    _description = "Tag"

    name = fields.Char("Nombre")

class ResUser(models.Model):
    _inherit = "res.users"

    movimiento_ids = fields.One2many("sa.movimiento","user_id")
