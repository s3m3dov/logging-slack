# -*- coding: utf-8 -*-
import os

from setuptools import setup

VERSION = "0.1.0"
PACKAGE_NAME = "logging_slacker"


def readme(*paths):
    with open(os.path.join(*paths), "r") as f:
        return f.read()


def requirements(*paths):
    with open(os.path.join(*paths), "r") as f:
        return list(
            line.strip() for line in f.readlines() if line.strip() != ""
        )


setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=VERSION,
    description="Posts log events to Slack via API",
    long_description=readme("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Communications :: Chat",
        "Topic :: Office/Business :: Groupware",
    ],
    url=f"https://github.com/s3m3dov/{PACKAGE_NAME}",
    download_url=f"https://github.com/s3m3dov/{PACKAGE_NAME}/archive/{VERSION}.tar.gz",
    author="Hikmat Samadov",
    author_email="hikmat@cublya.com",
    keywords=["slack", "logging"],
    install_requires=requirements("requirements.txt"),
    include_package_data=True,
    zip_safe=False,
)
