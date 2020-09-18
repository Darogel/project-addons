# -*- coding: utf-8 -*-

from odoo import models, fields

class ToDo(models.Model):
    _name = "todo.app"
    _description = "Lista de Tareas"

    name = fields.Char(string = "Nombre")
    state = fields.Char(string = "Estado")
    description = fields.Char(string="Descripcion")
    title = fields.Char(string="Titulo")
    price = fields.Char(string="Precio")