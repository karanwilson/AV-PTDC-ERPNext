from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ptdc_av/__init__.py
from ptdc_av import __version__ as version

setup(
	name="ptdc_av",
	version=version,
	description="Participant Management",
	author="PTDC Labs",
	author_email="karanav@vivaldi.net",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
