# -*- coding: utf-8 -*-
from odoo import models, fields, api
class Location(models.Model):
    _inherit = "stock.location"

    #codigo_sap = fields.Char()

    cod_sucursal_sii = fields.Char(string="Codigo asignado por el SII")

    direccion_sucursal = fields.Char(string='Direccion Sucursal',
                                     help='Dirección de Sucursal',
                                     required=True,
                                     default='')

    # comuna_sucursal = fields.Char(string='Comuna Sucursal',
    #                               help='Comuna de Sucursal',
    #                               required=True,
    #                               default='')
    city_id = fields.Many2one('res.city', string='Comuna Sucursal',
                                      help='Comuna de Sucursal',
                                      default='')
