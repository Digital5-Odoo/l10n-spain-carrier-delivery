# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    tracking_url = fields.Char()
