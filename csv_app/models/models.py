from odoo import fields, models, api, SUPERUSER_ID
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

    categoria_id = fields.Many2one("cv.categoria", string="Categoria", ondelete='restrict', required=True,
                                   default=lambda self: self.env['cv.categoria'].search([], limit=1),
                                   group_expand='_group_expand_stage_ids')

    user_id = fields.Many2one("res.users", string="Docente", required=True, default=lambda self: self.env.uid)

    tag_ids = fields.Many2many(
        'cv.tag', 'cv_tag_rel',
        'tag_id', 'tarea_id', string='Tags')

    @api.model
    def _group_expand_stage_ids(self, stages, domain, order):
        """ Read group customization in order to display all the stages in the
            kanban view, even if they are empty
        """
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def check_expiry(self):
        today = fields.Date.today()
        lista_tareas = self.env["cv.tarea"].search([])
        for tarea in lista_tareas:
            if tarea.expired == "no_expired" and tarea.date_fin < today:
                tarea.expired = "expired"

class Categoria(models.Model):
    _name = "cv.categoria"
    _description = "Categoria"
    _order = 'sequence'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Html(string="Descripcion")
    sequence = fields.Integer()


class Tag(models.Model):
    _name = "cv.tag"
    _description = "Etiqueta"

    name = fields.Char(required=True, translate=True)
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]

class ResUser(models.Model):

    _inherit = "res.users"

    us_cat = fields.Selection(
        selection=[("insatisfactorio", "Insatisfactorio"), ("poco_satisfactorio", "Poco Satisfactorio")
                   , ("satisfactorio", "Satisfactorio"), ("destacado", "Destacado")],
        string="Valoracion Cuantitativa",
        required=True, compute="_compute_valoracion_docente")
    pm_pedagogia = fields.Float(string="Valor Pedagogía", required=True)
    pm_etico = fields.Float(string="Valor Ético", required=True)
    pm_academico = fields.Float(string="Valor Académico", required=True)


    tarea_ids = fields.One2many("cv.tarea", "user_id")
    total_val = fields.Float("Total Valoracion", compute="_compute_valoracion_docente")


    #@api.depends("user_id")
    def _compute_valoracion_docente(self):
        for record in self:
            record.total_val = record.pm_academico + record.pm_etico + record.pm_pedagogia
        if record.total_val >= 0 and record.total_val <= 40:
            record.us_cat = "insatisfactorio"
        elif record.total_val > 40 and record.total_val <= 60:
            record.us_cat = "poco_satisfactorio"
        elif record.total_val > 60 and record.total_val <= 80:
            record.us_cat = "satisfactorio"
        elif record.total_val > 80 and record.total_val <= 100:
            record.us_cat = "destacado"
        elif record.total_val < 0 or record.total_val > 100:
            raise ValidationError("El valor esta fuera de rango (0-100)")

    def vista_tree(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Tareas",
            "res_model": "cv.tarea",
            "views": [(False, "kanban"),(False, "form"),(False, "tree")],
            "target": "self",
            "domain": [["user_id", "=", self.id]]
        }