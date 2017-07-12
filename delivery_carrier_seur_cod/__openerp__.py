# -*- coding: utf-8 -*-

{
    'name': 'Delivery carrier Seur Cash On Delivery',
    'version': '0.0.1',
    'category': 'Delivery',
    'author': 'Digital5, S.L.',
    'depends': [
        'delivery_carrier_seur',
        'delivery_carrier_cod_assured',
        'account_payment',
    ],
    'website': 'http://www.digital5.es',
    'data': [
        'views/seur_config_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
