#
# MIT License
#
# Copyright (c) 2020 Airbyte
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


from contextlib import contextmanager
from datetime import datetime, timezone
from typing import BinaryIO, Iterator, TextIO, Union

import smart_open

from .source_files_abstract.storagefile import StorageFile
from .utils import create_sftp_client


class SftpFile(StorageFile):
    def __init__(self, url: str, provider: dict):
        super().__init__(url, provider)
        self._setup_client()

    def _setup_client(self):
        """
        Making a new Session at file level rather than stream level as boto3 sessions are NOT thread-safe.
        Currently grabbing last_modified across multiple files asynchronously and may implement more multi-threading in future.
        See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html (anchor link broken, scroll to bottom)
        """
        self._sftp_client = create_sftp_client(self._provider)

    @property
    def last_modified(self) -> datetime:
        """
        Using decorator set up boto3 session & s3 resource.
        Note: slight nuance for grabbing this when we have no credentials.

        :return: last_modified property of the blob/file
        """
        obj = self._sftp_client.stat(self.url)

        return datetime.fromtimestamp(int(obj.st_mtime), timezone.utc)

    @contextmanager
    def open(self, binary: bool) -> Iterator[Union[TextIO, BinaryIO]]:
        """
        Utilising smart_open to handle this (https://github.com/RaRe-Technologies/smart_open)

        :param binary: whether or not to open file as binary
        :return: file-like object
        """
        mode = "rb" if binary else "r"
        # params = {"connect_kwargs": {"sock": self._sftp_client.get_channel().get_transport().open_sftp_client()}}
        params = {"connect_kwargs": {}}

        user = self._provider.get("user")
        password = self._provider.get("password")
        host = self._provider.get("host")
        port = self._provider.get("port")

        result = smart_open.open(f"sftp://{user}:{password}@{host}:{port}/{self.url}", transport_params=params, mode=mode)

        # see https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager for why we do this
        try:
            yield result
        finally:
            result.close()
