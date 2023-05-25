.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

pycoords
========

A python package that generates coordinates given addresses.

This project takes a CSV file of addresses as input, then
returns a new CSV file complete with the locations' coordinates. The
user has the option to change the engine used to geocode the addresses.

Dependencies
------------

- python 3.7 and up
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

Make sure you have pip installed ``python -m ensurepip``

Run ``pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pycoords``

Usage instructions
------------------

Run ``pycoords -h`` to see the usage.

.. code:: python

    usage: pycoords [-h] -s source_output [-o output_file] [-v] [-e engine] [-p]
    example: pycoords -s source.csv -o output.csv -v -e google -p

    -s
      # File name of the input CSV
      # Ex: [-s source.csv]
    -o
      # File name of the output
      # If no output file is provided, the output will be saved as output.csv
      # Ex: [-o output.csv]
    -v
      # If provided, debug logging is enabled
    -e
      # If provided, engine used to scrape coordinates is changed
      # Options: google, nominatim
      # Ex: [-e google]
    -p
      # If provided, sets parallel processing to true
      # Note: The nominatim engine does not support parallel processing
      # Ex: [-p]

Usecases
------------------
- Scraping coordinates from a CSV file
  .. code:: python

    pycoords -s source.csv -o output.csv

- Scraping coordinates from a CSV file using the google engine
  .. code:: python

    pycoords -s source.csv -o output.csv -e google

- Scraping coordinates from a CSV file using the google engine with parallel processing
  .. code:: python

    pycoords -s source.csv -o output.csv -e google -p



Making Changes & Contributing
-----------------------------

This project uses ``pre-commit``, please make sure to install it before making any
changes::

    pip install pre-commit
    cd pycoords
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate
