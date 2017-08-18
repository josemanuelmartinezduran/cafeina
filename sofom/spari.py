# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime


class jmdevaluacion(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.evaluacion"

    @api.multi
    def obten_total(self):
        for i in self.resultado:
            print("Eliminando")
            i.unlink()

        for i in self.lead_id.solicitud:
            self.write({
                'genero': i.genero,
                'estadoc': i.estadoc,
                'tviv': i.tviv,
                'nacimiento': i.nacimiento,
                'hijos': i.hijos,
                'dependientes': i.dependientes,
                'estudios': i.estudios,
                'nlocal': i.nlocal,
                'nttelefono': i.nttelefono,
                'nntiempo': i.nntiempo,
                'ntiempo': i.ntiempo,
                'nemp': i.nemp,
                'neemp': i.neemp,
                'nsalario': i.nsalario,
                'npension': i.npension,
                'napoyo': i.napoyo,
                'notro': i.notro,
                'tviv': i.tviv,
                'tasen': i.tasen,
                'ttviv': i.ttviv,
                'experiencia': i.experiencia,
                })
        total = 0
        sfecha = self.nacimiento
        hoy = datetime.datetime.today()
        dtfecha = datetime.datetime.strptime(sfecha, '%Y-%m-%d')
        diferencia = hoy - dtfecha
        edad = diferencia.days / 365
        ptsedad = 0
        if edad >= 20 and edad <= 30:
            ptsedad = -4
        elif edad > 30 and edad <= 45:
            ptsedad = 15
        elif edad > 45 and edad <= 60:
            ptsedad = 8
        elif edad > 61 and edad <= 75:
            ptsedad = 4

        self.env["sofom.evaluacion.line"].create({'name': 'Sexo',
            'maximo': '15',
            'puntaje': 15 if self.genero == 'f' else 10,
            'valor': str(self.genero),
            'evaluacion_id': self.id})
        total += 15 if self.genero == 'f' else 10
        self.env["sofom.evaluacion.line"].create({'name': 'Edad',
            'maximo': '15',
            'puntaje': ptsedad,
            'valor': str(edad),
            'evaluacion_id': self.id})
        total += edad
        pts = 0
        if self.dependientes <= 2:
            pts = 10
        elif self.dependientes <= 5:
            pts = 4
        else:
            pts = -4
        self.env["sofom.evaluacion.line"].create({'name': 'Dependientes',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.dependientes),
            'evaluacion_id': self.id})
        pts = 0
        if self.estadoc == "soltero":
            pts = -2
        if self.estadoc == "divorciado":
            pts = 2
        if self.estadoc == "viudo":
            pts = 4
        if self.estadoc == "ul":
            pts = 6
        if self.estadoc == "casado":
            pts = 10
        self.env["sofom.evaluacion.line"].create({'name': 'Estado Civil',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.estadoc),
            'evaluacion_id': self.id})
        pts = 0
        if self.estudios == 'sec' or self.estudios == 'prep' or\
            self.estudios == 'tec':
            pts = 10
        elif self.estudios == 'lic' or self.estudios == 'mc':
            pts = 0
        else:
            pts = 5
        self.env["sofom.evaluacion.line"].create({'name': 'Escolaridad',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.estudios),
            'evaluacion_id': self.id})
        self.env["sofom.evaluacion.line"].create({'name': 'Tipo de Local',
            'maximo': '10',
            'puntaje': 10 if self.nlocal == "est" else 5,
            'valor': str(self.nlocal),
            'evaluacion_id': self.id})
        pts = 0
        if self.tviv == 'propia':
            pts = 15
        elif self.tviv == 'pag':
            pts = 5
        elif self.tviv == 'ren':
            pts = -5
        elif self.tviv == 'fam':
            pts = 0
        self.env["sofom.evaluacion.line"].create({'name': 'Tipo de Local',
            'maximo': '15',
            'puntaje': pts,
            'valor': str(self.tviv),
            'evaluacion_id': self.id})
        self.env["sofom.evaluacion.line"].create({'name': 'Tipo Telefono',
            'maximo': '5',
            'puntaje': 5 if self.nttelefono == "negocio" else 0,
            'valor': str(self.nttelefono),
            'evaluacion_id': self.id})
        self.env["sofom.evaluacion.line"].create({'name': 'Tipo Telefono',
            'maximo': '5',
            'puntaje': 5 if self.nttelefono == "negocio" else 0,
            'valor': str(self.nttelefono),
            'evaluacion_id': self.id})
        pts = 0
        print(self.nntiempo)
        if int(self.nntiempo) <= 5:
            pts = 5
        elif int(self.nntiempo) <= 10:
            pts = 10
        elif int(self.nntiempo) <= 15:
            pts = 15
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Antigüedad del Negocio',
            'maximo': '15',
            'puntaje': pts,
            'valor': str(self.nntiempo),
            'evaluacion_id': self.id})
        pts = 0
        if int(self.ntiempo) <= 5:
            pts = 5
        elif int(self.ntiempo) <= 10:
            pts = 10
        elif int(self.ntiempo) <= 15:
            pts = 15
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Tiempo desarrollando la actividad',
            'maximo': '15',
            'puntaje': pts,
            'valor': str(self.ntiempo),
            'evaluacion_id': self.id})
        pts = 0
        if self.nemp == 0:
            pts = 0
        elif self.nemp <= 3:
            pts = 5
        else:
            pts = 10
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Numero de empleados',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.nemp),
            'evaluacion_id': self.id})
        pts = 0
        if int(self.neemp) == 0:
            pts = 0
        elif int(self.neemp) <= 3:
            pts = 5
        else:
            pts = 10
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Numero de empleados eventuales',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.neemp),
            'evaluacion_id': self.id})
        pts = 0
        valor = "Familiar/Ninguno"
        if self.notro:
            pts = 15
            valor = "Otro Negocio"
        elif self.npension:
            pts = 10
            valor = "Pensión"
        elif self.nsalario:
            pts = 5
            valor = "Salario"
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Otros ingresos',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(valor),
            'evaluacion_id': self.id})
        pts = 0
        if self.tviv == 'Propia':
            pts = 15
        elif self.tviv == 'Pagandola':
            pts = 5
        elif self.tviv == 'Rentada':
            pts = -5
        elif self.tviv == 'Familiar':
            pts = 0
        self.env["sofom.evaluacion.line"].create({'name': 'Tipo de Vivienda',
            'maximo': '15',
            'puntaje': pts,
            'valor': str(self.tviv),
            'evaluacion_id': self.id})
        pts = 0
        if int(self.ttviv) <= 0:
            pts = 0
        elif int(self.ttviv) <= 4:
            pts = 5
        else:
            pts = 8
        self.env["sofom.evaluacion.line"].create({'name': 'Tiempo de Arraigo',
            'maximo': '8',
            'puntaje': pts,
            'valor': str(self.ttviv),
            'evaluacion_id': self.id})
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Experiencia Crediticia',
            'maximo': '20',
            'puntaje': 20 if self.experiencia == "con" else 0,
            'valor': str(self.ttviv),
            'evaluacion_id': self.id})
        total = 0
        for k in self.resultado:
            total += k.puntaje
        self.write({'total': total})
        #self.lead_id.write({'puntaje': total})

    @api.multi
    def remove(self):
        for i in self.resultado:
            i.unlink()

    @api.multi
    def populate(self):
        for i in self.lead_id.solicitud:
            self.write({
                'genero': i.genero,
                'estadoc': i.estadoc,
                'tviv': i.tviv,
                'nacimiento': i.nacimiento,
                'hijos': i.hijos,
                'dependientes': i.dependientes,
                'estudios': i.estudios,
                'nlocal': i.nlocal,
                'nttelefono': i.nttelefono,
                'nntiempo': i.nntiempo,
                'ntiempo': i.ntiempo,
                'nemp': i.nemp,
                'neemp': i.neemp,
                'nsalario': i.nsalario,
                'npension': i.npension,
                'napoyo': i.napoyo,
                'notro': i.notro,
                'tviv': i.tviv,
                'tasen': i.tasen,
                'ttviv': i.ttviv,
                'experiencia': i.experiencia,
                })

    name = fields.Char("Descripción", default="EVALUACION CUALITATIVA")
    tipo = fields.Selection([("cuanti", "Cuantitativa"),
        ("cuali", "Cualitativa")], string="Tipo")
    total = fields.Float("Total")
    lead_id = fields.Many2one("crm.lead", string="Prospecto")
    genero = fields.Selection([("m", "Masculino"), ("f", "Femenino")],
        string="Género")
    estadoc = fields.Selection([("soltero", "Soltero"), ("casado", "Casado"),
        ("ul", "Unión Libre"), ("viudo", "Viudo")], string="Estado Civil")
    tviv = fields.Selection([("propia", "Propia"), ("pag", "Pagándola"),
        ("ren", "Rentada"), ("fam", "Familiar")], string="Propiedad del Local")
    nacimiento = fields.Date("Fecha de Nacimiento")
    hijos = fields.Integer("Número de Hijos")
    dependientes = fields.Integer("Número de Dependientes")
    estudios = fields.Selection([("prim", "Primaria"), ("sec", "Secundaria"),
        ("prep", "Preparatoria"), ("lic", "Licenciatura"),
        ("mc", "Maestría"), ("tec", "Carrera Técnica"),
        ("ct", "Carrera Trunca")], string="Último Grado de Estudios")
    nlocal = fields.Selection([("semi", "Semifijo"), ("est", "Establecido")],
        string="Tipo de local")
    nttelefono = fields.Selection([("negocio", "Del Negocio"),
        ("personal", "Personal")], string="Tipo de Teléfono")
    nntiempo = fields.Char("Antigüedad en el Negocio")
    ntiempo = fields.Char("Antigüedad desarrollando la actividad")
    nemp = fields.Integer("Empleados Permanentes")
    neemp = fields.Integer("Empleados Eventuales")
    nsalario = fields.Boolean("Salario")
    npension = fields.Boolean("Pensión")
    napoyo = fields.Boolean("Apoyo Familiar")
    notro = fields.Boolean("Otro Negocio")
    tviv = fields.Selection([("Propia", "Propia"), ("Pagandola", "Pagándola"),
        ("Rentada", "Rentada"),
        ("Familiar", "Familiar")], string="Tipo de Vivienda")
    ttviv = fields.Integer("Tiempo en la vivienda (Años)")
    tasen = fields.Selection([("casa", "Casa Sola"),
        ("dep", "Departamento/U. Habitacional/Fraccionamiento"),
        ("rural", "Asentamiento Rural")], string="Tipo de Asentamiento")
    experiencia = fields.Selection([("sin", "Sin Experiencia"),
        ("con", "Con Experiencia")], string="Experincia Crediticia")
    resultado = fields.One2many("sofom.evaluacion.line", "evaluacion_id",
         string="Resultados")


