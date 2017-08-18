# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdaccount(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.plazo"
    name = fields.Char("Plazo")
    producto = fields.Selection([("micro", "Microcrédito"),
        ("nom", "Nómina")], string="Producto")
    ciclos_anio = fields.Integer("Ciclos por Año")
    dias_ciclo = fields.Integer("Días entre el ciclo")
    meses_ciclo = fields.Integer("Meses entre ciclos")
    frecuencia = fields.Selection([("26", "Quincenal"), ("52", "Semanal"),
        ("12", "Mensual")], string="Frecuencia")
    destino = fields.Many2one("sofom.destino", string="Destino de Crédito")
    monto_max = fields.Float("Monto Máximo")
    pagos = fields.Integer("Pagos")