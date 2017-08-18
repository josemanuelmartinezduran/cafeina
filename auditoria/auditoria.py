# -*- coding: utf-8 -*-
#IStandForFreedom
from openerp import models, fields, api
from datetime import date


class auditoria(models.Model):
    _name = 'auditoria'
    _inherit = "mail.thread"

    def action_planeacion(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'planeacion'})
            return True

    def generate_rac(self, cr, uid, ids, context=None):
        ret = {}
        rac_obj = self.pool.get("rac")
        for i in self.browse(cr, uid, ids, context):
            rac_obj.create(cr, uid, {
                    'name': i.name,
                    'auditoria': i.id,
                })
        return ret

    def action_ejecucion(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            for j in i.checklist.preguntas:
                self.pool.get("auditoria.resultado").create(cr, uid, {
                    'name': j.pregunta,
                    'categoria': j.categoria, 
                    'referencia': j.valor_referencia,
                    'tipo': j.tipo_respuesta,
                    'aprobado': False,
                    'state': 'abierta',
                    'relation': i.id})
        self.write(cr, uid, ids, {'state': 'ejecucion'})
        return True

    def action_cierre(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'cierre'})
        return True

    @api.one
    @api.onchange('checklist')
    @api.depends('checklist')
    def onchange_checklist(self):
        print("Mi ID es")
        print((str(self.id)))
        print((str(self.name)))
        id_res = self.write({})
        print((str(id_res)))
        if self.resultado_ids:
            for i in self.resultado_ids:
                i.unlink()
        return True

    id_auditoria = fields.Integer('id_auditoria')
    name = fields.Char('Nombre', required=True, default=lambda self:
            self.env["ir.sequence"].get("auditoria"))
    auditores = fields.Many2many('hr.employee', string='Nombre')
    inicio = fields.Datetime('Fecha de inicio')
    fin = fields.Datetime('Fecha de fin')
    state = fields.Selection([('planeacion', 'Planeacion'),
            ('ejecucion', 'En ejecucion'), ('cierre', 'Cierre')], 'Estado')
    tipo_auditoria = fields.Many2one("auditoria.tipo",
        string="Tipo de Auditoria")
    planeacion = fields.One2many('auditoria.planeacion', 'relation',
            'Planeacion')
    objetivo = fields.Text('Objetivo de la auditoria')
    resultado_ids = fields.One2many("auditoria.resultado", "relation",
            string="Resultados")
    alcance = fields.Text("Alcance")
    checklist = fields.Many2one("auditoria.checklist", string="Checklist")
    no_conformidad = fields.One2many("no_conformidad", "auditoria_id",
        string="No Conformidad")
    acciones = fields.One2many("rac", "auditoria", string="Acciones")


class jmdaudittipo(models.Model):
    _name = "auditoria.tipo"
    name = fields.Char("Nombre")


class auditoria_planeacion(models.Model):
    _name = 'auditoria.planeacion'
    id_planeacion = fields.Integer('Id')
    fecha = fields.Datetime('Fecha', required=True)
    auditor = fields.Many2one('hr.employee', string='Auditor',
            required=True)
    anombre = fields.Char(string="Nombre")
    sujeto = fields.Many2one('hr.employee', string='Sujeto')
    nombre = fields.Char(string="Nombre")
    checklist = fields.Many2one('auditoria.checklist', string='Checklist')
    aprobado = fields.Selection([('si', 'Si'), ('no', 'No')], 'Aprobado')
    observaciones = fields.Text('Observaciones')
    relation = fields.Many2one("auditoria")


class auditoria_checklist(models.Model):
    _name = 'auditoria.checklist'

    def action_borrador(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'borrador'})
            return True

    def action_aprobado(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'aprobado'})
            return True

    id_checklist = fields.Integer('Id')
    name = fields.Char('Nombre')
    preguntas = fields.One2many('auditoria.checklist_preguntas',
            'relation', 'Preguntas')
    creador = fields.Many2one("hr.employee", string="Creador de la lista")
    fecha = fields.Date("Fecha de creación", default=lambda *a:
        date.today().strftime('%Y-%m-%d'))
    state = fields.Selection([('borrador', 'Borrador'),
            ('aprobado', 'Aprobado')], "Estado", readonly=True)


