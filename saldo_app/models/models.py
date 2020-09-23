from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Movimiento(models.Model):
    _name = "sa.movimiento" #sa_movimiento
    _description = "Movimiento"
    _inherit = "mail.thread"

    name = fields.Char(string="Nombre", required=True)
    type_mov = fields.Selection(selection=[("ingreso","Ingreso"),("gasto","Gasto")], string="Tipo",default="ingreso",required=True)
    date = fields.Date(string="Fecha")
    amount = fields.Float(string="Monto", track_visibility="onchange")
    receipt_image = fields.Binary(string="Foto del recibo")
    notas = fields.Html(string="Notas")

    #Relaciones
    user_id = fields.Many2one("res.users", string="Usuario", default=lambda self:self.env.user.id)
    category_id = fields.Many2one("sa.categoria",string="Categoria")
    tag_ids = fields.Many2many("sa.tag","sa_mov_sa_tag_rel","move_id","tag_id")
    currency_id = fields.Many2one("res.currency", default=2)
    email = fields.Char(related="user_id.email", string="Correo Electronico")

    #Funcion para controlar limite de monto
    @api.constrains("amount")
    def _check_amount(self):
        if not(self.amount >=0 and self.amount <= 1000000):
            raise ValidationError("El monto deber ser entre 0 y 1000000")

    #Funcion para cambiar descripcion del movimiento
    @api.onchange("type_mov")
    def onchange_type_move(self):
        if self.type_mov == "ingreso":
            self.name = "Ingreso: "
            self.amount = 50
        elif self.type_mov == "gasto":
            self.name = "Egreso: "
            self.amount = 100

    #Sobrecarga de Create
    @api.model
    def create(self, vals):
        name = vals.get("name","-")
        amount = vals.get("amount","0")
        type_mov = vals.get("type_mov","")
        date = vals.get("date", "")
        notas = """<p>Tipo de Movimiento: {}</p><p>Nombre: {}</p><p>Monto: {}</p><p>Fecha: {}<br></p>"""
        vals["notas"] = notas.format(type_mov, name, amount, date)
        return super(Movimiento, self).create(vals)

    def unlink(self):
        for record in self:
            if record.amount>=50:
                raise ValidationError("Movimientos con montos mayores a 50 NO pueden ser eliminados")
        return super(Movimiento, self).unlink()


class Category(models.Model):
    _name = "sa.categoria"
    _description = "Categoria"

    name = fields.Char(string="Nombre")
    type_mov = fields.Selection(selection=[("ingreso","Ingreso"),("gasto","Gasto")], string="Tipo",default="ingreso",required=True)

    #Funcion para Modal de cada Movimiento
    def ver_movimientos(self):
        return {
            "type":"ir.actions.act_window",
            "name":"Movimientos de Categoria: "+self.name,
            "res_model":"sa.movimiento",
            "views":[[False, "tree"]],
            "target":"new",
            #"target": "self",
            "domain":[["category_id","=",self.id]]
        }

class Tag(models.Model):
    _name = "sa.tag"
    _description = "Tag"

    name = fields.Char(string="Nombre")
    type_mov = fields.Selection(selection=[("ingreso","Ingreso"),("gasto","Gasto")], string="Tipo",default="ingreso",required=True)

class ResUser(models.Model):
    _inherit = "res.users"

    movimiento_ids = fields.One2many("sa.movimiento","user_id")
    currency_id = fields.Many2one("res.currency", default=2)
    total_ingresos = fields.Float("Total de Ingresos", compute="_compute_movimientos")
    total_egresos = fields.Float("Total de Egresos", compute="_compute_movimientos")

    #Funcion para el calculo total de ingresos y egresos
    @api.depends("movimiento_ids")
    def _compute_movimientos(self):
        for record in self:
            record.total_ingresos = sum(record.movimiento_ids.filtered(lambda r:r.type_mov =='ingreso').mapped("amount"))
            record.total_egresos = sum(record.movimiento_ids.filtered(lambda r: r.type_mov == 'gasto').mapped("amount"))

    #Funcion para Presentar vista Mi cuenta
    def mi_cuenta(self):
        return {
            "type":"ir.actions.act_window",
            "name":"Mi Cuenta",
            "res_model":"res.users",
            "res_id":self.env.user.id,
            "target":"self",
            "views":[(False, "form")]
        }