# -*- coding: utf-8 -*-


from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"

    product_assured = fields.Boolean(string="Product Assured")
    assured_amount = fields.Float(string='Assured Amount', digits=dp.get_precision('Account'), help="The amount assured per product unit")
    cod_amount = fields.Float(string='Cash on Delivery Amount', digits=dp.get_precision('Account'), copy=False)

    @api.onchange('product_assured')
    def _onchange_product_assured(self):
        if self.product_assured is True and self.assured_amount == 0.0:
            self.assured_amount = self.product_id.assured_amount
        elif self.product_assured is False:
            self.assured_amount = 0.0
