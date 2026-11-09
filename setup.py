from setuptools import setup, find_packages

try:
	with open("requirements.txt") as f:
		install_requires = [line.strip() for line in f if line.strip() and not line.startswith("#")]
except Exception:
	install_requires = []

from govt_hr_payroll import __version__ as version

setup(
	name="govt_hr_payroll",
	version=version,
	description="Comprehensive 7th Central Pay Commission (7th CPC) Government HR & Payroll System for Frappe Framework",
	author="NexGen ERP Technologies",
	author_email="support@nexgenerptechnologies.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
