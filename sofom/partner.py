# -*- coding: utf-8 -*-
from openerp import models, fields, api


class jmdaccount(models.Model):
    _inherit = "res.partner"

    @api.one
    def get_link(self):
        self.gmap = "http://maps.google.com/?q=" +\
            str(self.partner_latitude) + "," + str(self.partner_longitude)
        return True

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
    #nombre
    materno = fields.Char("Apellido Materno")
    paterno = fields.Char("Apellido Paterno")
    nombre = fields.Char("Nombre")
    ncliente = fields.Char("Numero de Cliente", size=7,
        default=lambda self: self.env["ir.sequence"].get("res.partner"))
    #Dirección
    calle = fields.Char("Calle")
    ext = fields.Char("Número Exterior")
    inte = fields.Char("Número Interior")
    col = fields.Many2one("utils.colonia", string="Colonia")
    cp = fields.Char("Código Postal")
    ciudad = fields.Char("Cuidad/Municipio")
    estado = fields.Many2one("res.country.state", string="Estado")
    #Ciclo
    ciclo = fields.Integer("Ciclo", default=0)
    #Link Google Maps
    gmap = fields.Char("Mapa", compute=get_link)

    @api.onchange('materno', 'paterno', 'nombre')
    def set_name(self):
        materno = self.materno if self.materno else ""
        paterno = self.paterno if self.paterno else ""
        nombre = self.nombre if self.nombre else ""
        self.name = nombre + " " + paterno + " " + materno

    @api.onchange('calle', 'ext', 'inte')
    def set_street(self):
        calle = self.calle if self.calle else ""
        ext = str(self.ext) if self.ext else ""
        inte = " Int. " + str(self.inte) if self.inte else ""
        self.street = calle + " " + ext + " " + inte

    @api.onchange('cp')
    def set_zip(self):
        self.zip = self.cp if self.cp else ""

    @api.onchange('col')
    def onchange_col(self):
        self.city = self.col.ciudad if (self.col and self.col.ciudad) else ""
        self.street2 = self.col.name if (self.col and self.col.name) else ""

    @api.onchange('estado')
    def onchange_(self):
        self.state_id = self.estado.id if self.estado else ""