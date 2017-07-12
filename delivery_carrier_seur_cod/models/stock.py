# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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

from openerp import models, fields, api, exceptions
from unidecode import unidecode


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def _get_label_data(self):
        data = super(StockPicking, self)._get_label_data()
        if self.sale_id and self.sale_id.payment_mode_id == self.carrier_id.seur_config_id.cod_payment_mode_id:
            data['clave_reembolso'] = self.carrier_id.seur_config_id.cod_type
            if self.carrier_id.seur_config_id.cod_type == "D":
                data['valor_reembolso'] = str(self.amount_cod)
            elif self.carrier_id.seur_config_id.cod_type == "F":
                cur = self.sale_id and self.sale_id.pricelist_id.currency_id or self.company_id.currency_id
                data['valor_reembolso'] = str(cur.round(self.amount_cod * (1 + self.carrier_id.seur_config_id.perc_commission / 100)))
        return data

