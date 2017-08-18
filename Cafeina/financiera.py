# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime
from dateutil.relativedelta import relativedelta
from num2words import num2words


class jmdcalculator(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.calculator"

    @api.depends('lineas')
    def get_pago(self):
        for record in self:
            monto = 0
            for linea in record.lineas:
                monto = linea.total
            if record.frecuencia == "26":
                monto *= 2
            elif record.frecuencia == "52":
                monto *= 4
            record.pago = monto

    @api.one
    def get_comision(self):
        monto = 0
        if self.producto == "nom":
            if self.monto < 9000:
                monto = self.monto * 0.03
            elif self.monto >= 9000:
                monto = 406
        self.comision = monto

    @api.one
    def get_centavos(self):
        centavos = round(self.monto - int(self.monto), 2)
        self.centavos = str(int(centavos * 100)).zfill(2)

    @api.one
    def get_letra(self):
        self.monto_letra = num2words(self.monto, lang='es').upper()

    @api.one
    def get_tasaletra(self):
        tasa = round(self.tasa.name, 1)
        entero = (int(tasa))
        decimal = round(tasa - int(tasa), 2) * 100
        self.tasa_letra = num2words(entero, lang='es').upper() + " PUNTO " +\
            num2words(decimal, lang='es').upper()

    name = fields.Char("Descripción", default=lambda self: self.
        env["ir.sequence"].get("sofom.calculator"))
    monto = fields.Float("Monto")
    monto_letra = fields.Char("Monto con Letra", compute=get_letra)
    total = fields.Float("Total del Prestamo")
    ciclo = fields.Integer("Ciclo")
    producto = fields.Selection([("micro", "Proyecto")], string="Producto")
    pagos = fields.Integer("Numero de Pagos")
    tipo = fields.Selection([("no", "Principal"),
        ("si", "Interciclo"), ('an', "Anticipo de Nómina")], string="Tipo")
    tasa = fields.Many2one("sofom.tasa", string="Tasa mensual")
    tasa_letra = fields.Char("Tasa Letra", compute=get_tasaletra)
    inicio = fields.Date("Fecha de inicio")
    lineas = fields.One2many("sofom.calculator.line", "calculator", "Lineas")
    lead = fields.Many2one("crm.lead", string="Prospecto")
    frecuencia = fields.Selection([("26", "Quincenal"), ("52", "Semanal"),
        ("12", "Mensual")], string="Frecuencia")
    plazo = fields.Many2one("sofom.plazo", string="Plazo")
    pago = fields.Float("Pago Mensual", compute=get_pago)
    destino = fields.Many2one("sofom.destino", string="Destino de Crédito")
    apertura = fields.Float("Comisión por apertura")
    cat = fields.Float("CAT")
    partner_id = fields.Many2one("res.partner",
        string="Cliente", related="lead.partner_id")
    tope = fields.Float("Tope del Crédito")
    comision = fields.Float("Comisión por Apertura", compute=get_comision)

    total_intereses = fields.Float("Total Intereses")
    total_iva = fields.Float("Total IVA")
    centavos = fields.Char("Centavos", compute=get_centavos)

    @api.multi
    def c_delete(self):
        for i in self.lineas:
            i.unlink()

    @api.one
    @api.constrains('monto')
    def check_monto(self):
        return True
    def c_payment(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            #finicio = datetime.srtptime(i.inicio, "%Y-%m-%d")
            insoluto = i.monto
            interes_periodo = i.tasa.name / (float(i.plazo.frecuencia) / 12)
            pago_fijo = i.calculate_payment(insoluto, interes_periodo,
                i.plazo.pagos)
            dias_plazo = i.plazo.dias_ciclo
            meses_plazo = i.plazo.meses_ciclo
            inicio_obj = datetime.datetime.strptime(i.inicio, "%Y-%m-%d")
            siguiente_pago = inicio_obj
            gran_total = 0
            total_iva = 0
            total_intereses = 0
            for j in range(i.plazo.pagos):
                line_obj = self.pool.get("sofom.calculator.line")
                interes = i.calculate_interest(interes_periodo, insoluto)
                capital = i.calculate_capital(interes, pago_fijo)
                insoluto -= capital
                iva = (interes / 1.16) * 0.16
                total = pago_fijo
                gran_total += total
                total_iva += iva
                total_intereses += interes
                print(("Numero de pago " + str(j)))
                line_obj.create(cr, uid, {
                    'calculator': i.id,
                    'fecha': siguiente_pago.strftime("%Y-%m-%d"),
                    'monto': pago_fijo,
                    'npago': str((j + 1)),
                    'capital': capital,
                    'intereses': interes,
                    'iva': iva,
                    'total': total,
                    'restante': insoluto,
                    })
                self.write(cr, uid, ids, {'pago': total})
                siguiente_pago += datetime.timedelta(days=dias_plazo)
                siguiente_pago += relativedelta(months=+meses_plazo)
            self.write(cr, uid, [i.id], {'total': gran_total,
                'total_iva': total_iva, 'total_intereses': total_intereses})
        return ret

    def calculate_payment(self, prestamo, interes, numero_cuotas):
        interes = interes / 100
        return prestamo * (interes * ((interes + 1) ** numero_cuotas)) / \
            (((interes + 1) ** numero_cuotas) - 1)

    def calculate_interest(self, interes, capital_pendiente):
        return (interes / 100) * capital_pendiente

    def calculate_capital(self, monto_interes, monto_pago):
        return monto_pago - monto_interes


class jmdcalculatorline(models.Model):
    _name = "sofom.calculator.line"
    name = fields.Char("Nombre")
    calculator = fields.Many2one("sofom.calculator", "Calculator")
    fecha = fields.Date("Fecha")
    monto = fields.Float("Monto")
    npago = fields.Char("Periodo")
    capital = fields.Float("Capital")
    intereses = fields.Float("Intereses")
    iva = fields.Float("IVA")
    total = fields.Float("Pago Total")
    restante = fields.Float("Capital Restante")
    
# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdtasa(models.Model):
    _name = "sofom.tasa"
    name = fields.Float("Tasa")
    producto = fields.Selection([("micro", "Proyecto")], string="Producto")
    ciclo = fields.Integer("Ciclo")
    tipo = fields.Selection([("no", "Principal")], string="Tipo")
    
class jmdaccount(models.Model):
    _name = "sofom.plazo"
    name = fields.Char("Plazo")
    ciclos_anio = fields.Integer("Ciclos por Año")
    dias_ciclo = fields.Integer("Días entre el ciclo")
    meses_ciclo = fields.Integer("Meses entre ciclos")
    frecuencia = fields.Selection([("26", "Quincenal"), ("52", "Semanal"),
        ("12", "Mensual")], string="Frecuencia")
    monto_max = fields.Float("Monto Máximo")
    pagos = fields.Integer("Pagos")
    
class jmffinanciera(models.Model):
    _inherit = "mail.thread"
    _name="cf.financiera"
    
    @api.one
    def calculate(self):
        ret = {}
        grantotal = 0
        for costo in self.lineas_costo:
            total =  (costo.costo_metro * (costo.techado + costo.terraza_techado) + (costo.costo_descubierto * (costo.no_techado + costo .terraza_techado)))
            print("El total es " + str(total))
            suma = total * costo.cantidad
            print("La suma es " + str(suma))
            costo.write({'costo_unidad': total,  'costo_total': suma})
            grantotal += suma
        for gasto in self.lineas_gasto:
            total_gasto = gasto.costo_base + (gasto.costo_metro * gasto.metros) + (gasto.unidades * gasto.costo_unidad)
            grantotal += total_gasto
            gasto.write({'costo_total': total_gasto})
        self.write({'costo': grantotal})
        preventa = (grantotal * (1+(self.preventa/100))) / self.meses - self.inicio_preventa
        parcial = grantotal / self.meses
        for i in range(self.meses):
            parcialidad = parcial
            if i >= self.inicio_preventa:
                parcialidad = parcial - preventa
            self.env["cf.financiera.calculo"].create({'name': i,  'monto':parcialidad})
        return ret
        
    name = fields.Char("Descripción")
    cliente = fields.Many2one("res.partner",  string="Cliente")
    fecha = fields.Date("Fecha de elaboración")
    elaborado = fields.Many2one("hr.employee", "Elaborado por")
    revisado = fields.Many2one("hr.employee",  "Revisado por")
    preventa = fields.Float("Porcentaje de Preventa")
    meses = fields.Integer("Numero de Periodos del Proyecto")
    inicio_preventa = fields.Integer("Periodo de Inicio de Preventa")
    costo = fields.Float("Costo")
    lineas_costo = fields.One2many("cf.financiera.line",  "financiera_id",  string="Costos")
    lineas_gasto = fields.One2many("cf.financiera.gasto",  "financiera_id",  string="Gasto")
    lineas_calculadas = fields.One2many("cf.financiera.calculo",  "financiera_id",  string="Aportaciones")
    
class jmd_cffinancieraline(models.Model):
    _inherit = "mail.thread"
    _name = "cf.financiera.line"
    
    name = fields.Char("Concepto")
    nivel = fields.Char("Nivel")
    cantidad = fields.Integer("Cantidad")
    metros = fields.Float("Metros cuadrados de construcción")
    terraza_techado = fields.Float("Metros terrazas techados")
    terraza_no_techado = fields.Float("Metros terrazas no techados")
    techado = fields.Float("Metros techados")
    no_techado = fields.Float("Metros no techados")
    cajones = fields.Integer("Cajones de Estacionamiento")
    apilados = fields.Integer("Cajones en Apilacoches")
    costo_metro = fields.Float("Costo Metro Cubierto")
    costo_descubierto = fields.Float("Costo Descubierto")
    costo_unidad = fields.Float("Costo Total por Unidad")
    costo_total = fields.Float("Costo Total")
    precio_unitario = fields.Float("Precio Unitario")
    precio_total = fields.Float("Precio de Venta")
    financiera_id = fields.Many2one("cf.financiera",  string="Corrida financiera")
    
class jmd_cffinancieragasto(models.Model):
    _inherit = "mail.thread"
    _name = "cf.financiera.gasto"
    name = fields.Char("Concepto")
    costo_base = fields.Float("Costo Base")
    costo_metro = fields.Float("Costo por Metro")
    metros = fields.Float("Metros Cuadrados")
    unidades = fields.Integer("Unidades")
    costo_unidad = fields.Float("Costo por Unidad")
    costo_total = fields.Float("Costo total")
    inversion = fields.Float("Porcentaje de Inversión")
    financiera_id = fields.Many2one("cf.financiera",  string="Corrida financiera")
    
class jmd_cffinancieraaportacion(models.Model):
    _inherit = "mail.thread"
    _name = "cf.financiera.calculo"
    name = fields.Char("Numero de aportación")
    monto = fields.Float("Cantidad")
    financiera_id = fields.Many2one("cf.financiera",  string="Corrida financiera")
    
