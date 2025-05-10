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


class Users(Api):
    def me(self) -> dict:
        """
        Zendesk requester user information

        :return: user information
        """
        return self.request_get(path='users/me.json')

    def autocomplete(self, name: str) -> dict:
        """
        Get the users with matching name

        :param name: user name to match
        :return: dictionary with the user details
        """
        return self.request_get(path=f'users/autocomplete?name={name}')

    def autocomplete_all(self, name: str) -> dict:
        """
        Get all the users with matching name

        :param name: user name to match
        :return: dictionary with the user details
        """
        results = {}
        current_page = 0
        next_page_url = 'initial value'
        while next_page_url:
            current_page += 1
            search_results = self.autocomplete(name=f'{name}'
                                                    f'&page={current_page}')
            if not results:
                # First page of results
                results = search_results
            elif 'error' in search_results:
                # Too many results, search interrupted server side
                results['error'] = search_results['error']
                results['description'] = search_results['description']
            else:
                # Append results
                results['users'].extend(search_results['users'])
            if 'error' not in search_results:
                # Continue processing the next page
                next_page_url = search_results['next_page']
            else:
                # Stop search if any error occurred
                next_page_url = None
        return results

    def get(self, user_id: int) -> dict:
        """
        Get a user's details

        :param user_id: user ID to get data from
        :return: dictionary with the user details
        """
        return self.request_get(path=f'users/{user_id}')

    def get_many(self, user_ids: list[int]) -> dict:
        """
        Get many users' details

        :param user_ids: list of users ID to get data from
        :return: dictionary with the user details
        """
        ids = ','.join(map(str, user_ids))
        return self.request_get(path=f'users/show_many?ids={ids}')

    def get_related(self, user_id: int) -> dict:
        """
        Get a user's related details

        :param user_id: user ID to get data from
        :return: dictionary with the user related details
        """
        return self.request_get(path=f'users/{user_id}/related')

    def merge(self, user_id: int, user_id_final: int) -> dict:
        """
        Merge a user into another

        :param user_id: user ID to get data from
        :param user_id_final: final user ID to merge data to
        :return: dictionary with the user related details
        """
        return self.request_put(path=f'users/{user_id}/merge',
                                json={'user': {
                                    'id': user_id_final}})

    def get_deleted(self, user_id: int) -> dict:
        """
        Get a deleted user's details

        :param user_id: user ID to get data from
        :return: dictionary with the user related details
        """
        return self.request_get(path=f'deleted_users/{user_id}')

    def list_deleted(self) -> dict:
        """
        Get the deleted users list

        :return: dictionary with the deleted users details
        """
        return self.request_get(path='deleted_users')

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

    def search(self, criteria_list: list) -> dict:
        """
        Get the users matching the specified criterias

        :param criteria_list: list of string criterias
        :return: dictionary with users details found
        """
        criteria = ' '.join(criteria_list)
        return self.request_get(
            path=f'users/search?query={criteria}')

    def search_all(self, criteria_list: list) -> dict:
        """
        Get the users matching the specified criterias processing all the
        results by requesting also the next pages.

        :param criteria_list: list of string criterias
        :return: dictionary with users details found
        """
        results = {}
        current_page = 0
        next_page_url = 'initial value'
        # Copy the criteria list which will be changed during the loop
        criteria_list = criteria_list.copy()
        while next_page_url:
            current_page += 1
            criteria_list.append(f'&page={current_page}')
            search_results = self.search(criteria_list=criteria_list)
            if not results:
                # First page of results
                results = search_results
            elif 'error' in search_results:
                # Too many results, search interrupted server side
                results['error'] = search_results['error']
                results['description'] = search_results['description']
            else:
                # Append results
                results['users'].extend(search_results['users'])
            if 'error' not in search_results:
                # Continue processing the next page
                next_page_url = search_results['next_page']
            else:
                # Stop search if any error occurred
                next_page_url = None
            criteria_list.remove(f'&page={current_page}')
        return results

    def create(self, user: dict) -> dict:
        """
        Create a new user

        :param user: user details dictionary
        :return: updated user details
        """
        return self.request_post(path='users',
                                 json={'user': user})

    def create_many(self, users: list[dict]) -> dict:
        """
        Create many new users

        :param user: user details dictionary
        :return: updated users details
        """
        return self.request_post(path='users/create_many',
                                 json={'users': users})

    def create_or_update(self, user: dict) -> dict:
        """
        Create a new user or update an existing user

        :param user: user details dictionary
        :return: updated user details
        """
        return self.request_post(path='users/create_or_update',
                                 json={'user': user})

    def create_or_update_many(self, users: list[dict]) -> dict:
        """
        Create many new users or update many existing users

        :param users: user details list of dictionaries
        :return: updated user details
        """
        return self.request_post(path='users/create_or_update_many',
                                 json={'users': users})

    def delete(self, user_id: int) -> dict:
        """
        Delete a user

        :param user_id: user ID to delete
        :return: deleted user details
        """
        return self.request_delete(path=f'users/{user_id}')

    def purge(self, user_id: int) -> dict:
        """
        Permanently delete a deleted user

        :param user_id: user ID to delete permanently
        :return: deleted user details
        """
        return self.request_delete(path=f'deleted_users/{user_id}')

    def update(self, user_id: int, user: dict) -> dict:
        """
        Updated an existing user

        :param user_id: user ID to update
        :param user: user details dictionary
        :return: updated user details
        """
        return self.request_put(path=f'users/{user_id}',
                                json={'user': user})
