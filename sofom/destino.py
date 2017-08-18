# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdaccount(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.destino"
    name = fields.Char("Nombre")
    destino = fields.Char("Destino del Crédito")
    producto = fields.Selection([("micro", "Microcrédito"),
        ("nom", "Nómina")], string="Producto")
    interciclo = fields.Selection([('si', 'Si'),
        ('no', 'No'), ('an', 'Anticipo de Nómina')],
        "Interciclo", default='no')