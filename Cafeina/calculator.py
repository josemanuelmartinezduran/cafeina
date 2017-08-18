# -*- coding: utf-8 -*-
from openerp import models, fields,  api
from openerp.exceptions import except_orm, Warning, RedirectWarning


class jmd_tipoproyecto(models.Model):
    _inherit = "mail.thread"
    _name = "cf.tipoproyecto"
    name = fields.Char("Tipo de Proyecto")
    fijos = fields.Float("Costos Fijos Por Metro Cuadrado")
    variable_ids = fields.One2many("cf.variable", "tipoproyecto_id", string="Variables")


class jmd_catpresupueto(models.Model):
    _inherit = "mail.thread"
    _name = "cf.catpresupuesto"
    name = fields.Char("Nombre")


class jmd_variable(models.Model):
    _inherit = "mail.thread"
    _name = "cf.variable"
    name = fields.Char("Nombre de la Variable")
    uom = fields.Char("Unidad de Medida")
    categoria = fields.Many2one("cf.catpresupuesto",  string="Categoría")
    tipoproyecto_id = fields.Many2one("cf.tipoproyecto", string="Tipo de Proyecto")
    asignado_id = fields.Many2one("hr.employee",  string="Responsable")
    valor_ids = fields.One2many("cf.valor", "relation_id", string="Valores")
    aplica_taza = fields.Boolean("Aplica taza por calidad")


class jmd_valor(models.Model):
    _inherit = "mail.thread"
    _name = "cf.valor"
    name = fields.Char("Valor")
    minimo = fields.Float("Minimo")
    maximo = fields.Float("Máximo")
    factor = fields.Float("Factor",  digits=(7,  6))
    default = fields.Boolean("Predeterminada")
    valor_base = fields.Float("Valor Base")
    relation_id = fields.Many2one("cf.variable", string="Variable")


class jmd_calculator(models.Model):
    _inherit = "mail.thread"
    _name = "cf.calculator"
    
    @api.one
    def populate(self):
        ret = {}
        self.write({'fijos': self.tipo.fijos})
        for i in self.tipo.variable_ids:
            self.write({'linea_ids': [(0,  0,  {'name': i.id,  'factor': i.aplica_taza, 'unidad': i.uom ,  'persona': i.asignado_id.id})]})
        return ret
        
    @api.one
    def aplicar_metros(self):
        ret = {}
        for i in self.linea_ids:
            i.write({'horas': self.metros_construccion})
        return ret
        
    @api.one
    def calculate(self):
        ret = {}
        gran_total = 0
        impuestos = 0
        total_fijos = self.fijos * self.metros_construccion
        self.write({'total_fijos': total_fijos})
        for i in self.linea_ids:
            total = 0
            horas_totales = 0
            for j in i.name.valor_ids:
                if i.horas > j.minimo and i.horas < j.maximo:
                    total = j.valor_base + (j.factor * i.horas * i.persona.timesheet_cost)
                    horas_totales  = j.valor_base + (j.factor * i.horas )
                    print("Horas totales = " + str(horas_totales))
            self.write({'linea_ids': [(1,  i.id,  {'total':  total,  'horas_totales': horas_totales} )]})
            gran_total += total
        subtotal = (gran_total  * (1 + (self.utilidad  / 100)) *  (1 + (self.negociable  / 100)) + (total_fijos) )
        impuestos = subtotal * (self.tasa_impuestos / 100)
        gran_total = subtotal + impuestos
        self.write({'total': gran_total,  'impuestos': impuestos,  'subtotal': subtotal})
        return ret
        
    @api.one
    def create_quotation(self):
        ret = {}
        self.env["sale.order"].create({'name': self.name, 
                                                            'partner_id': self.cliente.id, 
                                                            'order_line': [(0, 0,  {
                                                                                            'name': self.servicio.name, 
                                                                                            'product_id': self.servicio.id,
                                                                                           'product_uom': 1,  
                                                                                            'price_unit': self.total, 
                                                                                            'product_uom_qty': 1, 
                                                                                            })]})
        return ret
        
    @api.one
    def create_project(self):
        ret = {}
        #Primer paso creamos el proyecto con base en la plantilla
        print("Creando e nuevo proyecto")
        p = self.plantilla_proyecto.copy({'name': self.name})
        print("Creado " + str(p))
        for l in self.linea_ids:
            print("Creando las lineas")
            try:
                p.write({'task_ids': [(0,  0,  {'name': l.name.name, 
                'planned_hours': l.horas_totales, 
                'user_id': l.persona.user_id.id})]})
            except:
                raise Warning('La persona asignada no tiene un usuario asociado, la tarea no será creada')
        #Recorremos las lineas par crear con cada una una tarea
        return ret
        
    @api.one
    def reemplazar(self):
        ret = {}
        for i in self.linea_ids:
            if(i.persona.id == self.original_id.id):
                i.write({'persona': self.nuevo_id.id})
        return ret

    name = fields.Char("Nombre del Proyecto")
    negociable = fields.Float("Porcentaje de Negociación",  default="10")
    servicio = fields.Many2one("product.product",  string="Producto")
    utilidad = fields.Float("Porcentaje de Utilidad",  default="20")
    fijos = fields.Float("Costos fijos po M2")
    total_fijos = fields.Float("Total costos fijos")
    tasa_impuestos = fields.Float("Tasa de Impuestos",  default="13")
    impuestos = fields.Float("Impuestos")
    total = fields.Float("Total")
    cliente = fields.Many2one("res.partner",  string="Cliente")
    plantilla_proyecto = fields.Many2one("project.project",  string="Platinlla del Proyecto")
    tipo = fields.Many2one("cf.tipoproyecto", string="Tipo de Proyecto")
    linea_ids = fields.One2many("cf.calculator.line", "relation_id", string="Lineas")
    metros_construccion = fields.Float("Metros de Construcción")
    fcalidad_id = fields.Many2one("cf.moneyrange",  string="Factor de Calidad")
    subtotal = fields.Float("Subtotal")
    factor_calidad = fields.Float("Factor de calidad")
    original_id = fields.Many2one("hr.employee",  string="Reemplazar a")
    nuevo_id = fields.Many2one("hr.employee",  string="Con")


class jmd_calculatorline(models.Model):
    _inherit = "mail.thread"
    _name = "cf.calculator.line"
    name = fields.Many2one("cf.variable",  string="Variable")
    unidad = fields.Char("Unidad")
    horas = fields.Float("Total de Unidades")
    factor = fields.Boolean("Aplica Factor")
    horas_totales = fields.Float("Total de Horas")
    persona = fields.Many2one("hr.employee",  string="Persona Asignada",  required=False)
    total = fields.Float("Total")
    relation_id = fields.Many2one("cf.calculator", string="Calculadora")

class jmd_MoneyRange(models.Model):
    _inherit = "mail.thread"
    _name = "cf.moneyrange"
    name = fields.Char("Descripcion")
    minimo = fields.Float("Mínimo")
    maximo = fields.Float("Máximo")
    factor = fields.Float("Factor")
