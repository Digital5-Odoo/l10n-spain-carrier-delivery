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


class MrwConfig(models.Model):
    _name = 'mrw.config'
    _description = 'MRW Config'

    name = fields.Char('Name', required=True)
    is_test = fields.Boolean('Is a test?')
    franchise_code = fields.Char('Franchise Code', required=True)
    subscriber_code = fields.Char('Subscriber Code', required=True)
    department_code = fields.Char('Department Code')
    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True)
    sat_delivery = fields.Boolean(string='Delivery on Saturday')
