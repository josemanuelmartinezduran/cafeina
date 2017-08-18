# -*- coding: utf-8 -*-
from openerp import models, fields


class jmdaccount(models.Model):
    _inherit = "mail.thread"
    _name = "sofom.blacklist"
    name = fields.Char("Nombre")