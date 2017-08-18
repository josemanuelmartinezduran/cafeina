# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime
from openerp.exceptions import Warning


class jmdcredito(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.credito"

    def action_iniciado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'iniciado'})
        return True

    @api.multi
    def calculate_cobranza(self):
        for record in self.pagos:
            today = datetime.date.today().strftime('%Y-%m-%d')
            print(("Today" + str(today)))
            if record.fecha < today and record.estado != "paid":
                print("Cobranza atrasada")
                record.cobranza = 250.00
                record.write({'cobranza': 250})
                hoy = datetime.datetime.today()
                dtfecha = datetime.datetime.strptime(record.fecha, '%Y-%m-%d')
                diferencia = hoy - dtfecha
                dias = diferencia.days
                print(("Dias de atraso" + str(dias)))
                moratorios = record.monto * (((record.credito_id.tasa + 8) /
                    100)) * 12 / 365 * dias
                record.moratorios = moratorios
                record.write({'moratorios': moratorios})
                #Modificando la factura
                creado = False
                for linea in record.factura.invoice_line:
                    if linea.name == "Moratorios":
                        linea.write({'price_unit': moratorios})
                        creado = True
                    elif linea.name == "Cobranza":
                        linea.write({'price_unit': 250})
                        creado = True
                if not creado:
                    self.env['account.invoice.line'].create(
                    {'invoice_id': record.factura.id,
                    'name': 'Moratorios',
                    'quantity': 1,
                    'price_unit': moratorios,
                    'account_id': 284})
                    self.env['account.invoice.line'].create(
                    {'invoice_id': record.factura.id,
                    'name': 'Cobranza',
                    'quantity': 1,
                    'price_unit': 250,
                    'account_id': 284})

    @api.multi
    def action_terminado(self):
        print("Iniciando")
        for p in self.pagos:
            if p.factura.state != 'paid':
                print("Pendiente un pago")
                return False
        print("vanzando")
        ciclo = self.titular.ciclo
        ciclo = int(ciclo) + 1
        self.titular.write({'ciclo': ciclo})
        self.write({'state': 'terminado'})
        return True

    @api.multi
    def pagar(self):
        print("Pagando")
        resto = self.pagando
        por_pagar = 0
        for i in self.pagos:
            por_pagar += i.monto
        if self.pagando > por_pagar:
            raise Warning('El Monto a Pagar Excede el Adeudo')
            return
        if self.caja_id is None:
            raise Warning('Favor de elegir la caja con la\
                que realizará el cobro')
            return
        print("Generando el pago")
        #Generando el pago
        sfecha = datetime.date.today().strftime('%Y-%m-%d')
        abono_id = self.env['sofom.abono'].create({
                        'monto': self.pagando,
                        'fecha': sfecha,
                        'cliente_id': self.titular.id,
                        'credito_id': self.id})
        #Leer la sequncia que se coloco
        print("Leer la sequncia que se coloco")
        secuencia = abono_id.name
        print("Registrando en la caja")
        #Registrando en la caja
        self.env['account.bank.statement.line'].create({
                'name': 'Pago de Credito ' + self.name,
                'amount': self.pagando,
                'partner_id': self.titular.id,
                'ref': secuencia,
                'statement_id': self.caja_id.id
            })
        #Iterando en las lineas del credito
        print("Iterando en las lineas del Credito")
        for linea in self.pagos:
            print(("Pagando el pago numero" + linea.numero))
            print(("Me quedan " + str(resto)))
            moratorios = 0
            cobranza = 0
            interes = 0
            capital = 0
            if resto <= 0:
                print("Saliendo")
                return True
            if linea.saldo <= 0:
                print("Ya estaba pagado")
                continue
            pago = 0
            if resto >= linea.saldo:
                pago = linea.saldo
                linea.factura.write({'state': 'paid'})
                if linea.pagado == 0:
                    moratorios = linea.moratorios
                    cobranza = linea.cobranza
                    interes = linea.intereses
                    capital = linea.capital
                else:
                    pagado = linea.pagado
                    moratorios = linea.moratorios - pagado
                    moratorios = 0 if moratorios < 0 else moratorios
                    pagado -= linea.moratorios - moratorios
                    cobranza = linea.cobranza - pagado
                    cobranza = 0 if cobranza < 0 else cobranza
                    pagado -= linea.cobranza - cobranza
                    interes = linea.intereses - pagado
                    interes = 0 if interes < 0 else interes
                    pagado -= linea.intereses - interes
                    capital = linea.capital - pagado
                    capital = 0 if capital < 0 else capital
                    pagado -= linea.capital - capital
                resto = resto - moratorios - cobranza - interes - capital
                print(("Al final del pago me quedan " + str(resto)))
            elif resto < linea.saldo:
                pago = resto
                tresto = resto
                pagado = linea.pagado
                print(("El resto es " + str(resto)))
                resto = 0
                linea.factura.write({'state': 'open'})
                if pagado == 0:
                    if tresto >= linea.moratorios:
                        moratorios = linea.moratorios
                        tresto -= linea.moratorios
                    else:
                        moratorios = tresto
                        tresto = 0
                    if tresto >= linea.cobranza:
                        cobranza = linea.cobranza
                        tresto -= linea.cobranza
                    else:
                        cobranza = tresto
                        tresto = 0
                    if tresto >= linea.intereses:
                        interes = linea.intereses
                        tresto -= linea.intereses
                    else:
                        interes = tresto
                        tresto = 0
                    if tresto >= linea.capital:
                        capital = linea.capital
                        tresto -= linea.capital
                    else:
                        capital = tresto
                        tresto = 0
                else:
                    moratorios_pagar = linea.moratorios - pagado
                    moratorios_pagar = 0 if moratorios_pagar < 0 else\
                        moratorios_pagar
                    pagado -= linea.moratorios - moratorios_pagar
                    if tresto >= moratorios_pagar:
                        moratorios = moratorios_pagar
                        tresto -= moratorios_pagar
                    else:
                        moratorios = tresto
                        tresto = 0
                    cobranza_pagar = linea.cobranza - pagado
                    cobranza_pagar = 0 if cobranza_pagar < 0 else\
                        cobranza_pagar
                    pagado -= linea.cobranza - cobranza_pagar
                    if tresto >= cobranza_pagar:
                        cobranza = cobranza_pagar
                        tresto -= cobranza_pagar
                    else:
                        cobranza = tresto
                        tresto = 0
                    interes_pagar = linea.intereses - pagado
                    interes_pagar = 0 if interes_pagar < 0 else\
                        interes_pagar
                    pagado -= linea.intereses - interes
                    if tresto >= interes_pagar:
                        interes = interes_pagar
                        tresto -= interes_pagar
                    else:
                        interes = tresto
                        tresto = 0
                    capital_pagar = linea.capital - pagado
                    capital_pagar = 0 if capital_pagar < 0 else\
                        capital_pagar
                    pagado -= linea.capital - interes
                    if tresto >= capital_pagar:
                        capital = capital_pagar
                        tresto -= capital_pagar
                    else:
                        capital = tresto
                        tresto = 0
            print(("Vamos a pagar de moratorios" + str(moratorios)))
            print(("Vamos a pagar de cobranza" + str(cobranza)))
            print(("Vamos a pagar de interes" + str(interes)))
            print(("Vamos a pagar de capital" + str(capital)))
            if moratorios >= 0.01:
                self.env['sofom.abono.line'].create({'name': 'Moratorios',
                'monto': moratorios,
                'numero_pago': str(linea.numero),
                'abono_id': abono_id.id})
            if cobranza >= 0.01:
                self.env['sofom.abono.line'].create({'name': 'Cobranza0',
                'monto': cobranza,
                'numero_pago': str(linea.numero),
                'abono_id': abono_id.id})
            if interes >= 0.01:
                self.env['sofom.abono.line'].create({'name': 'Interes',
                'monto': interes,
                'numero_pago': str(linea.numero),
                'abono_id': abono_id.id})
            if capital >= 0.01:
                self.env['sofom.abono.line'].create({'name': 'Capital',
                'monto': capital,
                'numero_pago': str(linea.numero),
                'abono_id': abono_id.id})
            pagado = pago + linea.pagado
            linea.write({'pagado': pagado})
            linea.pagado = pagado
            #Pagando la factura
            self.env['account.voucher'].create({
                'ammount': pago,
                'partner_id': self.titular.id,
                'account_id': 284
                })

    @api.one
    def liquidar(self):
        por_pagar = 0
        for i in self.pagos:
            por_pagar += i.monto
        if self.pagando > por_pagar:
            raise Warning('El Monto a Pagar Excede el Adeudo')
            return
        if self.caja_id is None:
            raise Warning('Favor de elegir la caja con la\
                que realizará el cobro')
            return
        print("Generando el pago")
        #Generando el pago
        sfecha = datetime.date.today().strftime('%Y-%m-%d')
        abono_id = self.env['sofom.abono'].create({
                        'monto': self.monto_anticipado,
                        'fecha': sfecha,
                        'cliente_id': self.titular.id,
                        'credito_id': self.id})
        #Leer la sequncia que se coloco
        print("Leer la sequncia que se coloco")
        secuencia = abono_id.name
        print("Registrando en la caja")
        #Registrando en la caja
        self.env['account.bank.statement.line'].create({
                'name': 'Pago de Credito ' + self.name,
                'amount': self.pagando,
                'partner_id': self.titular.id,
                'ref': secuencia,
                'statement_id': self.caja_id.id
            })
        #Iterando en las lineas del credito
        print("Iterando en las lineas del Credito")
        for linea in self.pagos:
            linea.write({'pagado': linea.capital})
            linea.factura.write({'state': 'paid'})
            if linea.saldo > 0:
                linea.write({'intereses': 0})
        ciclo = self.titular.ciclo
        ciclo = int(ciclo) + 1
        self.titular.write({'ciclo': ciclo})
        self.write({'state': 'terminado'})

    @api.one
    def action_juridico(self):
        self.write({'state': 'juridico'})
        return 0

    @api.one
    def get_vencido(self):
        monto_vencido = 0
        for i in self.pagos:
            monto_vencido += i.monto + i.moratorios + i.cobranza - i.pagado
        self.monto_vencido = monto_vencido
        return True

    @api.one
    def get_fvencimiento(self):
        ultima_fecha = 0
        for i in self.pagos:
            ultima_fecha = i.fecha
        self.fecha_vencimiento = ultima_fecha

    @api.one
    def get_ultimafecha(self):
        ultima_fecha = 0
        for i in self.abono_ids:
            ultima_fecha = i.fecha
        self.ultima_fecha = ultima_fecha

    @api.one
    def get_oxxo(self):
        cadena = "04"
        ncredito = "0" + self.name[2:]
        cadena += ncredito
        cadena += str(self.fecha_vencimiento)[-2:]
        cadena += str(self.fecha_vencimiento)[-5: -3]
        cadena += str(self.fecha_vencimiento)[: 4]
        cadena += str(int(self.total_parcialidad)).zfill(5)
        cadena += str("%.2f" % round(self.total_parcialidad, 2))[-2:]
        digito_verificador = 0
        sw_onetwo = 1
        total = 0
        print(cadena)
        for i in cadena:
            num = 0
            try:
                num = int(i) * sw_onetwo
            except:
                print("Valor no aceptble")
                continue
            if sw_onetwo == 2:
                sw_onetwo = 1
            else:
                sw_onetwo = 2
            if num > 9:
                num = int(num % 10) + int(num / 10)
            total += num
        digito_verificador = int(total % 10)
        if digito_verificador != 0:
            digito_verificador = 10 - digito_verificador
        cadena += str(digito_verificador)
        self.oxxo_barcode = cadena

    @api.one
    def get_montocredito(self):
        monto_credito = 0
        for i in self.pagos:
            monto_credito += i.monto + i.moratorios + i.cobranza
        self.monto_credito = monto_credito

    @api.one
    def get_anticipado(self):
        monto = 0
        iteracion = 0
        for i in self.pagos:
            if i.estado != 'paid':
                iteracion += 1
                if iteracion == 1:
                    monto += i.monto + i.moratorios + i.cobranza - i.pagado
                else:
                    monto += i.monto - i.intereses
        self.monto_anticipado = monto

    @api.one
    def get_parcial(self):
        monto = 0
        for i in self.pagos:
            monto = i.monto
        self.total_parcialidad = monto

    name = fields.Char("Nombre del Crédito")
    titular = fields.Many2one("res.partner", string="Titular")
    state = fields.Selection([('iniciado', 'Iniciado'),
        ('terminado', 'Terminado'), ('juridico', 'En Juridico')],
        string="Estado")
    pagos = fields.One2many("sofom.pago", "credito_id",
        string="Pagos")
    tasa = fields.Float("Tasa")
    pagando = fields.Float("Pagar")
    pago_con = fields.Float("Pago con ")
    cambio = fields.Float("Cambio")
    abono_ids = fields.One2many("sofom.abono", "credito_id", string="Abonos")
    cobrador = fields.Many2one("hr.employee", string="Cobrador")
    interciclo = fields.Boolean("Interciclo")
    caja_id = fields.Many2one("account.bank.statement", string="Caja")
    monto_anticipado = fields.Float("Monto de Finiquito Anticipado",
        digits=(9, 2), compute=get_anticipado)
    monto_vencido = fields.Float("Monto Vencido", compute=get_vencido,
        digits=(9, 2))
    ultima_fecha = fields.Date("Última Fecha de Pago", compute=get_ultimafecha)
    monto_credito = fields.Float("Monto del Crédito",
        compute=get_montocredito, digits=(9, 2))
    fecha_vencimiento = fields.Date("Fecha Vencimiento",
        compute=get_fvencimiento)
    total_parcialidad = fields.Float("Total de Cada Parcialidad",
        compute=get_parcial)
    oxxo_barcode = fields.Char("Codigo del Oxxo", compute=get_oxxo)


