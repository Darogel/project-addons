from odoo import fields, models

class Movimiento(models.Model):
    _name = "sa.movimiento" #sa_movimiento
    _description = "Movimiento"

    name = fields.Char(string="Nombre", required=True)
    type_mov = fields.Selection(selection=[("ingreso","Ingreso"),("gasto","Gasto")], string="Tipo",default="ingreso",required=True)
    date = fields.Datetime(string="Fecha")
    amount = fields.Float(string="Monto")
    receipt_image = fields.Binary(string="Foto del recibo")
    notas = fields.Html(string="Notas")
    #Relaciones
    user_id = fields.Many2one("res.users", string="Usuario")
    category_id = fields.Many2one("sa.categoria",string="Categoria")
    tag_ids = fields.Many2many("sa.tag","sa_mov_sa_tag_rel","move_id","tag_id")

class Category(models.Model):
    _name = "sa.categoria"
    _description = "Categoria"

    name = fields.Char(string="Nombre")

class Tag(models.Model):
    _name = "sa.tag"
    _description = "Tag"

    name = fields.Char(string="Nombre")

class ResUser(models.Model):
    _inherit = "res.users"

    movimiento_ids = fields.One2many("sa.movimiento","user_id")
