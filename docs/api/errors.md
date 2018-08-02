# Errors
When things go wrong (and they will, trust me!) Dobby will gladly raise a lot of errors.
In the best case all of these should derive from [`DobbyBaseError`] or even better,
[`DobbyError`].
If you're wondering what the difference between the two is then you're probably not alone.

Contrary to the [`DobbyBaseError`] which is basically just a normal Python [Exception],
[`DobbyError`] stores a lot of metadata and is *hopefully* (but probably not) the only type
of error that should escape from Dobby!



## DobbyBaseError
Origin: `dobby.errors.DobbyBaseError`<br>
Alias: `dobby.DobbyBaseError`

#### Bases
[`DobbyBaseError`] > [Exception]

#### Description
As mentioned above, this class is just a normal [Exception] with a different name.



## DobbyError
Origin: `dobby.errors.DobbyError`<br>
Alias: `dobby.DobbyError`

#### Bases
[`DobbyError`] > [`DobbyBaseError`] > [Exception]

#### Description
As mentioned above, this class is just a normal [Exception] with a different name.

#### Methods

**\_\_init\_\_(msg: str, \*\*kwargs)**
    The constructor requires a message to be passed and everything else is optional.
    The keyword arguments consist of `hint` (`str`) and `ctx` ([`Context`]) which should be
    pretty self-explanatory (I hope).

#### Attributes
**msg: `str`**
    A nicely formatted string containing all the information associated with the error

**hint: `Optional[str]`**
    The hint which may have been provided when creating the error

**message: `Optional[str]`**
    A property for subclasses to override.
    For [`DobbyErrors`][`DobbyError`] this will always be `None`



## SetupError
Origin: `dobby.errors.SetupError`<br>
Alias: `dobby.SetupError`

#### Bases
[`SetupError`] > [`DobbyError`] > [`DobbyBaseError`] > [Exception]

#### Description
A subclass of [`DobbyError`] which really doesn't add anything to the base class **but**
it is (or at least should be) the base class for all errors that happen during the setup of
Dobby (that's basically everything before going to sleep to wait for the first task).



## EnvError
Origin: `dobby.errors.EnvError`<br>
Alias: `dobby.EnvError`

#### Bases
[`EnvError`] > [`SetupError`] > [`DobbyError`] > [`DobbyBaseError`] > [Exception]

#### Description
Finally we get to the first *real* error which is raised when trying to access a key from
the `env` that isn't defined in the environment variables or the [`env` config key].



## ConversionError
Origin: `dobby.errors.ConversionError`<br>
Alias: `dobby.ConversionError`

#### Bases
[`ConversionError`] > [`SetupError`] > [`DobbyError`] > [`DobbyBaseError`] > [Exception]

#### Description
Raised when the conversion of a config value to the designated slave argument type fails.

#### Attributes
**message: `str`**
    A string which provides information on which [`Converter`] was used, what was to be
    converted and for which slave argument.



[`DobbyBaseError`]:     #dobbybaseerror
[`DobbyError`]:         #dobbyerror
[`SetupError`]:         #setuperror
[`EnvError`]:           #enverror
[`ConversionError`]:    #conversionerror

[`Context`]:            context.md  "Context Documentation"

[Exception]:            https://docs.python.org/3/tutorial/errors.html  "Python Exception Documentation"