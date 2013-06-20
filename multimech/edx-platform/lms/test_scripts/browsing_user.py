import mechanize
import sys
import time

URL_ROOT = 'http://localhost:8000'


class Transaction(object):

    def run(self):
        init_timer = time.time()
        URL_ROOT = 'http://localhost:8000'
        #print ("Username, Password, Orgname, Coursename, Runtime")
        username = str(sys.argv[2])
        password = str(sys.argv[3])
        # Make a browser object
        br = mechanize.Browser()
        br.set_handle_referer(True)    # allow everything to be written to
        br.set_handle_robots(False)   # no robots
        br.set_handle_refresh(True)  # can sometimes hang without this
        br.set_handle_redirect(True)
        br.open(URL_ROOT)
        # Open the page
        br.open('%s/login' % URL_ROOT)
        # Get the csrf token and add it to the header
        csrf = br.request.get_header('Cookie').split("=")[1]
        br.addheaders = [('X-CSRFToken', csrf), ('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6')]
        # Validate Email by Resetting Password Request
        br.open('%s/login' % URL_ROOT)
        # Enter your user name and password and submit.
        # Note this user must already exist in the system.
        br.select_form(nr=1)
        br.form['email'] = username
        br.select_form(nr=1)
        br.form['password'] = password
        r = br.submit()
        r.read()
        br.open('%s/dashboard' % URL_ROOT)
        br.open('%s/dashboard' % URL_ROOT)
        br.open('%s/courses/MITx/6.00x/2013_Spring/info' % URL_ROOT)
        br.open('%s/courses/MITx/6.00x/2013_Spring/2013_Spring_Calendar/' % URL_ROOT)
        br.open('%s/courses/MITx/6.00x/2013_Spring/book/0/' % URL_ROOT)
        br.open('%s/courses/MITx/6.00x/2013_Spring/wiki/6.00x/' % URL_ROOT)
        br.open('%s/courses/MITx/6.00x/2013_Spring/courseware' % URL_ROOT)
        latency = time.time() - init_timer
        self.custom_timers['overall_browse'] = latency
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
