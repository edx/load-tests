import mechanize
import sys
import time
from loremipsum import get_paragraphs, get_sentences
from mechanize import HTMLForm

URL_ROOT = 'http://localhost:8000'


class Transaction(object):

    def run(self):
        init_timer = time.time()
        URL_ROOT = 'http://localhost:8000'
        #Username, Password, Orgname, Coursename, Runtime
        username = str(sys.argv[2])
        password = str(sys.argv[3])
        orgname = str(sys.argv[4])
        coursename = str(sys.argv[5])
        runtime = str(sys.argv[6])
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
        # Create the html form
        br.form = HTMLForm(URL_ROOT + '/courses/' + orgname + '/'+coursename + '/' + runtime + '/discussion/' + coursename + '_' + runtime + '_General/threads/create', method='POST', enctype='multipart/form-data')
        # Add a title
        br.form.new_control('text', 'title', {'value': str(get_sentences(1)[0])})
        # Add a body
        br.form.new_control('text', 'body', {'value': str(get_paragraphs(1)[0])})
        # Add submit button
        br.form.new_control('submit', 'Button', {})
        br.form.set_all_readonly(False)
        # Prepare to submit
        br.form.fixup()
        response = br.submit()
        # Submit!
        response.read()
        latency = time.time() - init_timer
        self.custom_timers['overall_topic'] = latency
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
