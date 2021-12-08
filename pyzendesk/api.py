##
#     Project: PyZendesk
# Description: API for Zendesk
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import logging
from typing import Optional

import requests
import requests.auth


class Api(object):
    def __init__(self, website: str):
        self.website = website[:-1] if website.endswith('/') else website
        self.username = None
        self.password = None

    def authenticate(self, username: str, password: str) -> None:
        """
        Set authentication username and password

        :param username: user name for login
        :param password: user password for login
        :return: None
        """
        self.username = username
        self.password = password

    def request_raw(self,
                    method: str,
                    path: str,
                    headers: dict,
                    params: Optional[dict],
                    data: Optional[bytes],
                    json: Optional[dict]) -> requests.Response:
        """
        Send a raw REST request to Zendesk

        :param method: REST method to use (get, post, put, delete)
        :param path: API path which will be added to the base API path
        :param headers: dictionary with HTTP headers
        :param params: additional query string to send along with the request
        :param data: additional raw data to send along with the request
        :param json: additional JSON data to send along with the request
        :return: raw requests response
        """
        logging_path = path.replace('\n', '\\n')
        logging.debug(f'Executing {method} request '
                      f'for url {self.website}/api/v2/{logging_path}')
        req = requests.request(method=method,
                               url=f'{self.website}/api/v2/{path}',
                               auth=requests.auth.HTTPBasicAuth(
                                   username=self.username,
                                   password=self.password),
                               headers=headers,
                               params=params,
                               data=data,
                               json=json)
        return req

    def request(self,
                method: str,
                path: str,
                json: Optional[dict]) -> dict:
        """
        Send a JSON REST request to Zendesk

        :param method: REST method to use (get, post, put, delete)
        :param path: API path which will be added to the base API path
        :param json: additional JSON data to send along with the request
        :return: response from JSON data
        """
        req = self.request_raw(method=method,
                               path=path,
                               headers={'Content-Type': 'application/json'},
                               params=None,
                               data=None,
                               json=json)
        return req.json()

    def request_get(self,
                    path: str) -> dict:
        """
        Send a GET REST request to Zendesk

        :param path: API path which will be added to the base API path
        :return: response from JSON data
        """
        return self.request(method='get', path=path, json=None)

    def request_put(self,
                    path: str,
                    json: dict) -> dict:
        """
        Send a PUT REST request to Zendesk

        :param path: API path which will be added to the base API path
        :param json: additional JSON data to send along with the request
        :return: response from JSON data
        """
        return self.request(method='put', path=path, json=json)
