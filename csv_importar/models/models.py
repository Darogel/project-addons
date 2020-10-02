from odoo import fields, models
from odoo.exceptions import ValidationError

#Clase de las Tareas
class Tareas(models.Model):
    _name = "cs.tarea"
    _description = "Tareas"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Html(string="Descripcion")
    date_init = fields.Date(string="Fecha inicio", required=True)
    date_fin = fields.Date(string="Fecha fin", required=True)
    rating = fields.Selection(selection=[("bajo","Bajo"),("medio","Medio"),("alto","Alto")], string="Calificacion", default="medio", required=True)
    state = fields.Selection(selection=[("pendiente","Pendiente"),("desarrollo","Desarrollo"),("hecho","Hecho")], string="Estado",default="pendiente", required=True)

    #Relaciones
    categoria_id = fields.Many2one("cs.categoria", string="Categoria")
    user_id = fields.Many2one("res.users", string="Usuario", default=lambda self:self.env.user.id)

#Clase de las categorias
class Categorias(models.Model):
    _name = "cs.categoria"
    _description = "Categoria"

    name = fields.Char(string="Nombre", required=True)
    desciption = fields.Html(string="Descripcion")

#clase de Los usuarios de la APP
class ResUser(models.Model):
    _inherit = "res.users"

    pl_pedagogia = fields.Float(string="Valor Pedagogia", required=True)
    pl_etico = fields.Float(string="Valor Etico", required=True)
    pl_academico = fields.Float(string="Valor Academico", required=True)

    #Relaciones
    tareas_ids = fields.One2many("cs.tarea", "user_id")