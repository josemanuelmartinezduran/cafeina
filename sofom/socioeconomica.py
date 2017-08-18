# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdaccount(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.socioeconomica"
    name = fields.Many2one("crm.lead", string="Soliciud")
    #Ingresos
    lunes = fields.Float("Lunes")
    martes = fields.Float("Martes")
    miercoles = fields.Float("Miércoles")
    jueves = fields.Float("Jueves")
    viernes = fields.Float("Viernes")
    sabado = fields.Float("Sábado")
    domingo = fields.Float("Domingo")
    itotal = fields.Float("Total")
    ingreso_promedio = fields.Float("Ingreso Promedio Mensual")
    #Gastos Negocio
    luz = fields.Float("Luz")
    telefono = fields.Float("Teléfono fijo y/o movil")
    renta = fields.Float("Renta")
    sueldos = fields.Float("Sueldos")
    cuotas = fields.Float("Cuotas Municipales")
    gas = fields.Float("Gas")
    agua = fields.Float("Agua")
    gasolina = fields.Float("Gasolina de transporte")
    etotal = fields.Float("Total de Egresos")
    #Ingresos Familiares
    salario = fields.Float("Salario del Solicitante")
    conyugue = fields.Float("Aporte del Conyugue")
    pension = fields.Float("Pensión/Jubilación")
    rentas = fields.Float("Rentas Propias")
    otros = fields.Float("Otros")
    iftotal = fields.Float("Total")
    #Gastos Familiares
    fluz = fields.Float("Luz")
    ftelefono = fields.Float("Teléfono")
    frenta = fields.Float("Renta")
    fgas = fields.Float("Gas")
    fgasolina = fields.Float("Gasolina y/o Transporte")
    fdiversion = fields.Float("Diversión")
    fcolegiaturas = fields.Float("Colegiaturas y/o Gastos Especiales")
    ftotal = fields.Float("Total")
    #Saldos
    saldo = fields.Float("Saldo en Caja Chica y/o Bancos")
    saldos = fields.One2many("sofom.saldos", "socioeconomica", string="Saldos")
    stotal = fields.Total("Total")
    #Inventarios
    iabarrotes = fields.Float("Abarrotes")
    ihigiene = fields.Float("Productos de Higiene")
    ibebidas = fields.Float("Bebidas")
    ilacteos = fields.Float("Lacteos")
    iperecederos = fields.Float("Perecederos")
    iotros = fields.Float("Otros")
    iotros_es = fields.Char("Especifique")
    itotal = fields.Float("Total")
    #Activo
    estantes = fields.Float("Estanteria")
    refrigeradores = fields.Float("Refrigeradores")
    mostradores = fields.Float("Mostradores")
    vitrinas = fields.Float("Vitrinas")
    rebanadoras = fields.Float("Rebanadoras")
    basculas = fields.Float("Basculas Electrónicas")
    congeladores = fields.Float("Congeladores")
    aotros = fields.Float("Otros")
    aoespecifique = fields.Char("Especifique")
    atotal = fields.Float("Total")
    #Vehiculos
    vehiculos = fields.One2many("sofom.vehiculos", "socioeconomica",
        string="Vehiculos")
    vtotal = fields.Float("Total")
    #Pagos
    pagos = fields.One2many("sofom.pago", "socioeconomica",
        string="Pagos")
    ptotal = fields.Float("Total")

    class jmdvehiculo(models.Model):
        _name = "sofom.vehiculo"
        _inherit = "mail.thread"
        name = fields.Char("Nombre")
        valor = fields.Float("Valor Comercial")
        socioeconomica = fields.Many2one("sofom.socioeconomica")

    class jmdpago(models.Model):
        _name = "sofom.pago"
        _inherit = "mail.thread"
        name = fields.Char("Nombre")
        valor = fields.Float("Valor Comercial")
        socioeconomica = fields.Many2one("sofom.socioeconomica")
        tipo = fields.Selection([('Corto', 'Corto Plazo'),
            ('Largo', 'Largo Plazo')], string="Tipo")
        banco = fields.Char("Nombre del Banco o Proveedor")

    class jmdsaldos(models.Model):
        _name = "sofom.saldos"
        _inherit = "mail.thread"
        name = fields.Char("Nombre")
        valor = fields.Float("Monto")
        socioeconomica = fields.Many2one("sofom.socioeconomica")