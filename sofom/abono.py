# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdpago(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.abono"
    name = fields.Char("Folio del Pago", default=lambda self:
        self.env["ir.sequence"].get("sofom.pago"))
    monto = fields.Float("Monto Total")
    fecha = fields.Date("Fecha del Pago")
    cliente_id = fields.Many2one("res.partner")
    credito_id = fields.Many2one("sofom.credito")
    lineas_ids = fields.One2many("sofom.abono.line", "abono_id",
        string="Desglose")


class jmdabonolineas(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.abono.line"
    name = fields.Char("Concepto")
    monto = fields.Float("Monto")
    numero_pago = fields.Char("Numero de Pago")
    abono_id = fields.Many2one("sofom.abono", string="Abono")
    fecha = fields.Date("Fecha", related="abono_id.fecha")
    folio = fields.Char("Folio del Pago", related="abono_id.name")
    cliente = fields.Char("Cliente", related="abono_id.cliente_id.name")
    credito = fields.Char("Crédito", related="abono_id.credito_id.name")