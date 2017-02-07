How I ran this test
===================

setup
-----

.. code-block:: sh

        mkdir ~/results/perf-404
        git clone https://github.com/edx/edx-load-tests
        cd edx-load-tests
        git checkout pwnage101/perf-404-working-branch
        virtualenv venv
        source venv/bin/activate
        make lms

        cat <<EOF >settings_files/lms.yml
        ---
        # Course ID that we're running these tests against.  The default
        # targets a course which currently exists on courses-loadtest.edx.org.
        COURSE_ID: course-v1:Fx+LT001+2015_T3
        
        # The name of the course data variable which corresponds to the
        # COURSE_ID specified above.  Must be defined in the lms.course_data
        # module.
        COURSE_DATA: demo_course
        
        # Run the specified TaskSet (must be imported into the lms/locustfile.py
        # file):
        LOCUST_TASK_SET: LmsTest
        
        # Optionally provide a pointer to a large thread which you seeded using the
        # SeedForumsTasks task set:
        #LARGE_TOPIC_ID:
        #LARGE_THREAD_ID:
        
        # Used to determine how 'active' users are in timed and proctored exams.
        # This is the multiplying factor for how often proctoring-specific tasks happen (default is 1):
        PROCTORED_EXAM_MODIFIER: 1
        
        # Used to determine how 'active' users are in timed and proctored exams.
        # This is the multiplying factor for how often CAPA-interactions happen (default is 1):
        MODULE_RENDER_MODIFIER: 1
        
        # Minimum/Maximum waiting time between the execution of locust tasks:
        LOCUST_MIN_WAIT: 300
        LOCUST_MAX_WAIT: 1000
        
        ---
        # secrets below
        
        # Use the following keys to optionally specify basic auth credentials to
        # access the target:
        #BASIC_AUTH_USER:
        #BASIC_AUTH_PASS:
        EOF

test session
------------

.. code-block:: sh

        screen -S test
        
        TEST_DURATION=10  # minutes
        DRIVER_ID=$(wget -q -O - http://169.254.169.254/latest/meta-data/instance-id)

search for peak throughput
--------------------------

.. code-block:: sh

        GUNICORN_WORKER_COUNT= # fill-me
        
        locust --host=https://courses-loadtest.edx.org -f loadtests/lms --no-web -r 20 -c <client count> 
        # repeat previous command until you find the highest throughput
        
        CLIENT_COUNT_PEAK_THROUGHPUT= # fill-me with value of client count that yeilds highest throughput

run experiment for the current gunicorn worker count
----------------------------------------------------

.. code-block:: sh

        CLIENT_COUNTS=$(for i in 0.5 0.6 0.7 0.8 0.9 1.0 1.25 1.50; do python -c "print int(round(${i} * ${CLIENT_COUNT_PEAK_THROUGHPUT}))"; done)
        
        LT_UID= # fill me with a note about this test run
        
        for clients in $CLIENT_COUNTS; do
            log_prefix=${HOME}/results/perf-404/${GUNICORN_WORKER_COUNT}workers-${clients}clients-${DRIVER_ID}-${LT_UID}
            timeout ${TEST_DURATION}m locust --host=https://courses-loadtest.edx.org -f loadtests/lms --no-web -c ${clients} -r 25 --logfile=${log_prefix}.events.log >${log_prefix}.stats.log 2>&1
            echo
            echo "sleeping for 20s..."
            echo
            sleep 20
        done
