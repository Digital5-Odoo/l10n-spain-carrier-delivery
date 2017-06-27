# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Digital5 S.L.
#                  Jon Erik Ceberio <jonerikceberio@digital5.es>
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

from openerp import models, api, exceptions, _
from unidecode import unidecode


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _get_label_data(self):
        data = super(StockPicking, self)._get_label_data()
        if self.delivery_address_id:
            partner = self.delivery_address_id

            #comprobacion de todos los campos al principio
            must_fields = {'No Street in Shipping address': partner.street,
                           'No Zip in Shipping address': partner.zip,
                           'No City in Shipping address': partner.city,
                           }
            for key, value in must_fields.items():
                if not value:
                    raise exceptions.Warning(_('%s' % key))
            data.update({
                'cliente_direccion': unidecode(partner.street +
                                               ((' ' + partner.street2) or '')),
                'cliente_poblacion': unidecode(partner.city),
                'cliente_cpostal': unidecode(partner.zip),
                'cliente_pais': unidecode(partner.country_id.code),
            })
        if self.consignee_id:
            data.update({
                'cliente_nombre': unidecode(self.consignee_id.name),
                'cliente_email': unidecode(self.consignee_id.email or u''),
                'cliente_telefono': unidecode(
                    self.consignee_id.phone or self.consignee_id.mobile or u''),
                'cliente_atencion': unidecode(self.consignee_id.name),
            })
        return data
