    # -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning
import datetime
from dateutil.relativedelta import relativedelta


class jmdlead(models.Model):
    _inherit = "crm.lead"

    @api.one
    def compute_oxoo(self):
        cadena = "04"
        cadena += str(self.partner_id.ncliente)
        cadena += str(self.fecha_vencimiento)[-2:]
        cadena += str(self.fecha_vencimiento)[-5: -3]
        cadena += str(int(self.pago_mensual)).zfill(5)
        cadena += str(round(self.pago_mensual, 2))[-2:]
        self.oxxo_barcode = cadena

    @api.one
    @api.depends("credito_solicitado")
    def get_vencimiento(self):
        vencimiento = ""
        for i in self.credito_solicitado.lineas:
            vencimiento = i.fecha
        self.fecha_vencimiento = vencimiento

    @api.one
    @api.depends("credito_solicitado")
    def get_mensual(self):
        pago = 0
        for i in self.credito_solicitado.lineas:
            pago = i.monto
        self.pago_mensual = pago

    name = fields.Char("Codigo", default=lambda self: self.
        env["ir.sequence"].get("sofom.lead"))
    interesado = fields.Boolean("Interesado")
    producto = fields.Selection([("micro", "Microcrédito"),
        ("nom", "Nómina")], string="Producto")
    giro = fields.Many2one("sofom.giro", "Giro")
    subgiro = fields.Many2one("sofom.subgiro", "Subgiro")
    cotizaciones = fields.One2many("sofom.calculator", "lead",
        string="Cotizaciones")
    credito_solicitado = fields.Many2one("sofom.calculator",
        string="Cotización Aceptada")
    visita = fields.Boolean("Inspección Ocular")
    avisita = fields.Binary("Evidencia de la Visita")
    navisita = fields.Char("Nombre de la Evidencia")
    ife = fields.Binary("IFE")
    nife = fields.Char("NIFE")
    cd = fields.Binary("Comprobante Domiciliario")
    ncd = fields.Char("NCD")
    ci = fields.Binary("Comprobante de Ingresos")
    nci = fields.Char("NCI")
    ac = fields.Binary("Autorización Para Consulta")
    nac = fields.Char("NAC")
    sol = fields.Binary("Solicitud Firmada")
    nsol = fields.Char("Nombre de la Solicitud")
    ing = fields.Binary("Declaración de Ingresos")
    ning = fields.Char("Nombre Delaracion")
    curp = fields.Binary("CURP")
    ncurp = fields.Char("Nombre CURP")
    ccpdf = fields.Binary("PDF")
    nccpdf = fields.Char("NPDF")

    ffachada = fields.Binary("Fotografía de la Fachada")
    finteriora = fields.Binary("Fotografía  Interior 1")
    finteriorb = fields.Binary("Fotografia Interior 2")
    fvehiculo = fields.Binary("Fotografía Vehiculo")
    fotro = fields.Binary("Otra Fotografía")

    nffachada = fields.Char("Fotografía de la Fachada")
    nfinteriora = fields.Char("Fotografía  Interior 1")
    nfinteriorb = fields.Char("Fotografia Interior 2")
    nfvehiculo = fields.Char("Fotografía Vehiculo")
    nfotro = fields.Char("Otra Fotografía")

    puntaje = fields.Float("Puntaje")
    cdp = fields.Float("Capacidad de Pago")
    contrato = fields.Binary("Contrato")
    ncontrato = fields.Char("NC")
    caratula = fields.Binary("Carátula")
    ncaratula = fields.Char("NC")
    resumen = fields.Binary("Resúmen del Contrato")
    nresumen = fields.Char("NR")
    anexos = fields.Binary("Anexos")
    nanexos = fields.Char("NA")
    ingreso = fields.Float("Ingreso Neto")
    puntaje = fields.Float("Puntaje")
    solicitud = fields.One2many("sofom.solicitud", "lead_id",
        string="Solicitud")
    solicitudn = fields.One2many("sofom.solicitudn", "lead_id",
        string="Solicitud")
    evaluacion_ids = fields.One2many("sofom.evaluacion", "lead_id",
        string="Evaluación")
    evaluacionn_ids = fields.One2many("sofom.evaluacionn", "lead_id",
        string="Evaluación")
    cuanti = fields.One2many("sofom.cuanti", "lead_id",
        string="Evaluación Cualitativa")
    cuantim = fields.One2many("sofom.cuantim", "lead_id",
        string="Evaluación Cualitativa")
    credito_id = fields.Many2one("sofom.credito", string="Crédito")
    fecha_contrato = fields.Date("Fecha del Contrato")
    aceptado = fields.Boolean("Credito Autorizado")
    forma_disposicion = fields.Selection([('Efectivo', 'Efectivo'),
        ('Deposito', 'Depósito'), ('Transferencia', 'Transferencia'),
        ('Cheque', 'Cheque')],
        string="Forma de Disposición")
    primer_pago = fields.Date("Fecha de Primer Pago")
    cat = fields.Float("CAT")
    credito_generado = fields.Boolean("Credito Generado")
    asignacion = fields.Selection([('Propios', 'Propios'),
        ('Otros', 'Otros')], string="Asignación de Recursos")
    fuente_id = fields.Many2one("sofom.fuente", "Fuente de Recursos")
    numero_cheque = fields.Char("Numero de cheque")

    isolicitud = fields.Many2one("sofom.solicitud", string="Importar Solicitud")
    isolicitudn = fields.Many2one("sofom.solicitudn",
        string="Importar Solicitud")
    monto = fields.Float("Monto Solicitado", related="credito_solicitado.monto")
    planned_revenue = fields.Float(string="Monto del Cŕedito Solicitado")
    #Barcode
    oxxo_barcode = fields.Char("Codigo de Barras Oxxo", compute=compute_oxoo)
    fecha_vencimiento = fields.Date("Vencimiento", compute=get_vencimiento)
    pago_mensual = fields.Float("Pago Mensual", compute=get_mensual)

    @api.onchange('credito_solicitado')
    @api.one
    def onchange_credito(self):
        self.planned_revenue = self.credito_solicitado.monto

    @api.one
    def change_primer(self):
        print("Aqui 1")
        print((str(self.primer_pago)))
        self.credito_solicitado.write({'inicio': self.primer_pago})
        print("Aqui 2")
        print((self.credito_solicitado.name))
        print("Aqui 3")
        inicio_obj = datetime.datetime.strptime(self.primer_pago, "%Y-%m-%d")
        siguiente_pago = inicio_obj
        for i in self.credito_solicitado.lineas:
            i.write({'fecha': siguiente_pago.strftime("%Y-%m-%d")})
            siguiente_pago += datetime.timedelta(days=self.credito_solicitado
                .plazo.dias_ciclo)
            siguiente_pago += relativedelta(months=self.credito_solicitado
                .plazo.meses_ciclo)
        return True

    @api.one
    def copy(self, default=None):
        default = dict(default or {})
        name = self.env["ir.sequence"].get("sofom.calculator")
        solicitud = None
        solicitudn = None
        for i in self.solicitud:
            solicitud = i.copy()
            break
        for i in self.solicitudn:
            solicitudn = i.copy()
            break
        print(("Id de la solicitud duplicada" + str(solicitud)))
        default.update({
            'stage_id': 10,
            'name': name,
            'solicitud': [(1, solicitud, {})],
            'solicitudn': [(1, solicitudn, {})],
            })
        return super(jmdlead, self).copy(default)

    @api.multi
    def goto_solicitud(self):
        if self.credito_solicitado:
            self.write({'stage_id': 1})
        else:
            raise Warning('No ha colocado la cotización en el campo Cotización\
                Aceptada')

    @api.one
    def importar(self):
        if self.isolicitud:
            self.isolicitud.copy({'lead_id': self.id})
        if self.isolicitudn:
            self.isolicitudn.copy({'lead_id': self.id})

    @api.multi
    def goto_documentos(self):
        if (bool(self.solicitud) or bool(self.solicitudn)):
            self.write({'stage_id': 4})
        else:
            raise Warning('No ha llenado la Solicitud, vaya a la pesataña\
                Solicitud')

    @api.multi
    def goto_analisis(self):
        if (self.ife and self.cd and self.ci and self.ac and self.sol
            and self.ing and self.curp):
            self.write({'stage_id': 5})
        else:
            raise Warning('No se han ingresado todos los documentos')

