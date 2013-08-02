RegExpGen
=========

Description
-----------

RegExpGen allows to generate regular expressions on the basis of format
supported by well known ``printf`` function.

Documentation can be found on `readthedocs <https://regexpgen.readthedocs.org/en/latest/>`_..

Getting started
---------------

    >>> import regexpgen
    >>> regexp = regexpgen.integer(r"%d")
    >>> print regexp
    ^-?[0-9]+$

Authors
-------

See AUTHORS file.

License
-------

RegExpGen is released under the MIT license. See LICENSE file.
