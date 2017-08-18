# -*- coding: utf-8 -*-
from openerp import models, fields
from openerp import api
import datetime


class jmdsolicitud(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.solicitud"
    name = fields.Char("Número", default=lambda self: self.
        env["ir.sequence"].get("sofom.solicitud"))
    lead_id = fields.Many2one("crm.lead", string="Originacion")
    fecha = fields.Date("Fecha", default=lambda *a: datetime.
        date.today().strftime('%Y-%m-%d'))
    lugar = fields.Selection([("campo", "Campo"), ("oficina", "Oficina")],
        string="LLenado en:", default="oficina")
    oficina = fields.Char("Oficina", default="SmartQuo")
    ciclo = fields.Integer("Ciclo", related="lead_id.partner_id.ciclo")
    asesor = fields.Many2one("hr.employee", string="Asesor")
    monto = fields.Float("Monto Solicitado",
        related="lead_id.credito_solicitado.monto")
    tasa = fields.Float("Tasa",
        related="lead_id.credito_solicitado.tasa.name")
    plazo = fields.Char("Plazo",
        related="lead_id.credito_solicitado.plazo.name")
    tipo = fields.Selection([("p", "Producttivo"), ("i",
        "Interciclo Productivo")], string="Tipo")
    #Datos Personales
    materno = fields.Char("Apellido Materno",
        related="lead_id.partner_id.materno")
    paterno = fields.Char("Apellido Paterno",
        related="lead_id.partner_id.paterno")
    nombre = fields.Char("Nombre",
        related="lead_id.partner_id.nombre")
    genero = fields.Selection([("m", "Masculino"), ("f", "Femenino")],
        string="Género")
    nacimiento = fields.Date("Fecha de Nacimiento")
    pais = fields.Char("Pais de Nacimiento", default="México")
    entidad = fields.Char("Entidad Federativa")
    nacionalidad = fields.Char("Nacionalidad", default="Mexicana")
    curp = fields.Char("CURP")
    rfc = fields.Char("RFC")
    identificacion = fields.Char("Número de Identificación")
    tipoid = fields.Selection([('ine', 'INE'), ('cedula', 'Cédula Profesional'),
        ('pasaporte', 'Pasaporte'), ('cartilla', 'Cartilla Militar')],
        string="Tipo de Identificación")
    clave = fields.Char("Clave de Elector")
    estadoc = fields.Selection([("soltero", "Soltero"), ("casado", "Casado"),
        ("ul", "Unión Libre"), ("viudo", "Viudo")], string="Estado Civil")
    regimen = fields.Selection([("sc", "Sociedad Conyugal"),
        ("sb", "Separación de Bienes")], string="Regimen Conyugal")
    hijos = fields.Integer("Número de Hijos")
    dependientes = fields.Integer("Número de Dependientes")
    estudios = fields.Selection([("prim", "Primaria"), ("sec", "Secundaria"),
        ("prep", "Preparatoria"), ("lic", "Licenciatura"),
        ("mc", "Maestría"), ("tec", "Carrera Técnica"),
        ("ct", "Carrera Trunca")], string="Último Grado de Estudios")
    experiencia = fields.Selection([("sin", "Sin Experiencia"),
        ("con", "Con Experiencia")], string="Experiencia Crediticia")
    #Domicilio Actual
    calle = fields.Char("Calle", related="lead_id.partner_id.calle")
    ext = fields.Char("Número Exterior", related="lead_id.partner_id.ext")
    inte = fields.Char("Número Interior", related="lead_id.partner_id.inte")
    col = fields.Many2one("utils.colonia", string="Colonia",
        related="lead_id.partner_id.col")
    cp = fields.Char("Código Postal", related="lead_id.partner_id.cp")
    ciudad = fields.Char("Cuidad/Municipio",
        related="lead_id.partner_id.ciudad")
    estado = fields.Many2one("res.country.state", string="Estado",
            related="lead_id.partner_id.estado")
    entrec = fields.Char("Referencia Entre Calles")
    ares = fields.Char("Años de Residencia")
    tel = fields.Char("Teléfono Fijo",
        related="lead_id.partner_id.phone")
    cel = fields.Char("Celular",
        related="lead_id.partner_id.mobile")
    email = fields.Char("Correo Electrónico",
        related="lead_id.partner_id.email")
    ttviv = fields.Integer("Tiempo en la vivienda (Años)")
    tviv = fields.Selection([("Propia", "Propia"), ("Pagandola", "Pagándola"),
        ("Rentada", "Rentada"), ("Familiar", "Familiar")],
        string="Tipo de Vivienda")
    dueno = fields.Char("Nombre del Dueño")
    telarr = fields.Char("Teléfono del Arrendador")
    renta = fields.Float("Costo de Renta")
    tasen = fields.Selection([("casa", "Casa Sola"),
        ("dep", "Departamento/U. Habitacional/Fraccionamiento"),
        ("rural", "Asentamiento Rural")], string="Tipo de Asentamiento")
    agua = fields.Boolean("Agua Potable")
    drenaje = fields.Boolean("Drenaje")
    gas = fields.Boolean("Gas")
    internet = fields.Boolean("Internet")
    luz = fields.Boolean("Luz")
    cable = fields.Boolean("TV Paga/Satelital")
    telefono = fields.Boolean("Teléfono")
    #Datos del Conyuge
    cnombre = fields.Char("Nombres y Apellidos")
    ctrabaja = fields.Boolean("Trabaja Actualmente")
    cocupacion = fields.Selection([("hogar", "Hogar"), ("com", "Comerciante"),
        ("empl", "Empleado"), ("jub", "Jubilado")], string="Ocupación")
    cempresa = fields.Char("Nombre de la Empresa en la que Labora")
    cpuesto = fields.Char("Puesto o Cargo")
    csueldo = fields.Char("Sueldo / Ingreso Mensual")
    cdom = fields.Char("Domicilio de la Empresa")
    ctel = fields.Char("Teléfono Oficina")
    ccel = fields.Char("Teléfono Celular")
    #Datos del Negocio
    sector = fields.Selection([("ind", "Industria"), ("com", "Comercio"),
        ("ser", "Servicios"), ("con", "Consultoría")],
        string="Sector Económico del Negocio")
    rama = fields.Selection([("principal", "Principal"),
        ("com", "Complementario")], string="Rama del Negocio")
    nnombre = fields.Char("Nombre del Negocio")
    ntiempo = fields.Char("Antigüedad desarrollando la actividad (En Años)")
    nntiempo = fields.Char("Antigüedad en el Negocio (En Años)")
    ngiro = fields.Char("Subgiro del Negocio",
        related="lead_id.subgiro.name")
    nlocal = fields.Selection([("semi", "Semifijo"), ("est", "Establecido")],
        string="El local es")
    npropio = fields.Boolean("Es negocio propio")
    nrentado = fields.Boolean("Rentado")
    nrenta = fields.Float("Renta Mensual")
    nfamiliar = fields.Boolean("Familiar")
    nhipoteca = fields.Float("Hipoteca Mensual")
    ndueno = fields.Char("Nombre del Dueño")
    nttelefono = fields.Selection([("negocio", "Del Negocio"),
        ("personal", "Personal")], string="Tipo de Teléfono")
    ntelefono = fields.Char("Teléfono")
    nemp = fields.Integer("Empleados Permanentes")
    neemp = fields.Integer("Empleados Eventuales")
    nmismo = fields.Boolean("Mismos que direcion personal")
    ncalle = fields.Char("Calle")
    nnext = fields.Char("Número Exterior")
    nint = fields.Char("Número Interior")
    ncol = fields.Many2one("utils.colonia", string="Colonia")
    ncp = fields.Char("Código Postal")
    ncuidad = fields.Char("Cuidad/Municipio")
    nestado = fields.Many2one("res.country.state", string="Estado")
    nref = fields.Char("Referencia Ubicación Entre Calles")
    nsalario = fields.Boolean("Salario")
    npension = fields.Boolean("Pensión")
    napoyo = fields.Boolean("Apoyo Familiar")
    notro = fields.Boolean("Otro Negocio")
    nmonto = fields.Float("Monto Mensual")
    #Solidario
    garantia = fields.Char("Garantia Prendaria")
    snombre = fields.Char("Nombres y Apellidos")
    strabaja = fields.Boolean("Trabaja Actualmente")
    socupacion = fields.Selection([("micro", "Microempresario"),
        ("emp", "Empleado")], string="Ocupación")
    ssector = fields.Selection([("ind", "Industria"), ("com", "Comercio"),
        ("ser", "Servicios")], string="Sector")
    srama = fields.Selection([("principal", "Principal"),
        ("com", "Complementario")], string="Rama del Negocio")
    snnombre = fields.Char("Nombre del Negocio")
    spuesto = fields.Char("Puesto")
    ssueldo = fields.Float("Sueldo Mensual")
    sdom = fields.Char("Domicilio de la Empresa")
    stel = fields.Char("Telefono Oficina")
    scel = fields.Char("Celular")
    scurp = fields.Char("CURP")
    srfc = fields.Char("RFC")
    sclave = fields.Char("Clave de Elector")
    sidentificacion = fields.Char("Número de Identificación")
    stipoid = fields.Selection([('ine', 'INE'),
        ('cedula', 'Cédula Profesional'),
        ('pasaporte', 'Pasaporte'), ('cartilla', 'Cartilla Militar')],
        string="Tipo de Identificación")
    sedad = fields.Integer("Edad")
    sestadoc = fields.Selection([("soltero", "Soltero"), ("casado", "Casado"),
        ("ul", "Unión Libre"), ("viudo", "Viudo")], string="Estado Civil")
    sregimen = fields.Selection([("sc", "Sociedad Conyugal"),
        ("sb", "Separación de Bienes")], string="Regimen Conyugal")
    shijos = fields.Integer("Número de Hijos")
    sdependientes = fields.Integer("Número de Dependientes")
    scalle = fields.Char("Calle")
    sext = fields.Char("Número Exterior")
    sinte = fields.Char("Número Interior")
    scol = fields.Char("Colonia")
    scp = fields.Char("Código Postal")
    sciudad = fields.Char("Cuidad/Municipio")
    sestado = fields.Char("Estado")
    sentrec = fields.Char("Referencia Entre Calles")
    stviv = fields.Selection([("propia", "Propia"), ("pag", "Pagándola"),
        ("ren", "Rentada"), ("fam", "Familiar")], string="Tipo de Vivienda")
    sdueno = fields.Char("Nombre del Dueño")
    sarrtel = fields.Char("Teléfono Arrendador")
    stasen = fields.Selection([("casa", "Casa Sola"),
        ("dep", "Departamento/U. Habitacional/Fraccionamiento"),
        ("rural", "Asentamiento Rural")], string="Tipo de Asentamiento")
    #Croquis
    croquis = fields.Binary("Croquis")
    ncroquis = fields.Char("NCroquis")
    indicaciones = fields.Text("Indicaciones para llegar")
    #Info Adicional
    resultado = fields.Char("Reultado de la Entevista")
    q1 = fields.Boolean("Si")
    q1puesto = fields.Char("Puesto o Cargo")
    q1periodo = fields.Char("Periodo")
    q2 = fields.Boolean("Si")
    q2paterno = fields.Char("Paterno")
    q2materno = fields.Char("Materno")
    q2nombre = fields.Char("Nombre")
    q2parentesco = fields.Char("Paretesco")
    q2puesto = fields.Char("Puesto o cargo")
    q2periodo = fields.Char("Periodo")
    #Ingresos
    imensual = fields.Float("Ingreso Mensual")
    iotros = fields.Float("Otros Ingresos (Mensuales)")
    iconyuge = fields.Float("Ingresos Mensuales del Conyuge")
    #Egresos de Negocio
    enrenta = fields.Float("Renta Mensual")
    enelectricidad = fields.Float("Electricidad")
    engas = fields.Float("Gas")
    enagua = fields.Float("Agua")
    entelefono = fields.Float("Teléfono")
    enimpuestos = fields.Float("Impuestos")
    ensueldos = fields.Float("Sueldos")
    enmaterial = fields.Float("Materia Prima")
    eninventario = fields.Float("Inventario al Final del Mes")
    entransporte = fields.Float("Transporte")
    emcomisiones = fields.Float("Comisiones")
    #Egresos Personales
    eprenta = fields.Float("Renta")
    epgas = fields.Float("Gas")
    epluz = fields.Float("Luz")
    eptelefono = fields.Float("Teléfono")
    epagua = fields.Float("Agua")
    epeducacion = fields.Float("Educación")
    epfamilia = fields.Float("Gastos Familiares")
    epcable = fields.Float("Televisión de Paga")
    epalimentos = fields.Float("Alimentos")

    @api.onchange('nmismo')
    def copy_address(self):
        self.ncalle = self.calle
        self.nnext = self.ext
        self.nint = self.inte
        self.ncol = self.col.id if self.col else None
        self.ncp = self.cp
        self.ncuidad = self.ciudad
        self.nestado = self.estado.id if self.estado else None
        self.nref = self.entrec


class jmdsolicitudn(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.solicitudn"

    def get_oficina(self):
        return "Smart Quo"

    @api.onchange('ingreso')
    @api.depends('ingreso')
    def _get_antiguedad(self):
        for record in self:
            sfecha = str(record.ingreso)
            if not record.ingreso:
                return
            hoy = datetime.datetime.today()
            dtfecha = datetime.datetime.strptime(sfecha, '%Y-%m-%d')
            diferencia = hoy - dtfecha
            edad = diferencia.days / 365
            record.antiq = str(edad) + " Años"

    name = fields.Char("Número", default=lambda self: self.
        env["ir.sequence"].get("sofom.solicitudn"))
    lead_id = fields.Many2one("crm.lead", string="Originacion")
    fecha = fields.Date("Fecha", default=lambda *a: datetime.
        date.today().strftime('%Y-%m-%d'))
    lugar = fields.Selection([("campo", "Campo"), ("oficina", "Oficina")],
        string="LLenado en:", default="oficina")
    oficina = fields.Char("Centro de Negocios", default=get_oficina)
    clave = fields.Integer("Clave Centro de Negocios")
    asesor = fields.Many2one("hr.employee", string="Asesor")
    no_solicitud = fields.Integer("Número de Solicitud")
    monto = fields.Float("Monto Solicitado",
        related="lead_id.credito_solicitado.monto")
    tasa = fields.Float("Tasa", related="lead_id.credito_solicitado.tasa.name")
    plazo = fields.Char("Plazo",
        related="lead_id.credito_solicitado.plazo.name")
    frecuencia = fields.Selection([("26", "Quincenal"), ("52", "Semanal"),
        ("12", "Mensual")], string="Frecuencia",
        related="lead_id.credito_solicitado.frecuencia")
    #Datos Personales
    materno = fields.Char("Apellido Materno",
        related="lead_id.partner_id.materno")
    paterno = fields.Char("Apellido Paterno",
        related="lead_id.partner_id.paterno")
    nombre = fields.Char("Nombre", related="lead_id.partner_id.nombre")
    genero = fields.Selection([("m", "Masculino"), ("f", "Femenino")],
        string="Género")
    nacimiento = fields.Date("Fecha de Nacimiento")
    pais = fields.Char("Pais de Nacimiento", defaukt="México")
    entidad = fields.Char("Entidad Federativa")
    nacionalidad = fields.Char("Nacionalidad", default="Mexicana")
    curp = fields.Char("CURP")
    rfc = fields.Char("RFC")
    pclave = fields.Char("Clave de Elector")
    identificacion = fields.Char("Número de Identificación")
    tipoid = fields.Selection([('ine', 'INE'), ('cedula', 'Cédula Profesional'),
        ('pasaporte', 'Pasaporte'), ('cartilla', 'Cartilla Militar')],
        string="Tipo de Identificación")
    estadoc = fields.Selection([("soltero", "Soltero"), ("casado", "Casado"),
        ("viudo", "Viudo")], string="Estado Civil")
    regimen = fields.Selection([("sc", "Sociedad Conyugal"),
        ("sb", "Separación de Bienes")], string="Regimen Conyugal")
    hijos = fields.Integer("Número de Hijos")
    dependientes = fields.Integer("Número de Dependientes")
    estudios = fields.Selection([("prim", "Primaria"), ("sec", "Secundaria"),
        ("prep", "Preparatoria"), ("lic", "Licenciatura"),
        ("mc", "Maestría"), ("tec", "Carrera Técnica"),
        ("ct", "Carrera Trunca")], string="Último Grado de Estudios")
    experiencia = fields.Selection([("sin", "Sin Experiencia"),
        ("con", "Con Experiencia")], string="Experiencia Crediticia")
    estado_credito = fields.Selection([("sin_atraso", "Sin Atraso"),
        ("sin_historial", "Sin Historial"), ("con_atraso", "Con Atraso")],
        string="Estado de los Créditos Actuales")
    #Solidario
    garantia = fields.Char("Garantia Prendaria")
    snombre = fields.Char("Nombres y Apellidos")
    strabaja = fields.Boolean("Trabaja Actualmente")
    socupacion = fields.Selection([("micro", "Microempresario"),
        ("emp", "Empleado")], string="Ocupación")
    ssector = fields.Selection([("ind", "Industria"), ("com", "Comercio"),
        ("ser", "Servicios")], string="Sector")
    srama = fields.Selection([("principal", "Principal"),
        ("com", "Complementario")], string="Rama del Negocio")
    snnombre = fields.Char("Nombre del Negocio")
    spuesto = fields.Char("Puesto")
    ssueldo = fields.Float("Sueldo Mensual")
    sdom = fields.Char("Domicilio de la Empresa")
    stel = fields.Char("Telefono Oficina")
    scel = fields.Char("Celular")
    scurp = fields.Char("CURP")
    srfc = fields.Char("RFC")
    sclave = fields.Char("Clave de Elector")
    sidentificacion = fields.Char("Número de Identificación")
    stipoid = fields.Selection([('ine', 'INE'),
        ('cedula', 'Cédula Profesional'),
        ('pasaporte', 'Pasaporte'), ('cartilla', 'Cartilla Militar')],
        string="Tipo de Identificación")
    sedad = fields.Integer("Edad")
    sestadoc = fields.Selection([("soltero", "Soltero"), ("casado", "Casado"),
        ("ul", "Unión Libre"), ("viudo", "Viudo")], string="Estado Civil")
    sregimen = fields.Selection([("sc", "Sociedad Conyugal"),
        ("sb", "Separación de Bienes")], string="Regimen Conyugal")
    shijos = fields.Integer("Número de Hijos")
    sdependientes = fields.Integer("Número de Dependientes")
    scalle = fields.Char("Calle")
    sext = fields.Char("Número Exterior")
    sinte = fields.Char("Número Interior")
    scol = fields.Char("Colonia")
    scp = fields.Char("Código Postal")
    sciudad = fields.Char("Cuidad/Municipio")
    sestado = fields.Char("Estado")
    sentrec = fields.Char("Referencia Entre Calles")
    stviv = fields.Selection([("propia", "Propia"), ("pag", "Pagándola"),
        ("ren", "Rentada"), ("fam", "Familiar")], string="Tipo de Vivienda")
    sdueno = fields.Char("Nombre del Dueño")
    sarrtel = fields.Char("Teléfono Arrendador")
    stasen = fields.Selection([("casa", "Casa Sola"),
        ("dep", "Departamento/U. Habitacional/Fraccionamiento"),
        ("rural", "Asentamiento Rural")], string="Tipo de Asentamiento")
    #Domicilio Actual
    calle = fields.Char("Calle", related="lead_id.partner_id.calle")
    ext = fields.Char("Número Exterior", related="lead_id.partner_id.ext")
    inte = fields.Char("Número Interior", related="lead_id.partner_id.inte")
    col = fields.Many2one("utils.colonia", string="Colonia",
        related="lead_id.partner_id.col")
    cp = fields.Char("Código Postal", related="lead_id.partner_id.cp")
    ciudad = fields.Char("Cuidad/Municipio",
        related="lead_id.partner_id.ciudad")
    estado = fields.Many2one("res.country.state", string="Estado",
        related="lead_id.partner_id.estado")
    entrec = fields.Char("Referencia Entre Calles",)
    ares = fields.Char("Años de Residencia")
    tel = fields.Char("Teléfono Fijo", related="lead_id.partner_id.phone")
    cel = fields.Char("Celular", related="lead_id.partner_id.mobile")
    email = fields.Char("Correo Electrónico")
    tviv = fields.Selection([("propia", "Propia"), ("pag", "Pagándola"),
        ("ren", "Rentada"), ("fam", "Familiar")], string="Tipo de Vivienda")
    ttviv = fields.Integer("Años de Residencia")
    dueno = fields.Char("Nombre del Dueño (Si es Rentada Y/O Familiar)")
    telarr = fields.Char("Teléfono del Arrendador")
    renta = fields.Float("Costo de Renta")
    tasen = fields.Selection([("casa", "Casa Sola"),
        ("dep", "Departamento/U. Habitacional/Fraccionamiento"),
        ("rural", "Asentamiento Rural")], string="Tipo de Asentamiento")
    agua = fields.Boolean("Agua Potable")
    drenaje = fields.Boolean("Drenaje")
    gas = fields.Boolean("Gas")
    internet = fields.Boolean("Internet")
    luz = fields.Boolean("Luz")
    cable = fields.Boolean("TV Paga/Satelital")
    telefono = fields.Boolean("Teléfono")
    #Información Laboral
    empresa = fields.Char("Empresa en la Que Labora",
        related="lead_id.partner_id.parent_id.name")
    ldepto = fields.Char("Área o Departamento")
    puesto = fields.Char("Puesto", related="lead_id.partner_id.function")
    antiq = fields.Char("Antigüedad (En Años)")
    ingreso = fields.Date("Fecha Ingreso")
    jefe = fields.Char("Jefe Inmediato")
    lmail = fields.Char("Correo Electrónico")
    lcalle = fields.Char("Calle",
        related="lead_id.partner_id.parent_id.calle")
    lext = fields.Char("Número Exterior",
        related="lead_id.partner_id.parent_id.ext")
    lint = fields.Char("Número Interior",
        related="lead_id.partner_id.parent_id.inte")
    lcol = fields.Many2one("utils.colonia", string="Colonia",
        related="lead_id.partner_id.parent_id.col")
    lcp = fields.Char("Código Postal",
        related="lead_id.partner_id.parent_id.cp")
    lcuidad = fields.Char(string="Ciudad",
        related="lead_id.partner_id.parent_id.ciudad")
    lestado = fields.Many2one("res.country.state", string="Estado",
        related="lead_id.partner_id.parent_id.estado")
    ltel = fields.Char("Teléfono")
    lextension = fields.Char("Extensión")
    lingreso = fields.Char("Ingreso Mensual")
    bonos = fields.Char("Bonos o Compensaciones")
    templeo = fields.Selection([('autoempleo', 'Autoempleo'),
        ('asalariado', 'Asalariado')], string="Tipo de Empleo")
    ttempleo = fields.Integer("Años en el Empleo")
    #Referencias
    r1nombre = fields.Char("Nombre Completo")
    r1dir = fields.Char("Dirección")
    r1cel = fields.Char("Celular")
    r1par = fields.Char("Parentesco")
    r1tiempo = fields.Char("Tiempo de Conocerlo")
    r1mail = fields.Char("Correo Eletrónico")
    r2nombre = fields.Char("Nombre Completo")
    r2dir = fields.Char("Dirección")
    r2cel = fields.Char("Celular")
    r2par = fields.Char("Parentesco")
    r2tiempo = fields.Char("Tiempo de Conocerlo")
    r2mail = fields.Char("Correo Eletrónico")
    #Referencoas
    banco = fields.Char("Banco")
    titular = fields.Char("Nombre del Titular de la Cuenta")
    rnum_cta = fields.Char("Número de Cuenta")
    rclabe = fields.Char("Número de Cuenta CLABE")
    #Croquis
    croquis = fields.Binary("Croquis")
    ncroquis = fields.Char("NCroquis")
    indicaciones = fields.Text("Indicaciones para llegar")
    #Info Adicional
    resultado = fields.Char("Reultado de la Entevista")
    q1 = fields.Boolean("Si")
    q1puesto = fields.Char("Puesto o Cargo")
    q1periodo = fields.Char("Periodo")
    q2 = fields.Boolean("Si")
    q2paterno = fields.Char("Paterno")
    q2materno = fields.Char("Materno")
    q2nombre = fields.Char("Nombre")
    q2parentesco = fields.Char("Paretesco")
    q2puesto = fields.Char("Puesto o cargo")
    q2periodo = fields.Char("Periodo")
    #Documentos
    scredito = fields.Binary("Solicitud de Crédito")
    scname = fields.Char("SC")
    dingresos = fields.Binary("Declaración de Ingresos")
    ning = fields.Char("DI")
    ife = fields.Binary("Identificación Oficial")
    nife = fields.Char("IO")
    cdomicilio = fields.Binary("Comprobante Domiciliario")
    ncdom = fields.Char("CD")
    cingresos = fields.Binary("Comprobante de Ingresos")
    nci = fields.Char("NCI")
    aut = fields.Binary("Autorización de Consulta")
    na = fields.Char("NA")
    #Gastos
    actividad = fields.Char("Actividad")
    area = fields.Char("Area")
    salario = fields.Float("Remuneración Mensual Neta")
    industrial_comercial = fields.Float("Actividad Industrial Y/O Comercial")
    servicios_profesionales = fields.Float("Servicios Profesionales,\
        Honorarios")
    venta = fields.Float("Venta de automoviles, casa, terrenos, obras de arte,\
        etc")
    actividad_financiera = fields.Float("Por actividad financiera")
    otros_ingresos = fields.Float("Otros")
    conyugue = fields.Float("Ingresos del conyugue y/o otros\
        dependientes económicos")
    hipoteca = fields.Float("Credito Hipotecario (Mensual)")
    automotriz = fields.Float("Crédito Automotriz (Mensual)")
    personal = fields.Float("Crédito Personal (Mensual)")
    tarjeta = fields.Float("Tarjetas de Crédito (Mensual)")
    telecomunicaciones = fields.Float("Telecomunicaciones (Mensual)")