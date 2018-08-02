# Configuration
The configuration file is a YAML file which defines the behaviour of Dobby (obviously).
It consists of the following keys:

1. [env](#env-optional)
2. [ext](#ext-optional)
3. [notifications](#notifications-optional)
4. [tasks](#tasks)

## *env* (optional)
The env key is there to specify various environmental variables.
Usually to define defaults which can be overridden in the "actual" environment variables.
When using `$<name>` in the configuration file Dobby will first try
to find a matching environment key and parse its value and then use the values
specified in the env section.
If there's no value specified in the env key, Dobby raises an error.

## *ext* (optional)
A list of python packages for Dobby to load as an extension. For further information refer to the non-existing [Development Guide]().

## *notifications* (optional)
In here you can tell Dobby how you'd like to get notified about various events such as the completion of a [Task](#tasks).

## tasks
In this section you define the things that Dobby actually does.
The tasks key holds an object where each key is the name of a task and the value is the task configuration.

The configuration consists of the settings for `run`, `report`, `jobs`.
For more information on task configuration [click here](That's what I meant by "Lacking")
