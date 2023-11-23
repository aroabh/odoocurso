# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Colores(models.Model):
    _name = 'reto.colores'
    _description = 'Colores Model'

    name = fields.Char(string='Color')
    color_id = fields.Many2one(comodel_name='reto.linea.pedido', string='Color')


