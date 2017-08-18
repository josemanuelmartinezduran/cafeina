#-*-coding:utf-8-*-
from openerp import models, fields, api
from datetime import datetime


class jmd_obra(models.Model):
    _inherit = "mail.thread"
    _name = "cf.obra"
    
    @api.one
    def calculate(self):
        ret = {}
        #Primero los conceptos
        for i in self.concepto_ids:
            i.write({'total': float(i.punit * i.cantidad)})
        return ret

    name = fields.Many2one("project.project",  string="Obra")
    inicio = fields.Date("Fecha de Inicio")
    fin = fields.Date("Fecha de finalización")
    concepto_ids = fields.One2many("cf.obra.concepto",  "obra_id",  string="Conceptos")
    estimacion_ids = fields.One2many("cf.estimacion",  "obra_id",  string="Estimaciones")
    
    
class jmd_concepto(models.Model):
    _inherit = "mail.thread"
    _name = "cf.obra.concepto"
    name=fields.Char("Concepto")
    clave = fields.Char("Clave")
    unidad = fields.Char("Unidad")
    categoria = fields.Char("Categoria")
    cantidad = fields.Float("Cantidad")
    punit = fields.Float("Precio Unitario")
    avance = fields.Float("Avance")
    porcentaje = fields.Float("Porcentaje")
    total = fields.Float("Total Proyectado")
    costo_real = fields.Float("Costo Ejercido")
    pgasto = fields.Float("Porcentaje de Gastos")
    obra_id = fields.Many2one("cf.obra",  string="Obra")
    
    
class jmd_estimacion(models.Model):
    _inherit="mail.thread"
    _name="cf.estimacion"
    name = fields.Char("Folio")
    fecha = fields.Date("Fecha")
    total = fields.Float("Total de la Estimación")
    validada = fields.Boolean("Validada")
    junta = fields.Many2one("utils.minuta",  sstring="Minuta de Acuerdos")
    inspeccion_id = fields.Many2one("auditoria",  string="Inspección")
    linea_ids = fields.One2many("cf.estimacion.linea",  "estimacion_id",  string="Lineas")
    obra_id = fields.Many2one("cf.obra",  string="Obra")
    
class jmd_estimacionlinea(models.Model):
    _inherit = "mail.thread"
    _name = "cf.estimacion.linea"
    name = fields.Char("Concepto")
    concepto_id = fields.Many2one("cf.obra.concepto",  string="Aplicar a")
    clave = fields.Char("Clave")
    uom = fields.Char("Unidad")
    cantidad = fields.Float("Cantidad reportada")
    finalizada = fields.Boolean("Finalizada")
    hecho = fields.Float("Cantidad realizada")
    costo = fields.Float("Precio unitario")
    estimacion_id = fields.Many2one("cf.estimacion",  string="Estimacion") 
