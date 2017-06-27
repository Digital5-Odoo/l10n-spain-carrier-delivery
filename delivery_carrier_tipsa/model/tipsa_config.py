# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 FactorLibre (http://www.factorlibre.com)
#                  Hugo Santos <hugo.santos@factorlibre.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api


class TipsaConfig(models.Model):
    _name = 'tipsa.config'

    @api.model
    def _get_tipsa_report_format(self):
        return [
            ('90', 'Default'),
            ('99', 'NUEVA etiqueta drivers'),
            ('100',
             'Etiquetas nuevas por códigos de escape (Modelo LP 2844-Z)'),
            ('101',
             'Etiquetas nuevas por códigos de escape (Modelo LP 2844)'),
        ]

    name = fields.Char("Configuration Description", required=True)
    is_test = fields.Boolean('Is a test?')
    agency_code = fields.Char("Agency Code", required=True)
    customer_code = fields.Char("Customer Code", required=True)
    customer_password = fields.Char("Customer Password", required=True)
    report_format = fields.Selection('_get_tipsa_report_format',
                                     string="Report Format", required=True)
