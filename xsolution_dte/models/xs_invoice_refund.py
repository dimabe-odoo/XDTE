# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
import requests

from odoo.exceptions import UserError


class xs_invoice_refund(models.TransientModel):
    _inherit = 'account.invoice.refund'

    def compute_refund(self,mode='refund'):
        result = super(xs_invoice_refund, self).compute_refund()
        for doc in self.env['account.invoice'].search(result.get('domain')):
            doc.tipo_dte ='61'
            referencia_ok = False
            if ref.folio_dte:
                if ref.tipo_dte in ('33','39') and ref.folio_dte:
                    referencia_ok = True
                for ref in self.env['account.invoice'].browse(self._context.get('active_id',False)):
                    self.env['account.invoice.referencias'].create(
                        {'TpoDocRef': ref.tipo_dte, 'CodRef': '1', 'motivo': 'Anula Documento', 'folio_referencia': ref.folio_dte, 'fecha_documento': ref.date_invoice, 'invoice_id': doc.id})
            if not referencia_ok:
                raise UserError('El documento debe referenciar a una Boleta Electrónica y/o Factura Electrónica')
        return result