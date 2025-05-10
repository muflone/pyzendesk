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

from pyzendesk import Admins as ZendeskAdmins


# Instance zendesk object
zendesk = ZendeskAdmins(website=os.environ['ZENDESK_SERVER'])
# Authenticate user
zendesk.authenticate(username=os.environ['ZENDESK_USERNAME'],
                     password=os.environ['ZENDESK_PASSWORD'])

# Get the admins count
count = zendesk.count()
print('admins count found:', count)

# Search
admins = zendesk.search(criteria_list=[])
print('admins details:', len(admins['users']))
# Search all
admins = zendesk.search_all(criteria_list=[])
print('admins details:', len(admins['users']))

# Get admin details
admin = zendesk.get(admin_id=admins['users'][0]['id'])
print(json.dumps(obj=admin,
                 indent=4))

# Get admin related details
admin = zendesk.get_related(admin_id=admins['users'][0]['id'])
print(json.dumps(obj=admin,
                 indent=4))

# Get many admins
admins = zendesk.get_many(admin_ids=[admins['users'][0]['id'],
                                     admins['users'][1]['id'],
                                     admins['users'][2]['id']])
print('admins details:', len(admins['users']))
