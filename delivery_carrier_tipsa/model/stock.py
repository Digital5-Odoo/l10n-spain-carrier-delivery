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
from datetime import datetime
from openerp import models, fields, api, exceptions, _
from ..webservice.tipsa_api import TipsaLogin, TipsaWebService


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _get_tipsa_service_type(self):
        return [
            ('14', '14 Horas (premium)'),
            ('48', 'Economy'),
            ('10', 'Antes 10'),
            ('MV', 'Masivo'),
            ('20', 'Recoger en delegacion')
        ]

    tipsa_service_type = fields.Selection(
        '_get_tipsa_service_type', string='Tipsa Service')

    @api.multi
    def _generate_tipsa_label(self, package_ids=None):
        self.ensure_one()
        if not self.carrier_id.tipsa_config_id:
            raise exceptions.warning(_('No tipsa config defined in carrirer'))
        if not self.picking_type_id.warehouse_id.partner_id:
            raise exceptions.Warning(
                _('Please define an address in the %s warehouse') % (
                    self.warehouse_id.name))
        warehouse_partner = self.picking_type_id.warehouse_id.partner_id

        tipsa_config = self.carrier_id.tipsa_config_id
        tipsa_login = TipsaLogin(tipsa_config)
        login_session = tipsa_login.session_code()
        tipsa_ws = TipsaWebService(self.carrier_id.tipsa_config_id,
                                   login_session)

        warehouse_address = warehouse_partner.street or ''
        if warehouse_partner.street2:
            warehouse_address = u"{0}, {1}".format(warehouse_address,
                                                   warehouse_partner.street2)

        partner_address = self.partner_id.street or ''
        if self.partner_id.street2:
            partner_address = u"{0}, {1}".format(partner_address,
                                                 self.partner_id.street2)
        nom_dest = self.partner_id.name
        if self.partner_id.parent_id:
            nom_dest = u"{} Att: {}".format(
                self.partner_id.parent_id.name, self.partner_id.name)
        send_mail_warning = False
        email_warning = None
        if self.partner_id.email:
            send_mail_warning = True
            email_warning = self.partner_id.email
        try:
            envio_response = tipsa_ws.client.service.GrabaEnvio4(
                strCodAgeCargo=self.carrier_id.tipsa_config_id.agency_code,
                strCodAgeOri=self.carrier_id.tipsa_config_id.agency_code,
                strCodCli=self.carrier_id.tipsa_config_id.customer_code,
                dtFecha=datetime.now().isoformat(),
                strCodTipoServ=self.tipsa_service_type,
                intPaq=self.number_of_packages or 1,
                dPesoOri=self.weight or 1,
                strNomOri=self.company_id.name,
                strDirOri=warehouse_address,
                strPobOri=warehouse_partner.city or '',
                strCPOri=warehouse_partner.zip,
                strTlfOri=warehouse_partner.phone or '',
                strNomDes=nom_dest, strDirDes=partner_address,
                strCPDes=self.partner_id.zip,
                strPobDes=self.partner_id.city or '',
                strTlfDes=self.partner_id.phone or '',
                boDesEmail=send_mail_warning, strDesDirEmails=email_warning)
        except Exception, e:
            raise exceptions.Warning(e.message)

        # TODO: Reembolsos, valores y portes debidos
        # dReembolso=None, dValor=None, dBaseImp=None, dImpuesto=None
        # boPorteDebCli=None, strPersContacto=None

        picking_ref = envio_response.strAlbaranOut
        try:
            shipping_label = tipsa_ws.client.service.ConsEtiquetaEnvio3(
                strAlbaran=picking_ref,
                intIdRepDet=int(tipsa_config.report_format or 90))
        except Exception, e:
            raise exceptions.Warning(e.message)

        label = {
            'file': shipping_label.decode('base64'),
            'file_type': 'pdf',
            'name': picking_ref + '.pdf',
        }

        self.write({'carrier_tracking_ref': picking_ref})

        return [label]

    @api.multi
    def generate_shipping_labels(self, package_ids=None):
        """ Add label generation for Tipsa """
        self.ensure_one()
        if self.carrier_id.type == 'tipsa':
            return self._generate_tipsa_label(package_ids=package_ids)
        return super(StockPicking, self).generate_shipping_labels(
            package_ids=package_ids)
