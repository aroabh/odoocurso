# -*- coding:utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import Warning

class UpdateWizard(models.TransientModel):
    _name = 'update.wizard'
    _description = 'Wizard para actualizar stock'

    name = fields.Text(string='Mensaje', readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(UpdateWizard, self).default_get(fields)
        res.update({
            'name': self.env.context.get('default_name', False)
        })
        return res

    def confirm_action(self):
        return {'type': 'ir.actions.act_window_close'}