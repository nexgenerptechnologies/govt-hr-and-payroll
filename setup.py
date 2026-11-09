from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

from govt_hr_payroll import __version__ as version

setup(
	name="govt_hr_payroll",
	version=version,
	description="Comprehensive 7th Central Pay Commission (7th CPC) Government HR & Payroll System for Frappe Framework v16",
	author="NexGen ERP Technologies",
	author_email="support@nexgenerptechnologies.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