class jmdcuanti(models.Model):
    _name = "sofom.cuanti"
    _inherit = "mail.thread"

    @api.multi
    @api.depends('lead_id')
    def calculate_payment(self):
        total = 0
        ingresos = 0
        egresos = 0
        print("Pagos")
        for i in self.lead_id.solicitudn:
            print(("Salario" + str(i.salario)))
            ingresos = i.salario + i.industrial_comercial +\
                i.servicios_profesionales + i. venta + i.actividad_financiera +\
                i.otros_ingresos + i.conyugue
            egresos = i.hipoteca + i.automotriz + i.personal + i.tarjeta +\
                i.telecomunicaciones
            total = ingresos - egresos
            self.write({'ingresos': ingresos,
                'egresos': egresos,
                'capacidad': (total * 0.3),
                'utilidad': total})
            self.lead_id.write({'ingreso': total})
            total = 0
        return 1

    name = fields.Char("Descripción", default="EVALUACION CUANTITATIVA")
    ingresos = fields.Float("Ingresos")
    egresos = fields.Float("Egresos")
    utilidad = fields.Float("Utilidad")
    capacidad = fields.Float("Capacidad de Pago")
    lead_id = fields.Many2one("crm.lead")


class jmdevaluacion(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.evaluacionn"

    @api.multi
    def obten_total(self):
        for i in self.resultado:
            print("Eliminando")
            i.unlink()

        for i in self.lead_id.solicitudn:
            self.write({
                'genero': i.genero,
                'estadoc': i.estadoc,
                'tviv': i.tviv,
                'nacimiento': i.nacimiento,
                'dependientes': i.dependientes,
                'tasen': i.tasen,
                'ttviv': i.ttviv,
                'experiencia': i.experiencia,
                'ciclo': self.lead_id.partner_id.ciclo,
                'estado_credito': i.estado_credito,
                'templeo': i.templeo,
                'ttempleo': i.ttempleo
                })

        #Sexo
        total = 0
        self.env["sofom.evaluacion.line"].create({'name': 'Sexo',
            'maximo': '15',
            'puntaje': 15 if self.genero == 'f' else 10,
            'valor': str(self.genero),
            'evaluacionn_id': self.id})
        total += 15 if self.genero == 'f' else 10
        #Estado Civil
        pts = 0
        if self.estadoc == "soltero":
            pts = 3
        if self.estadoc == "divorciado":
            pts = 1
        if self.estadoc == "viudo":
            pts = 4
        if self.estadoc == "casado":
            pts = 5
        self.env["sofom.evaluacion.line"].create({'name': 'Estado Civil',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.estadoc),
            'evaluacionn_id': self.id})
        total += pts
        #Tipo Unidad
        pts = 0
        if self.tasen == "casa":
            pts = 10
        elif self.tasen == "dep" or self.tasen == "rural":
            pts = -5
        self.env["sofom.evaluacion.line"].create({'name': 'Tipo de Unidad',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.tasen),
            'evaluacionn_id': self.id})
        total += pts
        #Tipo de unidad paso 2
        pts = 0
        if self.tviv == 'Propia':
            pts = 10
        elif self.tviv == 'Pagandola':
            pts = 5
        elif self.tviv == 'Rentada':
            pts = -7
        elif self.tviv == 'Familiar':
            pts = -5
        self.env["sofom.evaluacion.line"].create({'name': 'Tipo de Unidad',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.tviv),
            'evaluacionn_id': self.id})
        total += pts
        #Tiempo de Arraigo
        pts = 0
        if self.ttviv <= 0:
            pts = -5
        elif self.ttviv <= 4:
            pts = 5
        else:
            pts = 10
        self.env["sofom.evaluacion.line"].create({'name': 'Tiempo de Arraigo',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.ttviv),
            'evaluacionn_id': self.id})
        total += pts
        #Ciclo
        pts = 0
        if self.ciclo == 0:
            pts = 1
        elif self.ciclo == 1:
            pts = 5
        elif self.ciclo > 1:
            pts = 10
        self.env["sofom.evaluacion.line"].create({'name': 'Ciclo del Crédito',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.ciclo),
            'evaluacionn_id': self.id})
        total += pts
        #Edad
        sfecha = self.nacimiento
        hoy = datetime.datetime.today()
        dtfecha = datetime.datetime.strptime(sfecha, '%Y-%m-%d')
        diferencia = hoy - dtfecha
        edad = diferencia.days / 365
        ptsedad = 0
        if edad >= 18 and edad <= 24:
            ptsedad = -5
        elif edad > 24 and edad <= 34:
            ptsedad = 15
        elif edad > 34 and edad <= 45:
            ptsedad = 10
        elif edad > 45 and edad <= 65:
            ptsedad = 5
        self.env["sofom.evaluacion.line"].create({'name': 'Edad',
            'maximo': '15',
            'puntaje': ptsedad,
            'valor': str(edad),
            'evaluacionn_id': self.id})
        total += ptsedad
        #Experiencia
        pts = 0
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Experiencia Crediticia',
            'maximo': '20',
            'puntaje': 20 if self.experiencia == "con" else 0,
            'valor': str(self.ttviv),
            'evaluacionn_id': self.id})
        self.write({'total': total})
        total += pts
        #Atraso
        pts = 0
        if self.estado_credito == "sin_atraso":
            pts = 15
        elif self.estado_credito == "con_atraso":
            pts = -15
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Estado actual de crédito',
            'maximo': '15',
            'puntaje': pts,
            'valor': str(self.estado_credito),
            'evaluacionn_id': self.id})
        total += pts
        #Empleo
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Empleo',
            'maximo': '3',
            'puntaje': 3 if self.templeo == "asalariado" else 1,
            'valor': str(self.templeo),
            'evaluacionn_id': self.id})
        self.write({'total': total})
        total += 3 if self.templeo == "asalariado" else 1
        #Tiempo Empleo
        pts = 0
        if self.ttempleo < 1:
            pts = 5
        elif self.ttempleo <= 3:
            pts = 8
        else:
            pts = 12
        self.env["sofom.evaluacion.line"].create(
            {'name': 'Tiempo en el Empleo',
            'maximo': '12',
            'puntaje': pts,
            'valor': str(self.ttempleo),
            'evaluacionn_id': self.id})
        self.write({'total': total})
        total += pts
        #Dependientes
        pts = 0
        if self.dependientes <= 2:
            pts = 10
        elif self.dependientes <= 5:
            pts = 5
        else:
            pts = -5
        self.env["sofom.evaluacion.line"].create({'name': 'Dependientes',
            'maximo': '10',
            'puntaje': pts,
            'valor': str(self.dependientes),
            'evaluacionn_id': self.id})
        total += pts
        total = 0
        for k in self.resultado:
            total += k.puntaje
        self.write({'total': total})
        #self.lead_id.write({'puntaje': total})

    @api.multi
    def remove(self):
        for i in self.resultado:
            i.unlink()

    @api.multi
    def populate(self):
        for i in self.lead_id.solicitudn:
            self.write({
                'genero': i.genero,
                'estadoc': i.estadoc,
                'tviv': i.tviv,
                'nacimiento': i.nacimiento,
                'dependientes': i.dependientes,
                'tasen': i.tasen,
                'ttviv': i.ttviv,
                'experiencia': i.experiencia,
                'ciclo': self.lead_id.partner_id.ciclo,
                'estado_credito': i.estado_credito,
                'templeo': i.templeo,
                'ttempleo': i.ttempleo
                })

    name = fields.Char("Descripción", default="EVALUACION CUALITATIVA")
    total = fields.Float("Total")
    lead_id = fields.Many2one("crm.lead", string="Prospecto")
    genero = fields.Selection([("m", "Masculino"), ("f", "Femenino")],
        string="Género")
    estadoc = fields.Selection([("soltero", "Soltero"), ("casado", "Casado"),
        ("ul", "Unión Libre"), ("viudo", "Viudo")], string="Estado Civil")
    tviv = fields.Selection([("propia", "Propia"), ("pag", "Pagándola"),
        ("ren", "Rentada"), ("fam", "Familiar")], string="Propiedad del Local")
    nacimiento = fields.Date("Fecha de Nacimiento")
    dependientes = fields.Integer("Número de Dependientes")
    tviv = fields.Selection([("propia", "Propia"), ("pag", "Pagándola"),
        ("ren", "Rentada"), ("fam", "Familiar")], string="Tipo de Vivienda")
    ttviv = fields.Integer("Tiempo en la vivienda (Años)")
    tasen = fields.Selection([("casa", "Casa Sola"),
        ("dep", "Departamento/U. Habitacional/Fraccionamiento"),
        ("rural", "Asentamiento Rural")], string="Tipo de Asentamiento")
    experiencia = fields.Selection([("sin", "Sin Experiencia"),
        ("con", "Con Experiencia")], string="Experincia Crediticia")
    resultado = fields.One2many("sofom.evaluacion.line", "evaluacionn_id",
         string="Resultados")
    ciclo = fields.Integer("Ciclo")
    estado_credito = fields.Selection([("sin_atraso", "Sin Atraso"),
        ("sin_historial", "Sin Historial"), ("con_atraso", "Con Atraso")],
        string="Estado de los Créditos Actuales")
    templeo = fields.Selection([('autoempleo', 'Autoempleo'),
        ('asalariado', 'Asalariado')], string="Tipo de Empleo")
    ttempleo = fields.Integer("Años en el Empleo")