class auditoria_checklist_preguntas (models.Model):
    _name = 'auditoria.checklist_preguntas'

    id_pregunta = fields.Integer('Id')
    categoria = fields.Char("Categoria")
    pregunta = fields.Char('Pregunta', size=120)
    tipo_respuesta = fields.Selection([('sino', 'Si/No'),
        ('num', 'Numerico'), ("abierta", "Abierta")], 'Tipo de respuesta')
    valor_referencia = fields.Char('Valor Esperado')
    relation = fields.Many2one("auditoria.checklist")
    fisico = fields.Boolean("Físico")
    digital = fields.Boolean("Digital")


class auditoria_resultado(models.Model):
    _name = "auditoria.resultado"

    @api.one
    def calcula_avance(self):
        avance = 0
        for i in self.rac:
            if i.state == 'cerrada':
                avance += i.peso
        self.avance = avance

    @api.one
    def aprobar(self):
        self.write({'aprobado': True})
        return True

    @api.multi
    def rechazar(self):
        self.write({'aprobado': False})
        noconf_form = self.env.ref('auditoria.no_conformidad_view_form', False)
        ctx = dict(
            pregunta=self.name,
            auditoria_id=self.relation.id,
        )
        return {
            'name': "No Conformidad",
            'type': 'ir.actions.act_window',
            'res_model': 'no_conformidad',
            'views': [(noconf_form.id, 'form')],
            'view_id': noconf_form.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx,
            }

    def action_abierta(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'abierta'})
            return True

    @api.one
    def action_cerrada(self):
        self.write({'state': 'cerrada'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'no_conformidad',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            }

    def generate_rac(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            rac_obj = self.pool.get("rac")
            idrac = rac_obj.create(cr, uid, {
                'name': i.name,
                'auditoria': i.relation.id,
                'informacion': i.comentario,
                })
            self.write(cr, uid, [i.id], {'rac': idrac})
        return ret

    def generate_nc(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            nc_obj = self.pool.get("no_conformidad")
            idnc = nc_obj.create(cr, uid, {
                'name': i.name,
                'responsable': i.responsable.id,
                'descripcion': i.comentario,
                })
            self.write(cr, uid, [i.id], {'no_conformidad': idnc})
        return ret

    name = fields.Char(string="Pregunta", size=120)
    categoria = fields.Char("Categoria")
    fisico = fields.Boolean("Físico")
    digital = fields.Boolean("Digital")
    nombre = fields.Char(string="Nombre")
    referencia = fields.Char(string="Valor de Referencia", size=120)
    tipo = fields.Selection([("sino", "Si/No"), ("num",
                    "Numerica"), ("abierta", "Abierta")],
                    string="Tipo de Pregunta")
    valor_real = fields.Char(string="Valor Real", size=120)
    aprobado = fields.Boolean(string="Aprobado")
    comentario = fields.Text(string="Comentario")
    responsable = fields.Many2one("hr.employee", string="Responsable",
                ondelete="set null")
    fecha_observacion = fields.Date("Fecha de la Observación")
    fecha_limite = fields.Date("Fecha Límite")
    fecha_solucion = fields.Date("Fecha de Resolución")
    state = fields.Selection([('abierta', 'Abierta'),
                ('cerrada', 'Cerrada')], "Estado", readonly=True)
    relation = fields.Many2one("auditoria", string="Auditoria")
    no_conformidad = fields.Many2one("no_conformidad",
                "No Conformidad")
    rac = fields.One2many("rac", "resultado_id", "Accion Correctiva")
    avance = fields.Float("Avance", compute=calcula_avance)
