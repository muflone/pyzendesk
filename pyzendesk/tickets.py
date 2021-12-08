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


class Tickets(Api):
    def get(self, ticket_id: int) -> dict:
        """
        Get a ticket details

        :param ticket_id: ticket ID to get data from
        :return: dictionary with the ticket details
        """
        return self.request_get(path=f'tickets/{ticket_id}.json')

    def count(self, criteria_list: list) -> Optional[int]:
        """
        Get the number of tickets matching the specified criterias

        :param criteria_list: list of string criterias
        :return: number of tickets found
        """
        criteria = ' '.join(criteria_list)
        results = self.request_get(
            path=f'search/count?query=type:ticket {criteria}')
        return results.get('count')

    def search(self, criteria_list: list) -> dict:
        """
        Get the number of tickets matching the specified criterias

        :param criteria_list: list of string criterias
        :return: dictionary with tickets details found
        """
        criteria = ' '.join(criteria_list)
        return self.request_get(
            path=f'search?query=type:ticket {criteria}')

    def add_private_comment(self,
                            ticket_id: int,
                            text: str,
                            attachments: Optional[list[str]]) -> dict:
        """
        Add a private comment to a ticket

        :param ticket_id: ticket ID to update
        :param text: text to add to the ticket
        :param attachments: list of tokens for attached files
        :return: updated ticket details
        """
        return self.request_put(path=f'tickets/{ticket_id}.json',
                                json={
                                    'ticket': {
                                        'comment': {
                                            'public': False,
                                            'body': text,
                                            'uploads': attachments
                                        }
                                    }
                                })

    def add_public_comment(self,
                           ticket_id: int,
                           text: str,
                           attachments: Optional[list[str]]) -> dict:
        """
        Add a public comment to a ticket

        :param ticket_id: ticket ID to update
        :param text: text to add to the ticket
        :param attachments: list of tokens for attached files
        :return: updated ticket details
        """
        return self.request_put(path=f'tickets/{ticket_id}.json',
                                json={
                                    'ticket': {
                                        'comment': {
                                            'public': True,
                                            'body': text,
                                            'uploads': attachments
                                        }
                                    }
                                })

    def update_custom_fields(self, ticket_id: int, fields: dict) -> dict:
        """
        Update custom fields for a ticket

        :param ticket_id: ticket ID to update
        :param fields: dictionary object with key as field ID
        :return: updated ticket details
        """
        data = [{'id': key, 'value': value}
                for key, value in fields.items()]
        return self.request_put(path=f'tickets/{ticket_id}.json',
                                json={
                                    'ticket': {
                                        'custom_fields': data
                                    }
                                })
