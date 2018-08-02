# Tasks

A task is mainly a collection of [jobs](#job) which run together when *their time has come*.
At its most basic a task consists of a `taskid` a `job` and a `run` [Calendar] instruction.
Tasks are configured in the `tasks` object which maps `taskid`s to their configuration.

Structure:
```yaml
 tasks:
  <taskid>:
    run: <Calendar instruction>
    job: <job configuration>
```

## Keys
#### Required
- run
- [job / jobs](#job)

#### Optional
- enabled
- [report](#report)


## Report
A task can create a report after running all the jobs and send it using the configured
[Carriers][Carrier].


# Job

# Examples
```yaml
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
```

This configuration will create a task `http` which will be run every hour and run the
jobs `google` and `twitter` which will open the urls for the respective services.
After completing the requests the `http` task will create a report based on the provided
template which shows the combined length of the sites' HTML.





[Calendar]: calendar "Calendar Documentation"
[Carrier]: notification#carrier "Notification (Carrier) Documentation"