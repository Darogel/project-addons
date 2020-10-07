from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Tarea(models.Model):
    _name = "cv.tarea"
    _description = "Tareas"

    name = fields.Char(string="Tarea", required=True)
    description = fields.Html(string="Descripción")
    date_init = fields.Date(string="Fecha de Inicio", required=True)
    date_fin = fields.Date(string="Fecha Fin", required=True)
    expired = fields.Selection(selection=[("no_expired","No Expirado"),("expired","Expirado")],
                                string="Tiempo Límite",
                                default="no_expired")
    state = fields.Selection(selection=[("pendiente","Pendiente"),("desarrollo","Desarrollo"),("hecho","Hecho")],
                                string="Estado",
                                default="pendiente", required=True)
    rating = fields.Selection(selection=[("bajo", "Bajo"), ("medio", "Medio"), ("alto", "Alto")],
                             string="Valor",
                             default="bajo", required=True)

    categoria_id = fields.Many2one("cv.categoria", string="Categoria")

    user_id = fields.Many2one("res.users", string="Docente", default=lambda self: self.env.user.id)


    def check_expiry(self):
        today = fields.Date.today()
        lista_tareas = self.env["cv.tarea"].search([])
        for tarea in lista_tareas:
            if tarea.expired == "no_expired" and tarea.date_fin < today:
                tarea.expired == "expired"

        # Presentar vista mi CUenta
    def mis_tareas(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Mis Tareas",
            "res_model": "cv.tarea",
            "res_id": self.env.user.id,
            "target": "self",
            "views": [(False, "kanban")]
        }


class Categoria(models.Model):
    _name = "cv.categoria"
    _description = "Categoria"

    name = fields.Char(string="Nombre", required=True)
    description = fields.Html(string="Descripcion")

class ResUser(models.Model):

    _inherit = "res.users"

    pm_pedagogia = fields.Float(string="Valor Pedagogía", required=True)
    pm_etico = fields.Float(string="Valor Ético", required=True)
    pm_academico = fields.Float(string="Valor Académico", required=True)


    tarea_ids = fields.One2many("cv.tarea", "user_id")

    def vista_tree(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Mis Tareas",
            "res_model": "cv.tarea",
            "res_id": self.env.user.id,
            "target": "self",
            "views": [(False, "kanban")],
            "domain": [["user_id", "=", self.id]]
        }