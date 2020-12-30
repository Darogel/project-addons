from logging import info

from odoo import fields, models, api, SUPERUSER_ID
from odoo.exceptions import ValidationError, RedirectWarning, Warning
from datetime import datetime

class Tarea(models.Model):
    _name = "cv.tarea"
    _description = "Tareas"
    _inherit = "mail.thread"

    name = fields.Char(string="Tarea", required=True)
    description = fields.Html(string="Descripción", default="""<p>Tarea creada por: Administrador</p>""", track_visibility="onchange")
    date_init = fields.Date(string="Fecha de Inicio", required=True)
    date_fin = fields.Date(string="Fecha Fin", required=True)
    expired = fields.Selection(selection=[("no_expired","No Expirado"),("expired","Expirado")],
                                string="Tiempo Límite",
                                default="no_expired")

    #Eliminar campo state porque se lo maneja en otra clase Estado.
    state = fields.Selection(selection=[("pendiente","Pendiente"),("desarrollo","Desarrollo"),("hecho","Hecho")],
                                string="Estado",
                                default="pendiente", required=True, track_visibility="onchange")

    rating = fields.Selection(selection=[("bajo", "Bajo"), ("medio", "Medio"), ("alto", "Alto")],
                             string="Valor",
                             default="bajo", required=True)


    categoria_id = fields.Many2one("cv.categoria", string="Categoria", ondelete='restrict', required=True,
                                   default=lambda self: self.env['cv.categoria'].search([], limit=1),
                                   group_expand='_group_expand_stage_ids', track_visibility="onchange")

    user_id = fields.Many2one("res.users", string="Docente", required=True, default=lambda self: self.env.uid)

    informe_id = fields.Many2one("cv.informe", string="Informe")
    
    email = fields.Char(related="user_id.email", string="Correo Electronico")

    evicencia_id = fields.One2many("cv.evidencia", "tareas_ids")

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

class Evidencia(models.Model):
    _name = "cv.evidencia"
    _description = "Evicencias"

    name = fields.Char(required=True, translate=True)
    evidencia = fields.Html(string="Evidencias")

    tareas_ids = fields.Many2one("cv.tarea", string="Tareas")

    _sql_constraints = [
            ('name_unique', 'unique (name)', "Tag name already exists !"),
    ]

class Tag(models.Model):
    _name = "cv.tag"
    _description = "Etiqueta"

    name = fields.Char(required=True, translate=True)
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
            ('name_unique', 'unique(name)', "Tag name already exists !"),
    ]

class ResUser(models.Model):

    _inherit = "res.users"

    us_cat = fields.Selection(
        selection=[("insatisfactorio", "Insatisfactorio"), ("poco_satisfactorio", "Poco Satisfactorio")
                   , ("satisfactorio", "Satisfactorio"), ("destacado", "Destacado")],
        string="Valoracion Cuantitativa", store=True, compute="_compute_valoracion_docente")

    pm_pedagogia = fields.Float(string="Valor Pedagogía", required=True)
    pm_etico = fields.Float(string="Valor Ético", required=True)
    pm_academico = fields.Float(string="Valor Académico", required=True)

    count_tarea = fields.Float(string="Contador", compute="_contador_tareas", store=True)
    tarea_ids = fields.One2many("cv.tarea", "user_id")
    total_val = fields.Float("Total Valoracion", compute="_compute_valoracion_docente", store=True)

    informe_id = fields.One2many("cv.informe", "user_ids")

    @api.depends("tarea_ids")
    def _contador_tareas(self):

        for record in self:
            mes = datetime.now().year
            movs = record.tarea_ids.filtered(
                lambda r: r.create_date.year == mes)
            record.count_tarea = len(movs)

    @api.constrains('pm_academico')
    def _check_pm_academico(self):
        #for record in self:
            if self.pm_academico < 0:
                raise ValidationError("Valor académico no puede ser Negativo")

    @api.constrains('pm_etico')
    def _check_pm_etico(self):
        #for record in self:
            if self.pm_etico < 0:
                raise ValidationError("Valor Etico no puede ser Negativo")

    @api.constrains('pm_pedagogia')
    def _check_pm_pedagogia(self):
        #for record in self:
            if self.pm_pedagogia < 0:
                raise ValidationError("Valor pedagogía no puede ser Negativo")

    @api.depends('total_val', 'pm_academico', 'pm_etico', 'pm_pedagogia',
                 'us_cat')
    def _compute_valoracion_docente(self):
        for record in self:
            total_valor = record.pm_academico + record.pm_etico + record.pm_pedagogia

        if total_valor >= 0 and total_valor <= 40:
            us_cat = "insatisfactorio"
        elif total_valor > 40 and total_valor <= 60:
            us_cat = "poco_satisfactorio"
        elif total_valor > 60 and total_valor <= 80:
            us_cat = "satisfactorio"
        elif total_valor > 80 and total_valor <= 100:
            us_cat = "destacado"
        else:
            raise ValidationError("El valor esta fuera de rango (0-100)")
        record.total_val = total_valor
        record.us_cat = us_cat

    def vista_tree(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Plan Actividades",
            "res_model": "cv.informe",
            "docente": self.id,
            "views": [(False, "kanban"),(False, "tree")],
            "target": "self",
            "context": {"id_def": self.id}
        }


