##
#     Project: PyZendesk
# Description: API for Zendesk
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2021-2025 Fabio Castelli
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

from typing import Optional

from .api import Api
from .users import Users


class Admins(Api):
    def __init__(self, website: str):
        super().__init__(website=website)
        self._users = Users(website=website)

    def authenticate(self, username: str, password: str) -> None:
        """
        Set authentication username and password

        :param username: user name for login
        :param password: user password for login
        :return: None
        """
        super().authenticate(username=username,
                             password=password)
        self._users.authenticate(username=username,
                                 password=password)

    def me(self) -> dict:
        """
        Zendesk requester admin information

        :return: admin information
        """
        return self._users.me()

    def get(self, admin_id: int) -> dict:
        """
        Get a admin's details

        :param admin_id: admin ID to get data from
        :return: dictionary with the admin details
        """
        return self._users.get(user_id=admin_id)

    def get_many(self, admin_ids: list[int]) -> dict:
        """
        Get many admins' details

        :param admin_ids: list of admins ID to get data from
        :return: dictionary with the admin details
        """
        return self._users.get_many(user_ids=admin_ids)

    def get_related(self, admin_id: int) -> dict:
        """
        Get a admin's related details

        :param admin_id: admin ID to get data from
        :return: dictionary with the admin related details
        """
        return self._users.get_related(user_id=admin_id)

    def count(self) -> Optional[int]:
        """
        Get the number of admins

        :return: number of admins found
        """
        results = self._users.count(criteria_list=['role:admin'])
        return results

    def search(self, criteria_list: list) -> dict:
        """
        Get the admins matching the specified criterias

        :param criteria_list: list of string criterias
        :return: dictionary with admins details found
        """
        criteria_list_copy = criteria_list.copy()
        criteria_list_copy.append('role:admin')
        return self._users.search(criteria_list=criteria_list_copy)

    def search_all(self, criteria_list: list) -> dict:
        """
        Get the admins matching the specified criterias processing all the
        results by requesting also the next pages.

        :param criteria_list: list of string criterias
        :return: dictionary with admins details found
        """
        criteria_list_copy = criteria_list.copy()
        criteria_list_copy.append('role:admin')
        results = self._users.search_all(criteria_list=criteria_list_copy)
        return results
