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

import os

from pyzendesk import Attachments as ZendeskAttachments
from pyzendesk import Tickets as ZendeskTickets


# Instance zendesk object
zendesk = ZendeskTickets(website=os.environ['ZENDESK_SERVER'])
# Authenticate user
zendesk.authenticate(username=os.environ['ZENDESK_USERNAME'],
                     password=os.environ['ZENDESK_PASSWORD'])

# Get the tickets count from 2021-01-01 to 2021-01-31
count = zendesk.count(criteria_list=['created>=2021-01-01',
                                     'created<=2021-01-31'])
print('tickets count found:', count)

# Get the tickets details from 2021-01-01 to 2021-01-31
tickets = zendesk.search(criteria_list=['created>=2021-01-01',
                                        'created<=2021-01-31'])
print('tickets details:', len(tickets['results']))

# Get details for the first ticket using its ID
ticket_id = tickets['results'][0]['id']
ticket = zendesk.get(ticket_id=ticket_id)
print('ticket details:', ticket)

# Set ticket custom fields
ticket = zendesk.update_custom_fields(ticket_id=ticket_id,
                                      fields={1900004825713: 'something',
                                              1900005530233: 'fr'})
print('ticket details:', ticket)

# Add private comment to a ticket
ticket = zendesk.add_private_comment(ticket_id=ticket_id,
                                     text='This is **private** comment',
                                     attachments=None)
print('ticket details:', ticket)

# Add public comment to a ticket
ticket = zendesk.add_public_comment(ticket_id=ticket_id,
                                    text='This is **public** comment',
                                    attachments=None)
print('ticket details:', ticket)


# Instance attachments object
attachments = ZendeskAttachments(website=os.environ['ZENDESK_SERVER'])
attachments.authenticate(username=os.environ['ZENDESK_USERNAME'],
                         password=os.environ['ZENDESK_PASSWORD'])
with open(__file__, 'rb') as file:
    attachment_content = file.read()

# Add private comment to a ticket with attachments
attachment = attachments.upload(content_type='text/plain',
                                filename='test.py',
                                data=attachment_content)
attachment_token = attachment['upload']['token']
ticket = zendesk.add_private_comment(ticket_id=ticket_id,
                                     text='With attachment',
                                     attachments=[attachment_token])
print('tickets details:', ticket)

# Add public comment to a ticket with attachments
attachment = attachments.upload(content_type='text/plain',
                                filename='test.py',
                                data=attachment_content)
attachment_token = attachment['upload']['token']
ticket = zendesk.add_public_comment(ticket_id=ticket_id,
                                    text='With attachment',
                                    attachments=[attachment_token])
print('ticket details:', ticket)
