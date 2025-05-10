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

import json
import os

from pyzendesk import constants
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

# Get all the users details from 2021-01-01 to 2021-01-31
users = zendesk.search_all(criteria_list=['created>=2021-01-01',
                                          'created<=2021-01-31'])
print('users details:', len(users['users']))

# Get user details
user = zendesk.get(user_id=users['users'][0]['id'])
print(json.dumps(obj=user,
                 indent=4))

# Get user related details
user = zendesk.get_related(user_id=users['users'][0]['id'])
print(json.dumps(obj=user,
                 indent=4))

# Autocomplete users
users = zendesk.autocomplete(name='Fabio C')
print('users details:', len(users['users']))

# Autocomplete all users
users = zendesk.autocomplete_all(name='Fabio C')
print('users details:', len(users['users']))

# Get many users
users = zendesk.get_many(user_ids=[users['users'][0]['id'],
                                   users['users'][1]['id'],
                                   users['users'][2]['id']])
print('users details:', len(users['users']))

# Create new user
user = zendesk.create(user={'email': constants.APP_AUTHOR_EMAIL,
                            'name': constants.APP_AUTHOR,
                            'role': 'end-user',
                            'verified': True})
print(json.dumps(obj=user,
                 indent=4))

# Merge two users
user2 = zendesk.create(user={'email': f'{constants.APP_AUTHOR_EMAIL}.copy',
                             'name': constants.APP_AUTHOR,
                             'role': 'end-user',
                             'verified': True})
user = zendesk.merge(user_id=user2['user']['id'],
                     user_id_final=user['user']['id'])

# Create or update user
user = zendesk.create_or_update(user={'email': constants.APP_AUTHOR_EMAIL,
                                      'name': constants.APP_AUTHOR,
                                      'role': 'end-user',
                                      'verified': True,
                                      'phone': '+39987654321'})

# Update user
user = zendesk.update(user_id=user['user']['id'],
                      user={'phone': '+39123456789'})

# Delete the new user
user = zendesk.delete(user_id=user['user']['id'])
print(json.dumps(obj=user,
                 indent=4))

# List deleted users
users = zendesk.list_deleted()
print('users details:', len(users['deleted_users']))

# Get the newly deleted user
user = zendesk.get_deleted(user_id=user['user']['id'])
print(json.dumps(obj=user,
                 indent=4))

# Purge the new user
user = zendesk.purge(user_id=user['deleted_user']['id'])
print(json.dumps(obj=user,
                 indent=4))

# Create two new users
# status = zendesk.create_many(users=[
#     {'email': constants.APP_AUTHOR_EMAIL,
#      'name': constants.APP_AUTHOR,
#      'role': 'end-user',
#      'verified': True},
#     {'email': f'{constants.APP_AUTHOR_EMAIL}.copy',
#      'name': constants.APP_AUTHOR,
#      'role': 'end-user',
#      'verified': True},
#     ])
# print(json.dumps(obj=status,
#                  indent=4))

# Create two new users
# status = zendesk.create_or_update_many(users=[
#     {'email': constants.APP_AUTHOR_EMAIL,
#      'name': constants.APP_AUTHOR,
#      'role': 'end-user',
#      'verified': True},
#     {'email': f'{constants.APP_AUTHOR_EMAIL}.copy',
#      'name': constants.APP_AUTHOR,
#      'role': 'end-user',
#      'verified': True},
#     ])
# print(json.dumps(obj=status,
#                  indent=4))
