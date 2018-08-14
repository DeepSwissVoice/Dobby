Errors
======

When things go wrong (and they will, trust me!) Dobby will gladly raise
a lot of errors. In the best case all of these should derive from
`DobbyBaseError` or even better, `DobbyError`. If you're wondering what the
difference between the two is then you're probably not alone.

Contrary to the `DobbyBaseError` which is basically just a normal
Python `Exception`, `DobbyError` stores a lot of metadata and is
*hopefully* (but probably not) the only type of error that should escape
from Dobby!



.. contents:: Contents
    :depth: 2


DobbyBaseError
--------------
.. autoexception:: dobby.DobbyBaseError
    :members:
    :inherited-members:


DobbyError
----------
.. autoexception:: dobby.DobbyError
    :members:
    :inherited-members:


SetupError
----------
.. autoexception:: dobby.SetupError
    :members:
    :inherited-members:


EnvError
--------
.. autoexception:: dobby.EnvError
    :members:
    :inherited-members:


ConversionError
---------------
.. autoexception:: dobby.ConversionError
    :members:
    :inherited-members:
