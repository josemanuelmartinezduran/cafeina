# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdetemplate(models.Model):
    _inherit = "mail.thread"
    _name = "evaluacion.template"
    name = fields.Char("Descripción")
    tipo = fields.Many2one("evaluacion.tipo", string="Tipo")
    pregunta_ids = fields.One2many("evaluacion.template.pregunta",
        string="Preguntas")


class jmdaccount(models.Model):
    _name = "evaluacion.template.pregunta"
    _inherit = "mail.thread"
    name = fields.Char("Pregunta")
    source = fields.Char("Fuente de información")


class jmdaccount(models.Model):
    _name = "evaluacion.tipo"
    _inherit = "mail.thread"
    name = fields.Char("Nombre")