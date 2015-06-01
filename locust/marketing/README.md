Marketing Load Testing
======================

Performance tests for the marketing site APIs.

To start the test server on the host "www.example.com":

    >>> locust --host https://www.example.com

Then visit http://localhost:8089/.

### Available Task Sets ###

By default, all tasks are run when the locust test is started. These tasks are as follows:

* __RSSTasks__:         Calls that return RSS XML
* __CourseTasks__:      Calls that return course details
* __InstructorTasks__:  Calls that return instructor details
* __SearchTasks__:      Calls that return search results
* __StaticTasks__:      Calls that return static HTML pages

### Environment Variables ###

The load test supports the following environment variables:

|Variable         | Required? | Description                                          | Default              |
|-----------------|-----------|------------------------------------------------------|----------------------|
|LOCUST_TASK_SET  | No        | Name of the task set to run                          | MarketingTests (All) |
|COURSE_ID        | No        | Key of course in which course details are requested  | edx/DemoX/2014       |
|INSTRUCTOR_ID    | No        | ID of instructor whose courses should be requested   | 4306                 |
