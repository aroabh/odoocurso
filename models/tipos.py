# -*- coding:utf-8 -*-

from odoo import fields, models, api


class Tipos(models.Model):
    _name = 'reto.tipos'
    _description = 'Tipos Model'

    name = fields.Char(string='Tipo de prenda')
