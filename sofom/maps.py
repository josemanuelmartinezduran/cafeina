# -*- coding: utf-8 -*-
from openerp import models, fields, api


class jmdmaps(models.Model):
    _inherit = "mail.thread"
    _name = "utils.map"
    name = fields.Char("Nombre")
    key = fields.Char("Key")
    zoom = fields.Integer("Zoom")
    center = fields.Char("Centro")
    mapa = fields.Char("Mapa")
    size = fields.Char("Tamaño")
    marker_ids = fields.One2many("utils.map.marker", "mapa_id",
        string="Marcadores")

    @api.one
    def generate_map(self):
        ret = {}
        for i in self.marker_ids:
            i.unlink()
        #LLenando los marcadores
        for i in self.env["res.partner"].search([]):
            if i.partner_latitude:
                self.env["utils.map.marker"].create(
                    {'latitude': i.partner_latitude,
                    'longitude': i.partner_longitude,
                    'name': (i.name + " " + i.street +
                        " "),
                    'mapa_id': self.id})
        cadena = "http://maps.mydsolutions.com/index.php?"
        cadena += "zoom=" + str(self.zoom)
        cadena += "&size=" + str(self.size)
        cadena += "&center=" + str(self.center)
        cadena += "&key=" + str(self.key)
        for i in self.marker_ids:
            cadena += "&markers[]=" + str(i.latitude) + "," + str(i.longitude)\
                + "," + i.name
        self.mapa = cadena
        return ret


class jmdmarker(models.Model):
    _name = "utils.map.marker"
    name = fields.Char("Titulo")
    latitude = fields.Char("Latitud")
    longitude = fields.Char("Longitud")
    mapa_id = fields.Many2one("utils.map", "Mapa")