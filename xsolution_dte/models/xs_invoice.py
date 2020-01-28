# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
import requests


class xs_invoice(models.Model):
    _inherit = 'account.invoice'
    folio_dte = fields.Text("Folio DTE")
    tipo_dte =  fields.Selection(
        [
            ('33', 'Factura Electrónica'),
            ('34', 'Factura No Afecta o Exenta Electrónica'),
            ('39', 'Boleta de Venta Electrónica'),
            ('43', 'Liquidación-Factura Electrónica'),
            ('46', 'Factura de Compra Electrónica.'),
            ('52', 'Guía de Despacho Electrónica'),
            ('56', 'Nota de Débito Electrónica'),
            ('61', 'Nota de Crédito Electrónica'),
            ('110', 'Factura de Exportación.'),
            ('111', 'Nota de Débito de Exportación.'),
            ('112', 'Nota de Crédito de Exportación'),

        ],
        string="Tipo Documento",
    )
    xml_dte = fields.Text("XML")
    ted = fields.Text("TED")
    url_pdf = fields.Text("URL PDF")
    #estado_envio = fields.Text("Estado Envío")

    referencias = fields.One2many(
        'account.invoice.referencias',
        'invoice_id',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    forma_pago = fields.Selection(
        [
            ('1', 'Contado'),
            ('2', 'Crédito'),
            ('3', 'Gratuito')
        ],
        string="Forma de pago",
        readonly=True,
        states={'draft': [('readonly', False)]},
        default='1',
    )

    @api.one
    def enviar_sii(self):
        #PARA COMPLETAR EL DOCUMENTO SE DEBE BASAR EN http://www.sii.cl/factura_electronica/formato_dte.pdf

        dte = {}
        dte["Encabezado"] = {}
        # El Portal completa los datos del Emisor
        dte["Encabezado"]["IdDoc"] = {"TipoDTE": self.tipo_dte}
        #Si es Boleta de debe indicar el tipo de servicio, por defecto de venta de servicios
        if self.tipo_dte in ('39', 39):
            dte["Encabezado"]["IdDoc"]["IndServicio"] = 3

        if not self.tipo_dte in ('39', 39):
            #Se debe inicar SOLO SI los valores indicados en el documento son con iva incluido
            dte["Encabezado"]["IdDoc"]["MntBruto"] = 1

        #EL CAMPO VAT o NIF De la empresa, debe corresponder al RUT de la Empresa
        dte["Encabezado"]["Emisor"] = {"RUTEmisor": self.company_id.vat.replace(".","")}

        # EL CAMPO VAT o NIF Del Partner, debe corresponder al RUT , si es empresa extranjera debe ser 55555555-5
        dte["Encabezado"]["Receptor"] = {"RUTRecep": self.partner_id.vat.replace(".",""),
                                         "RznSocRecep": self.partner_id.name,
                                         "DirRecep": self.partner_id.street +  ' ' + self.partner_id.city,
                                         "CmnaRecep": self.partner_id.city,
                                         "GiroRecep": self.partner_id.giro}
        dte["Encabezado"]["IdDoc"] = {}
        dte["Encabezado"]["IdDoc"]["TermPagoGlosa"] = self.comment
        dte["Detalle"] = []
        for linea in self.invoice_line_ids:
            #El Portal Calculos los Subtotales
            ld = {'NmbItem': linea.product_id.name,
             'DscItem': '',
             'QtyItem': round(linea.quantity, 6),
             'PrcItem': round(linea.price_unit,4)
            }
            if linea.product_id.default_code:
                ld['CdgItem'] = {"TpoCodigo": "INT1",
                              "VlrCodigo": linea.product_id.default_code}
            if linea.discount:
                ld['DescuentoPct']= round(linea.discount,2)
            dte["Detalle"].append(ld)
        referencias = []
        for referencia in self.referencias:
            ref = {'TpoDocRef':referencia.TpoDocRef or 'SET',
                   'FolioRef':referencia.folio_referencia,
                   'FchRef':referencia.fecha_documento.__str__(),
                   'RazonRef':referencia.motivo}
            if referencia.CodRef:
                ref['CodRef'] =referencia.CodRef
            referencias.append(ref)
        if referencias:
            dte['Referencia'] = referencias
        print(dte)

        self.enviar(json.dumps(dte))

    def enviar(self, dte):
        url = self.company_id.url_dte
        rut_emisor = self.company_id.vat.replace(".", "").split("-")[0]
        hash = self.company_id.hash_dte
        auth = requests.auth.HTTPBasicAuth(hash, 'X')
        ssl_check = False
        # Api para Generar DTE
        apidte = '/dte/documentos/gendte?getXML=true&getPDF=false&getTED=png'
        emitir = requests.post(url + '/api' + apidte, dte, auth=auth, verify=ssl_check)
        if emitir.status_code != 200:
            print('Error al Temporal: ' + emitir.json())
            raise Exception('Error al Temporal: ' + emitir.json())
        data = emitir.json()
        self.folio_dte = data.get('folio', None)
        self.xml_dte = data.get("xml", None)
        self.ted = data.get("ted", None)
        fecha = data.get("fecha", None)
        total = data.get("total", None)
        self.url_pdf = "%s/dte/dte_emitidos/pdf/%s/%s/0/%s/%s/%s" % (url, self.tipo_dte, self.folio_dte, rut_emisor, fecha, total)


class xs_referencias(models.Model):
    _name = 'account.invoice.referencias'
    _description = 'Referencias de un DTE'

    TpoDocRef = fields.Selection(
            [
                ('33', 'Factura Electronica'),
                ('52', 'Guia d Despacho electrónica'),
                ('61', 'Nota de CRédito electronica'),
                ('39', 'Boleta de Venta Electrónica'),
                ('801', 'Orden de Compra'),
                ('HES', 'HES')
            ],
            string="Tipo Documento Referencia",
        )
    CodRef = fields.Selection(
            [
                ('1', 'Anula Documento de Referencia'),
                ('2', 'Corrige texto Documento Referencia'),
                ('3', 'Corrige montos')
            ],
            string="Tipo referencia",
        )
    motivo = fields.Char(
            string="Motivo",
        )
    folio_referencia = fields.Text(
            string="Numero Documento referencia",
            required=True,
        )
    fecha_documento = fields.Date(
            string="Fecha Documento",
            required=True,
    )
    invoice_id = fields.Many2one(
        'account.invoice',
        ondelete='cascade',
        index=True,
        copy=False,
        string="Documento",
    )