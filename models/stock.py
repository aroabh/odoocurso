# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Stock(models.Model):
    _name = 'reto.stock'
    _description = 'Stock Model'

    name = fields.Char(string='Stock')
    pedido = fields.Many2many('reto.pedido', string='Compra')

    pedido_id = fields.Many2one('reto.pedido', string='Pedido', inverse_name='num_pedido')
    venta_id = fields.Many2one('reto.ventas', string='Venta', inverse_name='num_venta')

    prenda_id = fields.Many2one(
        comodel_name='reto.prenda', inverse_name='linea_pedido_ids', string='Prenda',
        domain="[('proveedor_ids', '=', id_proveedor)]"
    )

    talla_id = fields.Many2one(
        comodel_name='reto.tallas.rel', inverse_name='talla_id', string='Talla',
        domain="[('prenda_id', '=', prenda_id)]",

    )

    color_id = fields.Many2one(
        comodel_name='reto.colores.rel', inverse_name='color_id', string='Color',
        domain="[('prenda_id', '=', prenda_id)]"
    )
    cantidad_p = fields.Integer(string='Cantidad')
    id_proveedor = fields.Many2one('res.partner', string='ID Proveedor', domain="[('is_company', '=', True)]")





