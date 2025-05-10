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


class Agents(Api):
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
        Zendesk requester agent information

        :return: agent information
        """
        return self._users.me()

    def get(self, agent_id: int) -> dict:
        """
        Get a agent's details

        :param agent_id: agent ID to get data from
        :return: dictionary with the agent details
        """
        return self._users.get(user_id=agent_id)

    def get_many(self, agent_ids: list[int]) -> dict:
        """
        Get many agents' details

        :param agent_ids: list of agents ID to get data from
        :return: dictionary with the agent details
        """
        return self._users.get_many(user_ids=agent_ids)

    def get_related(self, agent_id: int) -> dict:
        """
        Get a agent's related details

        :param agent_id: agent ID to get data from
        :return: dictionary with the agent related details
        """
        return self._users.get_related(user_id=agent_id)

    def count(self, include_admins: bool) -> Optional[int]:
        """
        Get the number of agents

        :param include_admins: include administrator as agents
        :return: number of agents found
        """
        criteria_list = ['role:agent']
        if include_admins:
            criteria_list.append('role:admin')
        results = self._users.count(criteria_list=criteria_list)
        return results

    def search(self, include_admins: bool, criteria_list: list) -> dict:
        """
        Get the agents matching the specified criterias

        :param include_admins: include administrator as agents
        :param criteria_list: list of string criterias
        :return: dictionary with agents details found
        """
        criteria_list_copy = criteria_list.copy()
        criteria_list_copy.append('role:agent')
        if include_admins:
            criteria_list_copy.append('role:admin')
        return self._users.search(criteria_list=criteria_list_copy)

    def search_all(self, include_admins: bool, criteria_list: list) -> dict:
        """
        Get the agents matching the specified criterias processing all the
        results by requesting also the next pages.

        :param include_admins: include administrator as agents
        :param criteria_list: list of string criterias
        :return: dictionary with agents details found
        """
        criteria_list_copy = criteria_list.copy()
        criteria_list_copy.append('role:agent')
        if include_admins:
            criteria_list_copy.append('role:admin')
        results = self._users.search_all(criteria_list=criteria_list_copy)
        return results
