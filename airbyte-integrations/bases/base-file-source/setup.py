#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#


from setuptools import find_packages, setup

setup(
    name="base-file-source",
    description="Contains helpers for handling file based sources.",
    author="Airbyte",
    author_email="contact@airbyte.io",
    packages=find_packages(),
    install_requires=[
        "airbyte-cdk~=0.1.28",
        "pyarrow==4.0.1",
        "wcmatch==8.2",
        "dill==0.3.4",
        "pytz",
    ],
)