class jmdpago(models.Model):
    _name = "sofom.pago"
    _inherit = "mail.thread"

    @api.multi
    def get_saldo(self):
        for record in self:
            record.saldo = record.monto + record.moratorios + record.cobranza -\
                record.pagado

    @api.depends('fecha')
    def get_cobranza(self):
        for record in self:
            today = datetime.date.today().strftime('%Y-%m-%d')
            print(("Today" + str(today)))
            if record.fecha < today and record.estado != "paid":
                print("Cobranza atrasada")
                record.cobranza = 250.00
            else:
                record.cobranza = 0.00

    @api.depends('fecha')
    def get_moratorios(self):
        for record in self:
            today = datetime.date.today().strftime('%Y-%m-%d')
            if record.fecha < today and record.estado != "paid":
                hoy = datetime.datetime.today()
                dtfecha = datetime.datetime.strptime(record.fecha, '%Y-%m-%d')
                diferencia = hoy - dtfecha
                dias = diferencia.days
                print(("Dias de atraso" + str(dias)))
                record.moratorios = record.monto * ((record.credito_id.tasa /
                    100) + 8) * 12 / 365 * dias
            else:
                record.moratorios = 0.00

    numero = fields.Char("Numero de Pago")
    name = fields.Char("Nombre")
    fecha = fields.Date("Fecha")
    monto = fields.Float("Monto")
    capital = fields.Float("Capital")
    intereses = fields.Float("Intereses")
    factura = fields.Many2one("account.invoice", string="Factura")
    estado = fields.Selection([('draft', "Draft"), ('open', 'Open'),
        ('paid', 'Paid')],
        "Estado", related="factura.state")
    moratorios = fields.Float("Moratorios")
    cobranza = fields.Float("Gastos de Cobranza")
    pagado = fields.Float("Monto Pagado")
    saldo = fields.Float("Saldo", compute=get_saldo)
    credito_id = fields.Many2one("sofom.credito", string="Crédito")
    cliente = fields.Char("Cliente", related="credito_id.titular.name")
    situacion = fields.Selection([('Colocado', "Colocado"),
        ('Perido', 'Perdido'), ('Retenido', 'Retenido'),
        ('Transito', 'En Transito'), ('Recuperado', 'Recuperado')],
        "Estado")