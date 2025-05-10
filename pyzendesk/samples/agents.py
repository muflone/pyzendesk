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

from pyzendesk import Agents as ZendeskAgents


# Instance zendesk object
zendesk = ZendeskAgents(website=os.environ['ZENDESK_SERVER'])
# Authenticate user
zendesk.authenticate(username=os.environ['ZENDESK_USERNAME'],
                     password=os.environ['ZENDESK_PASSWORD'])

# Get the agents count
count = zendesk.count(include_admins=False)
print('agents count found:', count)
count = zendesk.count(include_admins=True)
print('agents+admins count found:', count)

# Search
agents = zendesk.search(include_admins=False, criteria_list=[])
print('agents details:', len(agents['users']))
agents = zendesk.search(include_admins=True, criteria_list=[])
print('agents+admins details:', len(agents['users']))
# Search all
agents = zendesk.search_all(include_admins=False, criteria_list=[])
print('agents details:', len(agents['users']))
agents = zendesk.search_all(include_admins=True, criteria_list=[])
print('agents+admins details:', len(agents['users']))

# Get agent details
agent = zendesk.get(agent_id=agents['users'][0]['id'])
print(json.dumps(obj=agent,
                 indent=4))

# Get agent related details
agent = zendesk.get_related(agent_id=agents['users'][0]['id'])
print(json.dumps(obj=agent,
                 indent=4))

# Get many agents
agents = zendesk.get_many(agent_ids=[agents['users'][0]['id'],
                                     agents['users'][1]['id'],
                                     agents['users'][2]['id']])
print('agents details:', len(agents['users']))
