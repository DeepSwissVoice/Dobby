# Dobby

[![Build Status](https://travis-ci.org/DeepSwissVoice/Dobby.svg?branch=master)](https://travis-ci.org/DeepSwissVoice/Dobby)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7e86942ab7974dcbb95869b01565c27e)](https://www.codacy.com/app/siku2/Dobby?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DeepSwissVoice/Dobby&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/DeepSwissVoice/Dobby/branch/master/graph/badge.svg)](https://codecov.io/gh/DeepSwissVoice/Dobby)


> Dobby is by no means a finished product and the documentation is currently more than
lacking! You should *(probably)* not use it unless you know exactly what you're doing


Have you ever wished to have your personal slave? (I hope not!) <br>
Well, Dobby might be able to scratch that itch. (No it can't *and probably shouldn't*)

Dobby tries to make your life easier when it comes to doing chores around your server like
cleaning up your database or triggering certain events by opening an url.
Dobby can do pretty much anything (as long as you code it yourself because I'm too lazy to
code boiler-plate slaves that SwissVoice doesn't need) you need done every now and then.

All you have to do is write a configuration file, start Dobby and you're good to go!
(If you ignore all the bugs)


## Installation
The recommended way of running Dobby is using the Docker image `siku2/Dobby`.
The following tags are available:

|    Tag    |        Description        |
| --------- | ------------------------- |
| `latest`  | stable build
| `dev`     | latest build based on the [development branch](/DeepSwissVoice/Dobby/tree/development)
| `v-x`     | specify major release
| `v-x.y`   | specify the minor release too
| `v-x.y.z` | when you need to go all out...

Mount your config file to `/dobby/config.yml` and you're ready to go!


## Manual Usage
Start Dobby by running `dobby run <config file>`
where `<config file>` points to the location of your [config file](#configuration)...

If you for some reason desire to do a test run (runs through all tasks without waiting)
you can run `dobby test <config file>`

## Configuration
The configuration file is a YAML file which defines the behaviour of Dobby (obviously).
It consists of the following keys:

1. [env](#env-optional)
2. [ext](#ext-optional)
3. [notifications](#notifications-optional)
4. [tasks](#tasks)

### *env* (optional)
The env key is there to specify various environmental variables.
Usually to define defaults which can be overridden in the "actual" environment variables.
When using `$<name>` in the configuration file Dobby will first try
to find a matching environment key and parse its value and then use the values
specified in the env section.
If there's no value specified in the env key, Dobby raises an error.

### *ext* (optional)
A list of python packages for Dobby to load as an extension. For further information refer to the non-existing [Development Guide]().

### *notifications* (optional)
In here you can tell Dobby how you'd like to get notified about various events such as the completion of a [Task](#tasks).

### tasks
In this section you define the things that Dobby actually does.
The tasks key holds an object where each key is the name of a task and the value is the task configuration.

The configuration consists of the settings for `run`, `report`, `jobs`.
For more information on task configuration [click here](That's what I meant by "Lacking")

