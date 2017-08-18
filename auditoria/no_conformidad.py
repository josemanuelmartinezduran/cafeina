# -*- coding: utf-8 -*-
#Fixed By JMD #IStandForFreedom
from openerp import models, fields, api


class no_conformidad(models.Model):
    _name = 'no_conformidad'
    _inherit = "mail.thread"

    @api.model
    def default_get(self, vals):
        res = super(no_conformidad, self).default_get(vals)
        pregunta = self._context.get("pregunta", False)
        auditoria = self._context.get("auditoria_id", False)
        res.update({'pregunta': pregunta, 'auditoria_id': auditoria})
        return res

    @api.one
    def save(self):
        self.create({})

    @api.multi
    def genera_accion(self):
        print("Generando")
        rac_form = self.env.ref('auditoria.rac_view_form', False)
        ctx = dict(
            pregunta=self.name,
            auditoria_id=self.auditoria_id.id,
        )
        return {
            'name': "Acción Correctiva",
            'type': 'ir.actions.act_window',
            'res_model': 'rac',
            'views': [(rac_form.id, 'form')],
            'view_id': rac_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx,
            }

    def action_generada(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'generada'})
            return True

    def action_validada(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'validada'})
            return True

    def action_resuelta(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'resuelta'})
            return True

    name = fields.Char('Clave', required=True, default=lambda
        self: self.env["ir.sequence"].get("no_conformidad"))
    tipo = fields.Selection([('Menor', 'Menor'), ('Mayor', 'Mayor'),
        ('Hallazgo', 'Hallazgo')])
    auditoria_id = fields.Many2one("auditoria", string="Auditoría")
    pregunta = fields.Char("Pregunta")
    generador = fields.Many2one('hr.employee', string='Generador')
    gnombre = fields.Char(string="Nombre")
    responsable = fields.Many2one('hr.employee', string='Responsable')
    rnombre = fields.Char("Nombre")
    jefe_del_responsable = fields.Many2one('hr.employee',
            string='Jefe del responsable')
    jnombre = fields.Char(string="Nombre")
    area = fields.Many2one("hr.department", string="Departamento")
    fecha = fields.Date('Fecha')
    prioridad = fields.Selection([('baja', 'Baja'), ('media', 'Media'),
            ('alta', 'Alta')], 'Prioridad')
    state = fields.Selection([('generada', 'Generada'),
            ('validada', 'Validada'), ('resuelta', 'Resuelta')], 'Estado')
    descripcion = fields.Text('Descripcion')
    acciones = fields.One2many('no_conformidad.acciones',
             'relation_no_confomidad', 'Acciones')
    consecuencias = fields.Text("Consecuencias")
    concepto = fields.Char("Concepto")


class acciones(models.Model):
    _name = 'no_conformidad.acciones'
    name = fields.Char(string="Nombre", size=40)
    persona = fields.Many2one('hr.employee', string='Empleado')
    nombre = fields.Char(string="Nombre")
    accion = fields.Char('Accion')
    fecha = fields.Date('Fecha')
    horas_dedicas = fields.Boolean('Realizado')
    relation_no_confomidad = fields.Many2one("no_conformidad",
            string="Relacion con no conformidad", ondelete="set null")