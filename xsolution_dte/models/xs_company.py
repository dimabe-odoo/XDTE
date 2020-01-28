from odoo import models, fields, api
import re

#from odoo.odoo import fields


class XSCompany(models.Model):
    _inherit = 'res.company'
    giro = fields.Char(string='Giro')
    acteco = fields.Char(string='Actividad Economica',
                         help='Codigo de actividad Economica asignada por el SII',
                         required=True,
                         default='102030')
    url_dte = fields.Char(string='URL portal de Facturacion',
                          help='',
                          required=True,
                          default='http://dte.xdte.cl/')
    url_boletas = fields.Char(string='URL Validacion de Boletas',
                          help='',
                          required=True,
                          default='http://dte.xdte.cl/boletas')
    fecha_resolucion = fields.Date(string='Fecha Resolución',
                         help='Fecha de Resolución entregada por el SII',
                         required=True,
                         default='2014-08-22')
    num_resolucion = fields.Integer(string='Numero Resolución',
                                   help='Número de Resolución entregada por el SII',
                                   required=True,
                                   default='80')
    hash_dte = fields.Char(string='Hash de Facturación',
                                    help='Hash de acceso al Facturador Electrónico',
                                    required=True,
                                    default='')

