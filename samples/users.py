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

import json
import os

from pyzendesk import Users as ZendeskUsers


# Instance zendesk object
zendesk = ZendeskUsers(website=os.environ['ZENDESK_SERVER'])
# Authenticate user
zendesk.authenticate(username=os.environ['ZENDESK_USERNAME'],
                     password=os.environ['ZENDESK_PASSWORD'])

# Get the users count from 2021-01-01 to 2021-01-31
count = zendesk.count(criteria_list=['created>=2021-01-01',
                                     'created<=2021-01-31'])
print('users count found:', count)

# Get the users details from 2021-01-01 to 2021-01-31
users = zendesk.search(criteria_list=['created>=2021-01-01',
                                      'created<=2021-01-31'])
print('users details:', len(users['users']))

# Get all the tickets details from 2021-01-01 to 2021-01-31
users = zendesk.search_all(criteria_list=['created>=2021-01-01',
                                          'created<=2021-01-31'])
print('users details:', len(users['users']))

# Get user details
user = zendesk.get(user_id=users['users'][0]['id'])
print(json.dumps(obj=user,
                 indent=4))
