#!/usr/bin/env python3
"""
Setup script for NetMaster Pro.

This script handles the installation and distribution of NetMaster Pro.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="netmaster-pro",
    version="1.0.0",
    author="Moanes BBR",
    author_email="moanes.bbr@gmail.com",
    description="Professional Network Management Suite",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/moanesbbr/netmaster-pro",
    project_urls={
        "Bug Tracker": "https://github.com/moanesbbr/netmaster-pro/issues",
        "Documentation": "https://github.com/moanesbbr/netmaster-pro/wiki",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8>=3.8",
            "black>=21.0",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "netmaster-pro=netmaster_pro.ui.main_interface:main",
        ],
    },
    include_package_data=True,
    package_data={
        "netmaster_pro": ["assets/*"],
    },
    keywords="network, management, wifi, qr, monitoring, security",
    zip_safe=False,
) 