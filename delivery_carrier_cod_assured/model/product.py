# -*- coding: utf-8 -*-


from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    assured_amount = fields.Float(digits=dp.get_precision('Sale Price'))
