.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

pycoords
========

A python package that generates coordinates given addresses.

This project takes a CSV file that stores addresses as input, then 
returns a new CSV file complete with the locations' coordinates. The
user has the option to change the engine used by the program to scrape
the coordinates.

Dependencies
------------

- python 3.10+
- tox
- pydantic
- geopy
- loguru
- requests
- python-dotenv
- requests-ip-rotator
- alive_progress

Installation instructions
-------------------------

Make sure that all dependencies are satisfied. 

Run ``pip install pycoords``

Usage instructions
------------------

Run ``pycoords -h`` to see the usage.

.. code:: python

    usage: pycoords [-h] -s source_output [-o output_file] [-v] [-e engine] [-p]

    -s File name of the input CSV | [-s file_name.csv]
    -o File name of the output | [-o output_file.csv]
    -v If provided, debug logging is enabled
    -e If provided, engine used to scrape coordinates is changed | [-e nominatim] or [-e google]
    -p If provided, sets parallel processing to true

Making Changes & Contributing
-----------------------------

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    pip install pre-commit
    cd pycoords
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate