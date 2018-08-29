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


class SeurConfig(models.Model):
    _name = 'seur.config'

    @api.model
    def _get_file_type(self):
        return [
            ('pdf', 'PDF'),
            ('txt', 'TXT')
        ]

    name = fields.Char('Name', required=True)
    vat = fields.Char('VAT', required=True)
    integration_code = fields.Char('Integration Code', required=True)
    accounting_code = fields.Char('Accounting Code', required=True)
    franchise_code = fields.Char('Franchise Code', required=True)
    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True)
    file_type = fields.Selection([
        ('pdf', 'PDF'),
        ('txt', 'TXT')
    ], string="File type", required=True)
    seurid = fields.Char(
        'Identifier', required=True, default='Odoo',
        help='Identifier for the sending process, useful to trace the functionality in deployment.'
    )
    timeout = fields.Integer(
        string='Timeout', required=True, default=10,
        help='Time in seconds, to determine whether the webservice is responding or not.'
    )
