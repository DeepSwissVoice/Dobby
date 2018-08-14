.. _calendar-guide:

Calendar
========

.. contents::
    :depth: 2

A surprisingly complex part of Dobby is the scheduler for :ref:`Tasks <task-guide>` which goes
by the *extremely* creative name "Calendar". The Calendar's job is to calculate when the next
execution of a :ref:`Task <task-guide>` takes place.

.. attention::
    The Calendar currently only supports "explicit" values. For instance, you can't say: "run every 15 minutes".
    Okay that was a lie, incidentally, "every 15 minutes" works as it perfectly aligns over the hour mark, but
    "every 14 minutes" won't work the way most people would think.
    The :ref:`instruction <calendar-instruction-guide>` for this would look like this: ``[14M]``.
    What I'm trying to get at is that the Calendar understands this as:
    run every year, every month, every day, every hour, every 14 minutes, at second 0.
    Can you see the problem?
    Probably not, because this text is probably the worst piece of documentation anyone has EVER written...
    Anyway, the problem is that it doesn't care whether 14 minutes have passed, the Calendar only cares whether
    the current minute value is a multiple of 14. Thus "every 14 minutes" basically means: run at 0, 14, 28,
    *pulls out calculator...* 42, 56. Now the next run will be, again, at 0, with the hour value increased by one.

    This explains why 15 works, because 60 is a multiple of 15 and thus it "loops" perfectly.



.. _calendar-instruction-guide:

Instructions
------------
