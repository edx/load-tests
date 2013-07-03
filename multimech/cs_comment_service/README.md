
Naming convention for files
===========================
* Test Scripts:
** cs_foo: e.g. cs_get_search_threads. These scripts exercise a specific API call only.
** user_transaction: e.g. create_thread. These scripts exercise the series of transactions that are triggered by a particular user interaction from the lms.
* Other files in the test_scripts directory:
** helpers.py: helper methods used by all script files
** params.cfg: configuration file that is read by the __init__ of each script in order to populate defaults
** seed_data.py: Can be used to populate users, threads, and comments in the local dev environment. This was to bootstrap the search test. Execute with `python seed_data.py`
* Config.cfg: This is the configuration file that controls multi-mechanize test execution including number of threads and ramp up time for transactions

Data used by transactions
=========================
* Users: most of the scripts use a random user whose id is between 1 and max_user_id as defined in test_scripts/params.cfg.

* Threads and Comments:
Data for threads and comments should be stored in a data file that is at the same level as the test_scripts file. This data must be populated into the db somehow (either use a copy of prod, or seed with the rake task or by test_scripts/seed_data.py) and extracted into flat files prior to running the scripts with multi-mechanize.

To create the data files, add the following to the Rakefile:
```ruby
  task :print_threads => :environment do
    CommentThread.each {|thread| puts thread.id}
  end

  task :print_comments => :environment do
    Comment.each {|comment| puts comment.id}
  end
```
Run from the cs_comments_service rvm and direct the output to the proper file (afterwards move it from tmp to ../data):
```bash
bundle exec rake db:print_comments > /tmp/comments.txt
bundle exec rake db:print_threads > /tmp/threads.txt
```
