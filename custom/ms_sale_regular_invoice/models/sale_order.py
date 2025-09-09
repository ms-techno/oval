# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_create_regular_invoice(self):
        invoice = self.env['sale.advance.payment.inv'].with_context({
            'active_model': 'sale.order',
            'active_ids': [self.id],
            'active_id': self.id,
        }).create({
            'advance_payment_method': 'delivered',
        })
        invoice.create_invoices()
