#-*-coding:utf-8-*-
from openerp import models, fields, api
from datetime import datetime

#Minutas
class jmd_minuta(models.Model):
    _inherit = "mail.thread"
    _name = "utils.minuta"
    name = fields.Char("Consecutivo",  default=lambda self: self.env["ir.sequence"].get("utils.minuta"))
    hora_inicio = fields.Datetime("Hora Inicio")
    hora_fin = fields.Datetime("Hora Fin")
    lugar = fields.Char("Lugar")
    responsable_id = fields.Many2one("hr.employee",  string="Responsable")
    objetivo = fields.Char("Objetivo")
    acuerdos = fields.Text("Acuerdos")
    estado = fields.Selection([("Abierta",  "Abierta"),  ("Cerrada",  "Cerrada")])
    asistentes = fields.Many2many("res.partner",  string="Asistentes")
    proyecto_id = fields.Many2one("project.project", "Proyecto")
    asuntos_ids = fields.One2many("utils.minuta.asunto",  "minuta_id",  string="Asuntos")
    
    
class jmd_asunto(models.Model):
    _inherit = "mail.thread"
    _name = "utils.minuta.asunto"
    name = fields.Char("Consecutivo")
    descripcion = fields.Char("Descripción")
    responsable = fields.Many2one("hr.employee",  string="Responsable")
    fecha_limite = fields.Date("Fecha Límite")
    vuelta = fields.Integer("Vuelta",  default=1)
    horas_dedicadas = fields.Float("Horas Dedicadas")
    realizado = fields.Boolean("Realizado")
    comentarios = fields.Text("Comentarios")
    prioridad = fields.Selection([("Alta",  "Alta"),  ("Media",  "Media"),  ("Baja",  "Baja")], string="Prioridad")
    pasos = fields.Char("Pasos a seguir")
    minuta_id = fields.Many2one("utils.minuta")
