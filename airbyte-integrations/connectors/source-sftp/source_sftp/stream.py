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


import stat
import os
from typing import Any, Iterator, Mapping

from airbyte_cdk.logger import AirbyteLogger

from .sftpfile import SftpFile
from .source_files_abstract.stream import IncrementalFileStream
from .utils import create_sftp_client


class IncrementalFileStreamSftp(IncrementalFileStream):
    @property
    def storagefile_class(self) -> type:
        return SftpFile

    @staticmethod
    def _recurse_through(sftp_client, path) -> Iterator[str]:
        for file in sftp_client.listdir_attr(path):
            full_path = os.path.join(path, file.filename)

            if stat.S_ISDIR(file.st_mode):
                yield from IncrementalFileStreamSftp._recurse_through(sftp_client, full_path)
                print(full_path)
            else:
                yield full_path[2:]
                print(full_path)


    @staticmethod
    def filepath_iterator(logger: AirbyteLogger, provider: dict) -> Iterator[str]:
        """
        See _list_bucket() for logic of interacting with S3

        :param logger: instance of AirbyteLogger to use as this is a staticmethod
        :param provider: S3 provider mapping as described in spec.json
        :yield: url filepath to use in S3File()
        """
        sftp_client = create_sftp_client(provider)

        for full_path in IncrementalFileStreamSftp._recurse_through(sftp_client, "."):
            yield full_path
