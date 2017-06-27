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


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def _get_origin_address(self):
        return self.origin_address_id

    @api.multi
    def _get_destination_address(self):
        return self.delivery_address_id

    @api.multi
    def _mrw_transm_envio_request(self, mrw_api):
        self.ensure_one()
        transm_envio = super(StockPicking, self)._mrw_transm_envio_request(mrw_api)
        if self.consignee_id:
            if self.consignee_id.email:
                transm_envio.DatosServicio.Notificaciones.NotificacionRequest[0].MailSMS = self.consignee_id.email
            transm_envio.DatosEntrega.Nif = self.consignee_id.vat or ''
            transm_envio.DatosEntrega.Nombre = self.consignee_id.name  # Obligatorio
            if self.consignee_id.phone:
                transm_envio.DatosEntrega.Telefono = self.consignee_id.phone  # Opcional - Muy recomendable
        return transm_envio

    @api.multi
    def _generate_mrw_label(self, package_ids=None):
        self.ensure_one()
        if not self.origin_address_id:
            raise exceptions.Warning(_('Please define an origin address'))
        return super(StockPicking, self)._generate_mrw_label(package_ids=package_ids)
