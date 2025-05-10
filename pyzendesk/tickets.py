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

from typing import Any, Optional

from .api import Api

TICKET_STATUS_NEW = 'new'
TICKET_STATUS_OPEN = 'open'
TICKET_STATUS_PENDING = 'pending'
TICKET_STATUS_HOLD = 'hold'
TICKET_STATUS_SOLVED = 'solved'
TICKET_STATUS_CLOSED = 'closed'


class Tickets(Api):
    def get(self, ticket_id: int) -> dict:
        """
        Get a ticket details

        :param ticket_id: ticket ID to get data from
        :return: dictionary with the ticket details
        """
        return self.request_get(path=f'tickets/{ticket_id}.json')

    def get_comments(self, ticket_id: int) -> dict:
        """
        Get a ticket comments

        :param ticket_id: ticket ID to get data from
        :return: dictionary with the ticket details
        """
        return self.request_get(path=f'tickets/{ticket_id}/comments.json')

    def get_comments_all(self, ticket_id: int) -> dict:
        """
        Get all ticket comments

        :param ticket_id: ticket ID to get data from
        :return: dictionary with the ticket details
        """
        results = {}
        current_page = 0
        next_page_url = 'initial value'
        # Copy the criteria list which will be changed during the loop
        while next_page_url:
            current_page += 1
            search_results = self.request_get(
                path=f'tickets/{ticket_id}/comments.json?page={current_page}')
            if not results:
                # First page of results
                results = search_results
            elif 'error' in search_results:
                # Too many results, search interrupted server side
                results['error'] = search_results['error']
                results['description'] = search_results['description']
            else:
                # Append results
                results['comments'].extend(search_results['comments'])
            if 'error' not in search_results:
                # Continue processing the next page
                next_page_url = search_results['next_page']
            else:
                # Stop search if any error occurred
                next_page_url = None
        return results

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
        Get the tickets matching the specified criterias

        :param criteria_list: list of string criterias
        :return: dictionary with tickets details found
        """
        criteria = ' '.join(criteria_list)
        return self.request_get(
            path=f'search?query=type:ticket {criteria}')

    def search_all(self, criteria_list: list) -> dict:
        """
        Get the tickets matching the specified criterias processing all the
        results by requesting also the next pages

        :param criteria_list: list of string criterias
        :return: dictionary with tickets details found
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
                results['results'].extend(search_results['results'])
            if 'error' not in search_results:
                # Continue processing the next page
                next_page_url = search_results['next_page']
            else:
                # Stop search if any error occurred
                next_page_url = None
            criteria_list.remove(f'&page={current_page}')
        return results

    def search_export(self, criteria_list: list) -> dict:
        """
        Get the tickets matching the specified criterias
        using the search export API

        :param criteria_list: list of string criterias
        :return: dictionary with tickets details found
        """
        criteria = ' '.join(criteria_list)
        return self.request_get(
            path=f'search/export?filter[type]=ticket&query={criteria}')

    def search_export_all(self, criteria_list: list) -> dict:
        """
        Get the tickets matching the specified criterias processing all the
        results by requesting also the next pages using the search export API

        :param criteria_list: list of string criterias
        :return: dictionary with tickets details found
        """
        results = {}
        next_token = 'initial value'
        # Copy the criteria list which will be changed during the loop
        criteria_list = criteria_list.copy()
        while next_token:
            search_results = self.search_export(criteria_list=criteria_list)
            if not results:
                # First page of results
                results = search_results
            elif 'error' in search_results:
                # Too many results, search interrupted server side
                results['error'] = search_results['error']
                results['description'] = search_results['description']
            else:
                # Append results
                results['results'].extend(search_results['results'])
            if f'&page[after]={next_token}' in criteria_list:
                criteria_list.remove(f'&page[after]={next_token}')
            if search_results['meta']['has_more']:
                # Continue processing the next page
                next_token = search_results['meta']['after_cursor']
            else:
                # Stop search if any error occurred
                next_token = None
            criteria_list.append(f'&page[after]={next_token}')
        return results

    def add_comment(self,
                    ticket_id: int,
                    public: bool,
                    text: str,
                    attachments: Optional[list[str]],
                    status: str = None) -> dict:
        """
        Add a public comment to a ticket

        :param ticket_id: ticket ID to update
        :param public: boolean value to make the comment public
        :param text: text to add to the ticket
        :param attachments: list of tokens for attached files
        :param status: new status after the saving the comment
        :return: updated ticket details
        """
        ticket_data = {
            'ticket': {
                'comment': {
                    'public': public,
                    'body': text,
                    'uploads': attachments
                }
            }
        }
        if status is not None:
            ticket_data['ticket']['status'] = status
        return self.request_put(path=f'tickets/{ticket_id}.json',
                                json=ticket_data)

    def add_private_comment(self,
                            ticket_id: int,
                            text: str,
                            attachments: Optional[list[str]],
                            status: str = None) -> dict:
        """
        Add a private comment to a ticket

        :param ticket_id: ticket ID to update
        :param text: text to add to the ticket
        :param attachments: list of tokens for attached files
        :param status: new status after the saving the comment
        :return: updated ticket details
        """
        return self.add_comment(ticket_id=ticket_id,
                                public=False,
                                text=text,
                                attachments=attachments,
                                status=status)

    def add_public_comment(self,
                           ticket_id: int,
                           text: str,
                           attachments: Optional[list[str]],
                           status: str = None) -> dict:
        """
        Add a public comment to a ticket

        :param ticket_id: ticket ID to update
        :param text: text to add to the ticket
        :param attachments: list of tokens for attached files
        :param status: new status after the saving the comment
        :return: updated ticket details
        """
        return self.add_comment(ticket_id=ticket_id,
                                public=True,
                                text=text,
                                attachments=attachments,
                                status=status)

    def set_status(self, ticket_id: int, status: str) -> dict:
        """
        Update ticket status

        :param ticket_id: ticket ID to update
        :param status: new ticket status
        :return: updated ticket details
        """
        return self.request_put(path=f'tickets/{ticket_id}.json',
                                json={
                                    'ticket': {
                                        'status': status
                                    }
                                })

    def get_custom_field(self,
                         ticket: dict,
                         field_id: int,
                         default: Any) -> Optional[Any]:
        """
        Get a custom field value from a Zendesk ticket body

        :param ticket: dictionary with ticket body
        :param field_id: field ID
        :param default: default value for value not found
        :return: custom field value or default value
        """
        return ([field['value']
                 for field in ticket['custom_fields']
                 if field['id'] == field_id] or [default])[0]

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

    def get_requester_email(self, ticket: dict) -> Optional[str]:
        """
        Get the sender address from a ticket dictionary.
        In the case the ticket object doesn't contain a valid address try to
        process a new Zendesk search using a previous ticket followup

        :param ticket: dictionary with ticket body
        :return: requester email address
        """
        try:
            from_data = ticket['via']['source']['from']
            if 'address' in from_data:
                # Requester email address
                result = from_data['address'].lower()
            elif 'ticket_id' in from_data:
                # Missing requester address, check in the referenced ticket
                search_results = self.get(ticket_id=from_data['ticket_id'])
                from_data = search_results['ticket']['via']['source']['from']
                result = from_data['address'].lower()
            else:
                # Missing fields for email address
                raise KeyError
        except KeyError:
            result = None
        return result
