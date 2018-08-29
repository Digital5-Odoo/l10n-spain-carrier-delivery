##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 FactorLibre (http://www.factorlibre.com)
#                  Ismael Calvo <ismael.calvo@factorlibre.com>
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
from odoo import api, fields, models, tools, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from urllib.error import HTTPError


import logging
_logger = logging.getLogger(__name__)
try:
    from seur.picking import Picking
except ImportError:
    _logger.debug('Can not `from seur.picking import Picking`.')


class ManifestWizard(models.TransientModel):
    _inherit = 'manifest.wizard'

    @api.multi
    def get_manifest_file(self):
        self.ensure_one()
        if self.carrier_type == 'seur':
            config = self.carrier_id.seur_config_id

            seur_picking = Picking(
                config.username,
                config.password,
                config.vat,
                config.franchise_code,
                config.seurid or 'Odoo',  # seurid
                config.integration_code,
                config.accounting_code
            )
            try:
                connect = seur_picking.test_connection()
                if connect != 'Connection successfully':
                    raise exceptions.Warning(
                        _('Error conecting with SEUR:\n%s' % connect))
            except HTTPError as e:
                raise exceptions.Warning(
                    _('Error conecting with SEUR try later:\n%s' % e))

            data = {'date': 'T'.join(self.from_date.split(' ')) + 'Z'}

            manifiesto = False
            try:
                manifiesto = seur_picking.manifiesto(data)
            except HTTPError as e:
                raise exceptions.Warning(
                    _('Error generating SEUR manifest:\n%s' % e))

            self.write({
                'state': 'file',
                'file_out': manifiesto,
                'filename': ('manifiesto_%s.pdf') % (self.from_date)
            })

            return {
                'name': 'Seur Manifest',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'manifest.wizard',
                'view_id': False,
                'target': 'new',
                'type': 'ir.actions.act_window',
                'domain': [('id', '=', self.id)],
                'context': self.env.context,
                'nodestroy': True,
                'res_id': self.id,
            }
        else:
            return super(ManifestWizard, self).get_manifest_file()
