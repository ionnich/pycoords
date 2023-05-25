.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target:

.. image:: https://img.shields.io/badge/code%20style-flake8-black
    :target:

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
      # If provided, engine used to geocode coordinates is changed
      # Options: google, nominatim
      # Ex: [-e google]
    -p
      # If provided, sets parallel processing to true
      # Note: The nominatim engine does not support parallel processing
      # Ex: [-p]

Usecases
========

A few examples of how to use the package.

.. code:: python

    # Geocoding coordinates from a CSV file (default behavior)
    pycoords -s source.csv -o output.csv

.. code:: python

    # Geocoding coordinates from a CSV file with debug logging
    pycoords -s source.csv -o output.csv -v

.. code:: python

    # Using parallel processing with google maps api
    pycoords -s source.csv -o output.csv -e google -p


Cyclomatic Complexity testing with Radon
========================================

.. code:: python

     ➜ radon cc src/pycoords/ -a
    src/pycoords/address_mapper.py
        F 4:0 dict_to_address - A
    src/pycoords/address.py
        C 4:0 Address - A
        M 20:4 Address.none_to_empty - A
        M 47:4 Address.__str__ - A
    src/pycoords/initialize.py
        F 4:0 parse_args - A
    src/pycoords/csv_reader.py
        F 5:0 read_csv - A
    src/pycoords/csv_writer.py
        F 5:0 write_csv - A
    src/pycoords/backends.py
        F 11:0 geocode_with_nominatim - B
        F 50:0 geocode_with_google_maps - A
        F 95:0 geocode_with_ip_rotation - A
    src/pycoords/geocoder.py
        F 162:0 geocode_addresses - B
        F 116:0 generate_coordinates - A
        F 79:0 remove_geocoded - A
        F 33:0 parallel_processing - A
        F 12:0 get_api_key - A
        F 63:0 single_threaded_processing - A
        F 101:0 get_position_in - A
    src/pycoords/pycoords.py
        F 54:0 main - B
        F 40:0 setup_logging - A
        F 21:0 is_csv - A
        F 34:0 file_exists - A
        F 112:0 run - A

    22 blocks (classes, functions, methods) analyzed.
    Average complexity: A (3.272727272727273)


Making Changes & Contributing
-----------------------------

This project uses ``pre-commit``, please make sure to install it before making any
changes::

    pip install pre-commit
    cd pycoords
    pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate
