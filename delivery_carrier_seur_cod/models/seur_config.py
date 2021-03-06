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

from openerp import models, fields, api


class SeurConfig(models.Model):
    _inherit = 'seur.config'
    
    cod_type = fields.Selection([
        ('F', 'Commission on origin'),
        ('D', 'Commission on destination'),
    ], string='COD type', track_visibility='onchange',
        help="Commission on origin: The sender pays refund costs, "
             "Commission on destination: The addressee pays the refund costs")
    cod_payment_mode_id = fields.Many2one('payment.mode', string='Payment for COD')
    perc_commission = fields.Float(string='COD commission (%)')