#Ir a autorizacion
    @api.multi
    def goto_impresion(self):
        pago_mensual = 0
        capacidad_pago = 0
        if self.credito_solicitado:
            pago_mensual = self.credito_solicitado.pago
        if self.cuantim:
            capacidad_pago = self.cuantim.capacidad
        if self.cuanti:
            capacidad_pago = self.cuanti.capacidad
        if pago_mensual > capacidad_pago:
            raise Warning(('La capacidad de pago ' + str(capacidad_pago) +
                ' es menor al pago mensual ' + str(pago_mensual)))
        if (self.evaluacion_ids and self.cuantim) or\
            (self.evaluacionn_ids and self.cuanti):
            self.write({'stage_id': 6})
        else:
            raise Warning('No se han realizado ambas evaluaciones')

#Ir a impresion
    @api.multi
    def goto_autorizacion(self):
        if (self.aceptado):
            self.write({'stage_id': 11})
        else:
            raise Warning('No se ha Autorizado el Crédito')

    @api.multi
    def restart(self):
        self.write({'stage_id': 10})

    @api.multi
    def generate_payment(self):
        if self.credito_generado:
            return

        print("Generando el crédito")
        credito_id = self.env['sofom.credito'].create({
            'name': self.name,
            'titular': self.partner_id.id,
            'tasa': self.credito_solicitado.tasa.name,
            'oxxo_barcode': self.oxxo_barcode,
            })
        print("Llego hasta aqui")
        self.write({'credito_id': credito_id.id,
            'credito_generado': True})
        fecha = self.primer_pago
        dias_plazo = self.credito_solicitado.plazo.dias_ciclo
        meses_plazo = self.credito_solicitado.plazo.meses_ciclo
        inicio_obj = datetime.datetime.strptime(self.primer_pago, "%Y-%m-%d")
        siguiente_pago = inicio_obj
        for i in self.credito_solicitado.lineas:
            fecha = siguiente_pago.strftime("%Y-%m-%d")
            id_factura = self.env['account.invoice'].create(
                    {'partner_id': self.partner_id.id,
                    'date_invoice': fecha,
                    'account_id': 142,
                    'journal_id': 3,
                    'type': 'out_invoice',
                    'reference_type': 'none'})
            self.env['account.invoice.line'].create(
                    {'invoice_id': id_factura.id,
                    'name': 'Capital',
                    'quantity': 1,
                    'price_unit': i.capital,
                    'account_id': 284})
            self.env['account.invoice.line'].create(
                    {'invoice_id': id_factura.id,
                    'name': 'Interés',
                    'quantity': 1,
                    'price_unit': i.intereses,
                    'account_id': 284})
            self.env['sofom.pago'].create({
                    'numero': i.npago,
                    'fecha': fecha,
                    'monto': i.monto,
                    'capital': i.capital,
                    'intereses': i.intereses,
                    'factura': id_factura.id,
                    'credito_id': credito_id.id,
                })
            siguiente_pago += datetime.timedelta(days=dias_plazo)
            siguiente_pago += relativedelta(months=+meses_plazo)


class jmdgiro(models.Model):
    _name = "sofom.giro"
    _inherit = "mail.thread"
    name = fields.Char("Nombre")


class jmdaccount(models.Model):
    _name = "sofom.subgiro"
    _inherit = "mail.thread"
    name = fields.Char("Nombre")
    giro = fields.Many2one("sofom.giro", "Giro")


class jmdfuente(models.Model):
    _name = "sofom.fuente"
    name = fields.Char("Nombre")
    actual = fields.Float("Monto Actual")
    nomina = fields.Boolean("Activo en Nómina")
    micro = fields.Boolean("Activo en Microcrédito")
    tasa = fields.Float("Tasa")
    pagos_ids = fields.One2many("sofm.fuente.pago", "fuente_id",
        string="Fuentes")


class jmdfpago(models.Model):
    _inherit = "mail.thread"
    _name = "sofm.fuente.pago"
    name = fields.Char("Folio del Pago")
    monto = fields.Float("Monto")
    intereses = fields.Float("Intereses")
    iva = fields.Float("IVA")
    fuente_id = fields.Many2one("sofom.fuente")
    fecha = fields.Date("Fecha")