import os
from setuptools import setup, find_packages

PACKAGE_DIR = 'src'

def read(file_name):
	return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
	name = "regexpgen",
	version = '0.0.2',
	author = read("AUTHORS"),
	keywords = "regular expression generator",
	url = "https://github.com/perfidia/regexpgen",
	package_dir = {'': PACKAGE_DIR},
	long_description = read("README.md"),
	packages = find_packages(PACKAGE_DIR, exclude=['ez_setup', 'examples', 'tests']),
	zip_safe = False,
	# https://pypi.python.org/pypi?%3aaction=list_classifiers
	classifiers = [
			'Environment :: Console',
			'Environment :: Web Environment',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: MIT License',
			'Operating System :: Microsoft :: Windows',
			'Operating System :: POSIX',
			'Programming Language :: Python :: 2.7',
	],
)
