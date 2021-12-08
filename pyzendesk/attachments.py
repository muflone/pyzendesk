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

from .api import Api


class Attachments(Api):
    def upload(self, content_type: str, filename: str, data: bytes) -> dict:
        """
        Upload an attachment using the specified content type

        :param content_type: HTTP content_type
        :param filename: filename for the uploaded file
        :param data: raw data to upload
        :return: upload JSON results
        """
        return self.request_raw(method='post',
                                path='uploads.json',
                                headers={'Content-Type': content_type},
                                params={'filename': filename},
                                data=data,
                                json=None).json()
