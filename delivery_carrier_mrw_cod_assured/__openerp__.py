##############################################################################
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
{
    'name': 'COD and assured amount in MRW Deliveries WebService',
    'version': '0.0.1',
    'author': "Digital5 S.L.",
    'category': 'Sales Management',
    'depends': [
        'delivery_carrier_mrw',
        'delivery_carrier_cod_assured',
    ],
    'data': [
        'view/mrw_config_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
