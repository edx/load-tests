import mechanize
import uuid
import time
URL_ROOT = 'http://localhost:8000'


class Transaction(object):

    def run(self):
        init_timer = time.time()
        # Make a browser object
        i = uuid.uuid4()
        br = mechanize.Browser()
        br.set_handle_referer(True)    # allow everything to be written to
        br.set_handle_robots(False)   # no robots
        br.set_handle_refresh(True)  # can sometimes hang without this
        br.set_handle_redirect(True)
        br.open(URL_ROOT)

        # Open the page
        br.open('%s/register' % URL_ROOT)

        # Get the csrf token and add it to the header
        csrf = br.request.get_header('Cookie').split("=")[1]
        br.addheaders = [('X-CSRFToken', csrf)]
        # Enter your user name and password and submit.
        # Note this user must already exist in the system.
        br.select_form(nr=1)
        br.form['email'] = str(i) + '@edx.org'
        br.select_form(nr=1)
        br.form['password'] = 'test'
        br.select_form(nr=1)
        br.form['username'] = str(i)
        br.select_form(nr=1)
        br.form['name'] = str(i)
        br.find_control("terms_of_service").items[0].selected = True
        br.find_control("honor_code").items[0].selected = True
        r = br.submit()
        r.read()
        r.geturl()
        # Navigate to the dashboard.
        br.open('%s/dashboard' % URL_ROOT)
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
        br.select_form(nr=0)
        br.form['email'] = str(i) + '@edx.org'
        br.submit()
        br.open('%s/login' % URL_ROOT)
        # Enter your user name and password and submit.
        # Note this user must already exist in the system.
        br.select_form(nr=1)
        br.form['email'] = str(i) + '@edx.org'
        br.select_form(nr=1)
        br.form['password'] = 'test'
        print str(i) + '@edx.org'
        r = br.submit()
        r.read()
        latency = time.time() - init_timer
        self.custom_timers['overall_make_account'] = latency
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
