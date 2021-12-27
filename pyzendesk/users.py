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

from typing import Optional

from .api import Api


class Users(Api):
    def me(self) -> dict:
        """
        Zendesk requester user information

        :return: user information
        """
        return self.request_get(path='users/me.json')

    def get(self, user_id: int) -> dict:
        """
        Get a user's details

        :param user_id: yser ID to get data from
        :return: dictionary with the user details
        """
        return self.request_get(path=f'users/{user_id}.json')

    def count(self, criteria_list: list) -> Optional[int]:
        """
        Get the number of users matching the specified criterias

        :param criteria_list: list of string criterias
        :return: number of users found
        """
        criteria = ' '.join(criteria_list)
        results = self.request_get(
            path=f'users/search?query={criteria}')
        return results.get('count')
