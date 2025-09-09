# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    stock_state = fields.Selection([('draft', 'Draft'), ('waiting', 'Waiting Another Operation'),
                                    ('confirmed', 'Waiting'), ('assigned', 'Ready'),
                                    ('done', 'Done'), ('cancel', 'Cancelled')],
                                   compute='_compute_stock_state', store=True)

    @api.depends('picking_ids', 'picking_ids.state')
    def _compute_stock_state(self):
        for order in self:
            if not order.picking_ids:
                order.stock_state = 'draft'
            else:
                states = order.picking_ids.mapped('state')
                if 'cancel' in states:
                    order.stock_state = 'cancel'
                elif 'done' in states:
                    order.stock_state = 'done'
                elif 'assigned' in states:
                    order.stock_state = 'assigned'
                elif 'confirmed' in states:
                    order.stock_state = 'confirmed'
                elif 'waiting' in states:
                    order.stock_state = 'waiting'
                else:
                    order.stock_state = 'draft'

    def action_stock_button_validate(self):
        self.picking_ids.button_validate()
