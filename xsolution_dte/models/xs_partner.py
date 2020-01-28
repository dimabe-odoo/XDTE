from odoo import models, fields, api
import re


class XSPartner(models.Model):
    _inherit = 'res.partner'
    giro = fields.Char(string='Giro')



