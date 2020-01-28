# -*- coding: utf-8 -*-
####################   XSOLUTION      #######################
#    XSolution SpA Base
#    Copyright (C) 2019-XSolution(<http://www.xsolution.cl>).
#    Author: vbenitez(<http://www.xsolution.cl>)
####################   XSOLUTION      ##########################

#
#
#
{
    'name': 'XSolution BASE',
    'summary': """Base Facturacion Electrónica Chile""",
    'version': '12.0.1.0',
    'description': """Datos Base para el funcionamiento de Facturacion Electronica""",
    'author': 'XSolution',
    'company': 'XSolution ',
    'website': 'http://www.xsolution.cl',
    'category': 'Point of Sale',
    'depends': ['base','stock','account'],
    'license': 'OPL-1',
    'data': [
    	'views/xs_company.xml',
    	'views/xs_location.xml',
        'views/xs_partner.xml',
        'views/xs_invoice.xml',
        'security/ir.model.access.csv'
    ],
    'qweb': [],
    'images': [],
    'demo': [],        
    'installable': True,
    'application': True,
    'auto_install': False,

}
