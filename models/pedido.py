# -*- coding:utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.exceptions import UserError
logger = logging.getLogger(__name__)


class Pedido(models.Model):
    _name = 'reto.pedido'
    _description = 'Cabecera de Pedido'

    name = fields.Char(string='Compra')
    fecha_compra = fields.Date(string='Fecha de Compra', default=fields.Date.today())
    linea_pedido_ids = fields.One2many('reto.linea.pedido', 'pedido_id', string='Detalles del Pedido')
    num_pedido = fields.Char(string='Número de pedido', copy=False)
    tot_prendas_pedido = fields.Float(string='Total Prendas en Pedido', compute='_compute_tot_prendas_pedido',
                                      store=True)
    precio_total = fields.Float(string='Precio total pedido',  compute='_compute_total')
    base = fields.Float(string='Base pedido', compute='_compute_total')
    impuestos = fields.Float(string='impuestos pedido')
    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado')
    ], default='borrador', string='Estado', copy=False)

    fch_creacion = fields.Datetime(string="Fecha creación", copy=False,
                                   default=lambda self: fields.Datetime.now())
    fch_aprobado = fields.Datetime(string='fecha aprobado', copy=False)
    fch_cancelado = fields.Datetime(string='fecha cancelado', copy=False)

    @api.model
    def create(self, variables):
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.numero.pedido')
        variables['num_pedido'] = correlativo
        return super(Pedido, self).create(variables)

    @api.depends('linea_pedido_ids.p_total')
    def _compute_tot_prendas_pedido(self):
        for pedido in self:
            tot_prendas = sum(pedido.linea_pedido_ids.mapped('p_total'))
            pedido.tot_prendas_pedido = tot_prendas

    @api.depends('linea_pedido_ids')
    def _compute_total(self):
        for record in self:
            sub_total = 0
            for linea in record.linea_pedido_ids:
                sub_total += linea.p_total
            record.base = sub_total
            record.impuestos = sub_total * 0.21
            record.precio_total = sub_total * 1.21

    def aprobar_presupuesto(self):
        logger.info('Estamos en entrado en aprobar presuesto')
        self.state='aprobado'
        self.fch_aprobado= fields.Datetime.now()
        obj_stock = self.env['reto.stock']
        for linea in self.linea_pedido_ids:
            prod = linea.prenda_id
            tall = linea.talla_id
            col = linea.color_id
            cant = linea.cantidad_p
            compr = obj_stock.search([('prenda_id', '=', prod.id), ('talla_id', '=', tall.id), ('color_id', '=', col.id)])
            if compr:
                compr.write({'cantidad_p': compr.cantidad_p + cant})
            else:
                obj_stock.create({'pedido_id': self.name, 'prenda_id': prod.id, 'talla_id': tall.id,
                                  'color_id': col.id, 'cantidad_p': cant})

    def cancelar_presupuesto(self):
        logger.info('Entrando en cancelar presupuesto')
        self.state = 'cancelado'
        self.fch_cancelado = fields.Datetime.now()

    def unlink(self):
        for presupuesto in self:
            if presupuesto.state == 'cancelado':
                logger.warning('*********** Eliminando presupuesto ****************')
                super(Pedido, presupuesto).unlink()
            else:
                raise UserError('********* no se puede eliminar presupuesto *******')

