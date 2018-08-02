# Dobby

[![Build Status](https://travis-ci.org/DeepSwissVoice/Dobby.svg?branch=master)](https://travis-ci.org/DeepSwissVoice/Dobby)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7e86942ab7974dcbb95869b01565c27e)](https://www.codacy.com/app/siku2/Dobby?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DeepSwissVoice/Dobby&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/DeepSwissVoice/Dobby/branch/master/graph/badge.svg)](https://codecov.io/gh/DeepSwissVoice/Dobby)


> Dobby is by no means a finished product and the documentation is currently more than
lacking! You should *(probably)* not use it unless you know exactly what you're doing


Have you ever wished to have your personal slave? (I hope not!) <br>
Well, Dobby might be able to scratch that itch. (No it can't *and probably shouldn't*)

Dobby tries to make your life easier when it comes to doing chores around your server like
cleaning up your database or triggering certain events by opening a url.
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
| `dev`     | latest build based on the [development branch]
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
Read the [Documentation]


[Documentation]:        https://deepswissvoice.github.io/Dobby  "The totally finished *cough* documentation"
[development branch]:   /DeepSwissVoice/Dobby/tree/development  "The bleeding edge"

