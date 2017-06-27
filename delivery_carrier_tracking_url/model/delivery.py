# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    tracking_url = fields.Char()
