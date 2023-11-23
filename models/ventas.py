# -*- coding:utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.exceptions import UserError
logger = logging.getLogger(__name__)

class Ventas(models.Model):
    _name = 'reto.ventas'
    _description = 'Ventas Model'

    name = fields.Char(string='Venta')
    fecha_venta = fields.Date(string='Fecha de Venta', default=fields.Date.today())
    linea_venta_ids = fields.One2many('reto.linea.venta', 'venta_id', string='Detalles de la Venta')
    num_venta = fields.Char(string='Número de venta', copy=False)
    tot_prendas_venta = fields.Float(string='Total Prendas en venta', compute='_compute_tot_prendas_venta',
                                      store=True)
    precio_total = fields.Float(string='Precio total venta', compute='_compute_total')
    base = fields.Float(string='Base venta', compute='_compute_total')
    impuestos = fields.Float(string='impuestos venta')
    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado')
    ], default='borrador', string='Estado', copy=False)

    fch_creacion = fields.Datetime(string="Fecha creación", copy=False,
                                   default=lambda self: fields.Datetime.now())
    fch_aprobado = fields.Datetime(string='fecha aprobado', copy=False)
    fch_cancelado = fields.Datetime(string='fecha cancelado', copy=False)
    cliente = fields.Many2one('res.partner', string = 'Cliente')

    @api.model
    def create(self, variables):
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.numero.venta')
        variables['num_venta'] = correlativo
        return super(Ventas, self).create(variables)

    @api.depends('linea_venta_ids.p_total')
    def _compute_tot_prendas_venta(self):
        for venta in self:
            tot_prendas = sum(venta.linea_venta_ids.mapped('p_total'))
            venta.tot_prendas_venta = tot_prendas

    @api.depends('linea_venta_ids')
    def _compute_total(self):
        for record in self:
            sub_total = 0
            for linea in record.linea_venta_ids:
                sub_total += linea.p_total
            record.base = sub_total
            record.impuestos = sub_total * 0.21
            record.precio_total = sub_total * 1.21

    def aprobar_presupuesto(self):
        logger.info('Estamos en entrado en aprobar presupuesto')
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()
        obj_stock = self.env['reto.stock']

        for linea in self.linea_venta_ids:
            prod = linea.prenda_id
            tall = linea.talla_id
            col = linea.color_id
            cant = linea.cantidad_p
            stock_entry = obj_stock.search([
                ('prenda_id', '=', prod.id),
                ('talla_id', '=', tall.id),
                ('color_id', '=', col.id)
            ], limit=1)

            if stock_entry and stock_entry.cantidad_p >= cant:
                stock_entry.write({'cantidad_p': stock_entry.cantidad_p - cant})
            else:
                self.state = 'borrador'
                mensaje = f"No hay suficiente stock para la prenda '{prod.name}', talla '{tall.name}', color '{col.name}'. Stock disponible: {stock_entry.cantidad_p if stock_entry else 0}"
                context = {
                    'default_name': mensaje,
                }
                return {
                    'name': 'Actualizar Stock',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'view_id': self.env.ref('tienda_ropa.view_update_wizard_form').id,
                    # Reemplaza 'tu_modulo' con el nombre de tu módulo
                    'view_type': 'form',
                    'res_model': 'update.wizard',
                    'target': 'new',
                    'context': context,
                }

    def cancelar_presupuesto(self):
        logger.info('Entrando en cancelar presupuesto')
        self.state = 'cancelado'
        self.fch_cancelado = fields.Datetime.now()

    def unlink(self):
        for presupuesto in self:
            if presupuesto.state == 'cancelado':
                logger.warning('*********** Eliminando presupuesto ****************')
                super(Ventas, presupuesto).unlink()
            else:
                raise UserError('********* no se puede eliminar presupuesto *******')