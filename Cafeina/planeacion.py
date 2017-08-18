#-*-coding:utf-8-*-
from openerp import models, fields, api
from datetime import datetime

#planeacion
class jmd_cf_planeacion(models.Model):
    _inherit = "mail.thread"
    _name = "cf.planeacion"
    name = fields.Many2one("project.project", string="Nombre del Proyecto")
    #cuestionario_kickoff = fields.Many2one("auditoria",  string="Cuestionario KickOff")
    checklist_entrega = fields.Many2one("auditoria",  string="Checklist de Entrega")
    junta_inicial = fields.Many2one("utils.minuta",  string="Junta Inicial")
    obra = fields.Many2one("cf.obra",  string="Obra")
    corrida = fields.Many2one("obra.financiera",  string="Corrida Financiera")
    junta_financiera = fields.Many2one("utils.minuta",  string="Junta Finanzas")
