RegExpGen
=========

Description
-----------

TODO

Installation
------------

### Simple

    python setup.py install

### Using eggs

    python setup.py bdist_egg
    cd dist
    easy_install <package_name>

Getting started
---------------

	>>> import regexpgen
	>>> pattern = r"%d"
	>>> regexp = regexpgen.integer(pattern)
	>>> print regexp
	^-?[0-9]+$

Authors
-------

See AUTHORS file.

License
-------

RegExpGen is released under the MIT license. See LICENSE file.
