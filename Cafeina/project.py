#-*-coding:utf-8-*-
from openerp import models, fields, api
from datetime import datetime


#Task management changes
class jmd_task(models.Model):
    _inherit = "account.analytic.line"
    start = fields.Datetime("Inicio") 
    end = fields.Datetime("Fin")
    
    @api.one
    def timer_start(self):
        ret = {}
        self.write({'start': datetime.today().strftime("%m-%d-%Y %H:%M:%S")})
        return ret
        
    @api.one
    def timer_stop(self):
        ret = {}
        self.write({'end': datetime.today().strftime("%m/%d/%Y %H:%M:%S")})
        end = datetime.strptime(self.end , "%Y-%m-%d %H:%M:%S")
        start = datetime.strptime(self.start , "%Y-%m-%d %H:%M:%S")
        delta = end - start
        print("La diferencia es de ")
        print(delta.seconds)
        horas = delta.seconds / 3600.00
        print(horas)
        self.write({'unit_amount': horas})
        return ret
