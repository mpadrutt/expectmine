Cli IO
======

Basic Cli based input class. It uses `InquirerPy <https://inquirerpy.readthedocs.io/en/latest>`_
under the hood to query the user for information. It should be used if you want
to provide the user with an interactive experience. The CliIo step does not need
to know all query keys in advance.

Usage
_____
To create a new CliIo instance, simply import the Class and create an instance.
Same holds true for the CliIoAdapter.

.. code-block:: python

   from src.io.io.cli_io import CliIo
   from src.io.adapters.cli_io_adapter import CliIoAdapter

   io_object = CliIo()
   adapter = CliIoAdapter()


Further Info
___________
.. toctree::
   :maxdepth: 3

   cli_io
   cli_io_adapter
