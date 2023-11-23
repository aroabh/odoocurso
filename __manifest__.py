# -*- coding:utf-8 -*-

{
    'name': 'Tienda de ropa',
    'version': '1.0',
    'depends':['base', 'mail'],
    'author': 'Aroa',
    'category': 'Ropa',
    'website': '',
    'description': '''Módulo reto para crear una Tienda de Ropa''',
    'data' :[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/secuencia.xml',
        'views/menu.xml',
        'views/prenda.xml',
        'views/pedido.xml',
        'views/stock.xml',
        'views/ventas.xml',
        'views/search_colors.xml',
        'report/reporte_pedido.xml',
        'wizard/update_wizard_views.xml',
        'wizard/update_wizard_action.xml'
    ]
}

