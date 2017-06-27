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
import urllib
from datetime import datetime
from openerp import models, fields, api, exceptions
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def _mrw_transm_envio_request(self, mrw_api):
        self.ensure_one()
        transm_envio = super(StockPicking, self)._mrw_transm_envio_request(mrw_api)
        service_data = transm_envio.DatosServicio
        
        if self.sale_id and self.sale_id.payment_method_id == self.carrier_id.mrw_config_id.cod_payment_id:
            service_data.Reembolso = self.carrier_id.mrw_config_id.cod_type
            if self.carrier_id.mrw_config_id.cod_type == "D":
                service_data.ImporteReembolso = str(self.amount_cod).replace(".", ",")
            elif self.carrier_id.mrw_config_id.cod_type == "O":
                cur = self.sale_id and self.sale_id.pricelist_id.currency_id or self.company_id.currency_id
                service_data.ImporteReembolso = str(cur.round(self.amount_cod * (1 + self.carrier_id.mrw_config_id.perc_commission / 100))).replace(".", ",")

        if self.amount_assured > 0.0:
            service_data.SeguroOpcional.CodigoNaturaleza = "1"
            service_data.SeguroOpcional.ValorAsegurado = str('%.2f' % self.amount_assured).replace(".", ",")

        return transm_envio
