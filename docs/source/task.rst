.. _task-guide:

Tasks
=====

.. contents::
    :depth: 2

A task is mainly a collection of :ref:`Jobs <job-guide>` which run together when *their
time has come*. At its most basic a task consists of a ``taskid``, a
``job``, and a ``run`` :ref:`Calendar <calendar-guide>` instruction. Tasks are configured in
the ``tasks`` object which maps the ``taskid`` to its configuration.

Structure:

.. code-block:: yaml

    tasks:
     <taskid>:
       run: <Calendar instruction>
       job: <job configuration>

A task can be configured using the following keys:
Required:

-  run
-  :ref:`job / jobs <job-guide>`

Optional:

-  enabled
-  :ref:`report <report-guide>`

Report
------

A task can create a report after running all the jobs and send it using
the configured ref:`carrier-guide`.

.. _job-guide:

A closer look at Jobs
=====================

.. _task-examples:

Examples
========

.. code-block:: yaml

    tasks:
      http:
       run: every hour
       report: "Google and Twitter returned {len(google.text) + len(twitter.text)} characters!"
       jobs:
         google:
           slave: dobby.get_url
           url: https://google.com
         twitter:
           slave: dobby.get_url
           url: https://twitter.com

This configuration will create a task ``http`` which will be run every
hour and run the jobs ``google`` and ``twitter`` which will open the
urls for the respective services. After completing the requests the
``http`` task will create a report based on the provided template which
shows the combined length of the sites’ HTML.