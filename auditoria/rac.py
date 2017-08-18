# -*- coding: utf-8 -*-
#Fixed By JMD #IStandForFreedom
from openerp import models, fields, api
import datetime


class rac(models.Model):
    _name = 'rac'
    _inherit = "mail.thread"

    def action_abierta(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'abierta'})
            return True

    def action_cerrar(self, cr, uid, ids):
            print("Cerrando")
            self.write(cr, uid, ids, {'state': 'cerrada'})
            return True

    @api.one
    def save(self):
        self.create({})

    @api.model
    def default_get(self, vals):
        res = super(rac, self).default_get(vals)
        pregunta = self._context.get("pregunta", False)
        auditoria = self._context.get("auditoria_id", False)
        res.update({'pregunta': pregunta, 'auditoria': auditoria})
        return res

    @api.one
    def get_avance(self):
        avance = 0
        for i in self.acciones:
            if i.realizado:
                avance += i.peso
        self.avance = avance

    name = fields.Char('Nombre', required=True, default=lambda
        self: self.env["ir.sequence"].get("rac"))
    auditoria = fields.Many2one('auditoria', string='Auditoria de Origen')
    auditor = fields.Many2many('hr.employee', string='Auditor')
    pregunta = fields.Char("Pregunta")
    fecha_reporte = fields.Datetime('Fecha de reporte', default=lambda *a:
        datetime.date.today().strftime('%Y-%m-%d'))
    fecha_limite = fields.Datetime('Fecha limite')
    prioridad = fields.Selection([('baja', 'Baja'), (' media', 'Media'),
            ('alta', 'Alta')], 'Prioridad')
    responsable = fields.Many2one('hr.employee', string='Responsable')
    informacion = fields.One2many('rac.informacion', 'relation',
            string='Obsrevación')
    acciones = fields.One2many('rac.acciones', 'relation_rac',
            'Acciones')
    state = fields.Selection([('abierta', 'Abierta'), ('cerrada',
            'Cerrada')], "Estado", readonly=True)
    resultado_id = fields.Many2one("auditoria.resultado", string="Pregunta")
    peso = fields.Float("Ponderacion (%) ")
    avance = fields.Float("Avance", compute=get_avance)


class rac_informacion(models.Model):
    _name = 'rac.informacion'
    name = fields.Char('Observación')
    comentarios = fields.Char('Comentarios')
    relation = fields.Many2one("rac")
    emisor = fields.Many2one("hr.employee", string="Emisor")
    receptor = fields.Many2one("hr.employee", string="Receptor")


class rac_acciones(models.Model):
    _name = 'rac.acciones'
    name = fields.Char('Accion')
    persona = fields.Many2one('hr.employee', string='Persona')
    fecha = fields.Date('Fecha')
    horas_dedicadas = fields.Integer('Horas dedicadas')
    relation_rac = fields.Many2one("rac", string="Relacion con RAC",
            ondelete="set null")
    tipo = fields.Selection([('preventiva', 'Preventiva'),
            ('correctiva', 'Correctiva'), ('inmediata',
            'Correctiva Inmediata')], string="Tipo")
    realizado = fields.Boolean("Realizado")
    peso = fields.Float("Peso (%)")