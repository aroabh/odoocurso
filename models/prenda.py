# -*- coding:utf-8 -*-

from odoo import models, fields, api


class Prenda(models.Model):
    _name = 'reto.prenda'
    _description = 'Prenda'

    name = fields.Char(string='Prenda', required=True)

    prenda_id = fields.Many2one('reto.linea.pedido', string='Prenda')

    genero = fields.Selection(selection=[
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
        ('Unisex', 'Unisex'),
        ('Mascotas', 'Mascotas'),
    ], string='Género')
    precio_may = fields.Float(string='Precio mayorista')
    p_tipo = fields.Many2one(comodel_name='reto.tipos', string='Tipo')

    p_colores = fields.One2many(comodel_name='reto.colores.rel', inverse_name='prenda_id', string='Colores')

    p_talla = fields.One2many(comodel_name='reto.tallas.rel', inverse_name='prenda_id', string='Tallas')

    proveedor_ids = fields.Many2one(comodel_name='res.partner',
                                    string='Proveedor', domain="[('is_company', '=', True)]")

    linea_pedido_ids = fields.One2many('reto.linea.pedido', 'prenda_id', string='Líneas de Pedido')

    imagen = fields.Binary(string='imagen')


class ColoresRel(models.Model):
    _name = 'reto.colores.rel'
    _description = 'Relación Colores y Prendas'

    name = fields.Char(string='Color', related='color_id.name')
    prenda_id = fields.Many2one('reto.prenda', string='Prenda')
    color_id = fields.Many2one('reto.colores', string='Color')


class TallasRel(models.Model):
    _name = 'reto.tallas.rel'
    _description = 'Relación Tallas y Prendas'

    name = fields.Char(string='Talla', related='talla_id.name')
    prenda_id = fields.Many2one('reto.prenda', string='Prenda')
    talla_id = fields.Many2one('reto.tallas', string='Talla')