class Informe(models.Model):
    _name = "cv.informe"
    _description = "Informe"

    name = fields.Char(required=True, translate=True)
    date_init = fields.Date(string="Fecha de Inicio", required=True)
    date_fin = fields.Date(string="Fecha Fin", required=True)
    objetivo = fields.Char(string="Objetivos")
    conclusion = fields.Html(string="Conclusion")

    estado_Inicializar = fields.Boolean(default=True)

    estado_Comunicar = fields.Boolean(default=False)

    tarea_ids = fields.One2many("cv.tarea", "informe_id")

    user_ids = fields.Many2one("res.users", string="Docente")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Nombre name already exists !"),
    ]


    def inicializar(self):
        active_ids = self.ids
        print(active_ids)
        lista_tareas = self.env["cv.tarea"].search([])
        lista_docentes = self.env["res.users"].search([])




        print(len(lista_docentes))
        print(len(lista_tareas))
        for tarea in lista_tareas:
            print(tarea.informe_id.id)
            print(active_ids[0])
            for docente in lista_docentes:
                if int(active_ids[0]) == int(tarea.informe_id):
                    print("Entro")
                    if docente.name != "Administrator":
                        self.env["cv.tarea"].create({"name": tarea.name, "date_init": tarea.date_init,
                                                 "date_fin": tarea.date_fin, "state": tarea.state,
                                                 "rating": tarea.rating, "categoria_id": '1',
                                                 "user_id": docente.id, "informe_id": active_ids[0]})
                    else:
                        print("Admin")
                    # print(tarea.id)
                    # print(tarea.name)
                else:
                    print("No Entro")

        self.env["cv.informe"].browse(active_ids[0]).write({"estado_Inicializar": True})
        self.env.cr.commit()
        raise Warning('Las actividades se mostraran a los docentes y se enviará una '
                      'notificación de la inicialización del Plan Mejoras.')

    def return_confirmation(self):
        return {
            'name': 'Are you sure?',
            'type': 'ir.actions.act_window',
            'res_model': 'cv.confirm_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new'
        }


    def canceled_progressbar(self):

        if (self.return_confirmation()):
            print("HOla")
        else:
            print("Chao")

    def comunicar(self):
        active_ids = self.ids
        #self.env["cv.informe"].browse(active_ids[0]).write({"estado_Inicializar": False})
        #self.env["cv.informe"].browse(active_ids[0]).write({"estado_Comunicar": True})
        #self.env.cr.commit()
        action = self.env.ref('mail.action_discuss')
        msg = ('Está seguro que desea comunicar el Plan Mejoras?\n Recuerde que debe socializarlo.')
        raise RedirectWarning(msg, action.id, ('Ir a  comunicar el Plan Mejoras'), 'dsa')




    def vista_tree_tareas(self):
        id_def = self.env.context.get('id_def');
        return {
            "type": "ir.actions.act_window",
            "name": "Tareas",
            "res_model": "cv.tarea",
            "views": [(False, "kanban"),(False, "form"),(False, "tree")],
            "target": "self",
            "domain": [["informe_id", "=", self.id], ["user_id", "=", id_def]]
        }

class confirm_wizard(models.TransientModel):
    _name = 'cv.confirm_wizard'

    yes_no = fields.Char(default='Do you want to proceed?')
    

    def yes(self):
        return True


    def no(self):
        return False












