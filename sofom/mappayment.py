# -*- coding: utf-8 -*-
from openerp import models, fields, api


class jmdmaps(models.Model):
    _inherit = "mail.thread"
    _name = "utils.mappay"
    name = fields.Char("Nombre")
    key = fields.Char("Key")
    zoom = fields.Integer("Zoom")
    center = fields.Char("Centro")
    mapa = fields.Char("Mapa")
    size = fields.Char("Tamaño")
    marker_ids = fields.One2many("utils.mappay.marker", "mapa_id",
        string="Marcadores")
    start = fields.Date("Fecha de Inicio")
    end = fields.Date("Fecha de Fin")

    @api.one
    def generate_map(self):
        ret = {}
        for i in self.marker_ids:
            i.unlink()
        for j in self.env["sofom.pago"].search([]):
            fecha_pago = j.fecha
            print("Fecha de Pago")
            print(fecha_pago)
            print("Fecha de Inicio")
            print((str(self.start)))
            print("Es Mayor")
            print((str(self.start < fecha_pago)))
            i = j.credito_id.titular
            if i.partner_latitude and self.start <= fecha_pago\
                and self.end >= fecha_pago:
                self.env["utils.mappay.marker"].create(
                    {'latitude': i.partner_latitude,
                    'longitude': i.partner_longitude,
                    'name': i.name + str(j.name) + " " + str(j.saldo),
                    'mapa_id': self.id})
        cadena = "http://maps.mydsolutions.com/index.php?"
        cadena += "zoom=" + str(self.zoom)
        cadena += "&center=" + str(self.center)
        cadena += "&key=" + str(self.key)
        for i in self.marker_ids:
            cadena += "&markers[]=" + str(i.latitude) + "," + str(i.longitude)\
                + "," + str(i.name)
        self.mapa = cadena
        return ret


class jmdmarker(models.Model):
    _name = "utils.mappay.marker"
    name = fields.Char("Titulo")
    latitude = fields.Char("Latitud")
    longitude = fields.Char("Longitud")
    mapa_id = fields.Many2one("utils.mappay", "Mapa")