class jmdcuantin(models.Model):
    _name = "sofom.cuantim"
    _inherit = "mail.thread"

    @api.multi
    @api.depends('lead_id')
    def calculate_payment(self):
        total = 0
        ingresos = 0
        egresos = 0
        print("Pagos")
        for i in self.lead_id.solicitud:
            ingresos = i.imensual + i.iotros + i.iconyuge
            egresos = i.enrenta + i.enelectricidad + i.engas +\
                i.enagua + i.entelefono + i.enimpuestos +\
                i.ensueldos + i.enmaterial - i.eninventario +\
                i.entransporte + i.emcomisiones + i.eprenta +\
                i.epgas + i.epluz + i.eptelefono + i.epagua +\
                i.epeducacion + i.epfamilia + i.epcable +\
                i.epalimentos
            total = ingresos - egresos
            self.write({'ingresos': ingresos,
                'egresos': egresos,
                'capacidad': (total * 0.3),
                'utilidad': total})
            self.lead_id.write({'ingreso': total})
            total = 0
        return 1

    name = fields.Char("Descripción", default="EVALUACION CUANTITATIVA")
    ingresos = fields.Float("Ingresos")
    egresos = fields.Float("Egresos")
    utilidad = fields.Float("Utilidad")
    capacidad = fields.Float("Capacidad de Pago")
    lead_id = fields.Many2one("crm.lead")

    class jmdevaline(models.Model):
        _name = "sofom.evaluacion.line"
        _inherit = "mail.thread"
        name = fields.Char("Criterio")
        maximo = fields.Float("Valor Máximo")
        puntaje = fields.Float("Puntaje")
        valor = fields.Char("Valor")
        evaluacion_id = fields.Many2one("sofom.evaluacion", string="Evaluación")
        evaluacionn_id = fields.Many2one("sofom.evaluacionn",
            string="Evaluación")