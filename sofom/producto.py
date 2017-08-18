# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdproducto(models.Model):
    _inherit = "product.template"
    is_financial = fields.Boolean("Es Financiero")
    attribute_ids = fields.One2many("product.financial.line", "template_id",
        string="Atributos")


class jmdpproduct(models.Model):
    _inherit = "product.product"
    is_financial = fields.Boolean("Es Financiero")
    attribute_ids = fields.One2many("product.financial.line", "product_id",
        string="Atributos")


class jmdatributo(models.Model):
    _name = "product.financial.line"
    name = fields.Char("Nivel")
    minimo = fields.Float("Minimo")
    maximo = fields.Float("Máximo")
    tasa = fields.Float("Tasa")
    plazo = fields.Integer("Plazo (meses)")
    product_id = fields.Many2one("product.product", string="Producto")
    template_id = fields.Many2one("product.template", string="Plantilla")