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

from .api import Api                                               # noqa: F401
from .constants import APP_VERSION as __version__                  # noqa: F401
from .tickets import (TICKET_STATUS_NEW,                           # noqa: F401
                      TICKET_STATUS_OPEN,                          # noqa: F401
                      TICKET_STATUS_PENDING,                       # noqa: F401
                      TICKET_STATUS_HOLD,                          # noqa: F401
                      TICKET_STATUS_SOLVED,                        # noqa: F401
                      TICKET_STATUS_CLOSED,                        # noqa: F401
                      Tickets)                                     # noqa: F401
from .attachments import Attachments                               # noqa: F401
from .users import Users                                           # noqa: F401
