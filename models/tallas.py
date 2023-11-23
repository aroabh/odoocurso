# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Tallas(models.Model):
    _name = 'reto.tallas'
    _description = 'Talla Model'

    name = fields.Char(string='Talla')

