# -*- coding:utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.exceptions import UserError
logger = logging.getLogger(__name__)

class Linea_pedido(models.Model):
    _name = 'reto.linea.pedido'
    _description = 'Detalle de Pedido'

    name = fields.Char(string='Linea Pedido', related='pedido_id.name')
    pedido_id = fields.Many2one('reto.pedido', string='Pedido', inverse_name='num_pedido',
                                )  #esto esté mal, no funciona. Mirar desde aquí
    id_proveedor = fields.Many2one('res.partner', string='ID Proveedor', domain="[('is_company', '=', True)]")
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
    precio_p_may = fields.Float(string='Precio prenda mayorista', related='prenda_id.precio_may')
    p_total = fields.Float(string='Total', compute='_calcular_p_total')

    @api.model
    def _get_talla_options(self):
        # Obtén las tallas disponibles para la prenda seleccionada
        talla_options = self.prenda_id.p_talla.mapped('name')

        logging.info(talla_options)

        # Crea una lista de tuplas para el campo de selección
        return [(talla, talla) for talla in talla_options]

    @api.onchange('prenda_id')
    def _onchange_prenda_id(self):
        # Limpiar y actualizar las opciones de talla cuando cambia la prenda
        self.talla_id = False
        return {'domain': {'talla_id': [('id', 'in', self.prenda_id.p_talla.ids)]}}


    @api.onchange('cantidad_p', 'precio_p_may')
    def _onchange_precio(self):
        self.p_total = self.cantidad_p * self.precio_p_may

    @api.depends('cantidad_p', 'precio_p_may')
    def _calcular_p_total(self):
        for rec in self:
            rec.p_total = rec.cantidad_p * rec.precio_p_may


    # @api.onchange('name')
    # def _onchange_name(self):
    #     if self.name:
    #         self.precio_p_may = self.name.precio_may









    # cantidad = fields.Float(string='Cantidad')
    # precio_moneda = fields.Monetary(string='Precio en Moneda')


