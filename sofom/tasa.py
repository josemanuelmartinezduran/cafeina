# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdtasa(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.tasa"
    name = fields.Float("Tasa")
    producto = fields.Selection([("micro", "Microcrédito"),
        ("nom", "Nómina")], string="Producto")
    ciclo = fields.Integer("Ciclo")
    tipo = fields.Selection([("no", "Principal"),
        ("si", "Interciclo"), ('an', "Anticipo de Nómina")], string="Tipo")