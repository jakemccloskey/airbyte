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


from typing import Optional

from pydantic import BaseModel, Field

from .source_files_abstract.source import SourceFilesAbstract
from .source_files_abstract.spec import SourceFilesAbstractSpec
from .stream import IncrementalFileStreamSftp


class SourceSftpSpec(SourceFilesAbstractSpec, BaseModel):
    class Config:
        title = "SFTP Source Spec"

    class SftpProvider(BaseModel):
        class Config:
            title = "SFTP: Secure File Transfer Protocol"

        user: str = Field(
            description="User to login with.",
        )
        password: Optional[str] = Field(
            default=None,
            description="Password to login with.",
            airbyte_secret=True,
        )
        host: str = Field(
            description="Host of the server.",
        )
        port: Optional[str] = Field(
            default="22",
            description="Port of the server.",
        )

    provider: SftpProvider = Field(...)


class SourceSftp(SourceFilesAbstract):
    stream_class = IncrementalFileStreamSftp
    spec_class = SourceSftpSpec
    documentation_url = "https://docs.airbyte.io/integrations/sources/sftp"
