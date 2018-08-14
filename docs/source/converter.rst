Converter
=========

Converters handle converting the limited YAML structures into complex
Python types.

Making your own
---------------

A converter can either be a function or a subclass of `Converter`.
If you want to use your converter for a `Slave` you’re either
gonna have to annotate the argument with the converter, or register
it using the `converter` decorator which needs to be given the type
your converter converts to.