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
import os
import logging
from suds.client import Client
from suds.plugin import MessagePlugin
from suds.sax.element import Element

_logger = logging.getLogger(__name__)


class LogPlugin(MessagePlugin):
    def sending(self, context):
        _logger.info(context.envelope.decode('utf-8', errors='ignore'))

    def received(self, context):
        _logger.info(context.reply.decode('utf-8', errors='ignore'))

    def marshalled(self, context):
        #remove empty tags inside the Body element
        #context.envelope[0] is the SOAP-ENV:Header element
        context.envelope[1].prune()


class TipsaConfig(object):

    def __init__(self, agency_code, customer_code, customer_password,
                 is_test=True):
        self.agency_code = agency_code
        self.customer_code = customer_code
        self.customer_password = customer_password
        self.is_test = is_test


class TipsaBase(object):

    def __init__(self, tipsa_config, wsdl_name):
        wsdl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'wsdl')
        self.tipsa_config = tipsa_config
        if self.tipsa_config.is_test:
            self.wsdl_path = os.path.join(wsdl_path, 'test', wsdl_name)
        else:
            self.wsdl_path = os.path.join(wsdl_path, wsdl_name)
        self.client = Client('file:///%s' % self.wsdl_path.lstrip('/'),
                             cache=None, plugins=[LogPlugin()])


class TipsaLogin(TipsaBase):

    def __init__(self, tipsa_config):
        self.tipsa_config = tipsa_config
        super(TipsaLogin, self).__init__(self.tipsa_config,
                                         'LoginWSService.wsdl')

    def loginCli(self):
        response = self.client.service.LoginCli(
            self.tipsa_config.agency_code, self.tipsa_config.customer_code,
            self.tipsa_config.customer_password)
        return response

    def session_code(self):
        response = self.loginCli()
        return response.strSesion


class TipsaWebService(TipsaBase):

    def __init__(self, tipsa_config, login_session):
        self.tipsa_config = tipsa_config
        super(TipsaWebService, self).__init__(self.tipsa_config,
                                              'WebServService.wsdl')
        session_id = Element('ID').setText(login_session)
        client_header = Element('ROClientIDHeader').insert(session_id)
        self.client.set_options(soapheaders=client_header)
