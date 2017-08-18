# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdcolonia(models.Model):
    _inherit = "mail.thread"
    _name = "utils.colonia"
    name = fields.Char("Nombre")
    tipo = fields.Char("Tipo")
    cp = fields.Integer("Codigo Postal")
    estado = fields.Char("Estado")
    municipio = fields.Char("Municipio")
    ciudad = fields.Char("Ciudad")