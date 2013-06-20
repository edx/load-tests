import time
import re
from loremipsum import get_paragraphs
from mechanize import HTMLForm
import sys
import mechanize
from random import choice

URL_ROOT = 'http://localhost:8000'


class Transaction(object):

    def run(self):
        init_timer = time.time()
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

        response = br.open(URL_ROOT + '/courses/' + orgname +'/' + coursename +'/' + runtime +'/discussion/forum/'+ coursename +'_'+ runtime +'_General/threads')
        # get the page HTML to parse
        html = response.read()
        html = html.replace("&quot;", " ")
        # Regex to parse out the post UUIDs
        iterator = re.finditer('([0-9A-Fa-f]*) : { voted :', html)
        ids = set([])
        for items in iterator:
            postid = items.group(0)
            # Strip remaining regex stuff
            postid = postid.replace(" : { voted :", "")
            ids.add(postid)
        # Get a list of the unique post IDs
        ids = list(ids)

        # Open a page to have something to post from
        br.open('%s/dashboard' % URL_ROOT)
        # Build the url
        url = URL_ROOT+'/courses/' + orgname +'/' + coursename +'/' + runtime +'/discussion/threads/' + choice(ids) + '/reply'
        # Make the form
        br.form = HTMLForm(url, method='POST', enctype='multipart/form-data')
        # Propegate with lorem ipsum
        br.form.new_control('text','body',{'value':str(get_paragraphs(1)[0])})
        # Add a submit button
        br.form.new_control('submit', 'Button', {})
        br.form.set_all_readonly(False)
        # Prepare for submission
        br.form.fixup()

        # Submit it!
        response = br.submit()
        html = response.read()
        #print html
        latency = time.time() - init_timer
        self.custom_timers['overall_response'] = latency
if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers
