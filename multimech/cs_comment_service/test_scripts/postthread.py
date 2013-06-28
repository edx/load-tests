import sys
import getopt
from loremipsum import get_paragraphs, get_sentences
import requests
import re

def main(argv):
    # Defaults
    userid = "4"
    anonymous = "False"
    key = "PUT_YOUR_API_KEY_HERE"
    portnumber = "4567"
    hostname = "http://localhost"

    try:
        opts, args = getopt.getopt(argv, "c:p:o:r:u:k:a:h:n:")
    except getopt.GetoptError:
        print '-a <anonymous (t/f)> -c <coursename> -k <apiKey> -n <hostName> -o <orgname> -p <portnumber> -r <runtime> -u <UserID>'
        sys.exit(2)
    print opts
    for opt, arg in opts:
        if opt == '-h':
            print '-a <anonymous (t/f)> -c <coursename> -k <apiKey> -n <hostName> -o <orgname> -p <portnumber> -r <runtime> -u <UserID>'
            sys.exit()
        elif opt in ("-u"):
            userid = arg
        elif opt in ("-k"):
            key = arg
        elif opt in ("-o"):
            orgname = arg
        elif opt in ("-r"):
            runtime = arg
        elif opt in ("-c"):
            coursename = arg
        elif opt in ("-p"):
            portnumber = arg
        elif opt in ("-n"):
            hostname = arg
        elif opt in ("-a"):
            if arg == 't':
                anonymous = "True"
    data = {"body": str(get_paragraphs(1)[0]), "anonymous_to_peers": anonymous, "user_id": userid, "title": str(get_sentences(1)[0]), "commentable_id": orgname + "_" + runtime + "_General", "anonymous": "False", "course_id": orgname + "/" + coursename + "/" + runtime, "api_key": key, "splat": [], "captures": [coursename + "_" + runtime + "_General"]}
    result = requests.post(hostname + ":" + portnumber + "/api/v1/" + coursename + "_" + runtime + "_General/threads", data=data)
    text = result.text
    print text
    fo = open("threadids.txt", "a")
    iterator = re.finditer('([0-9A-Fa-f]*)","user_id', text)
    print "======="
    for items in iterator:
        postid = items.group(0)
        # Strip remaining regex stuff
        postid = postid.replace('","user_id', "")
        print postid
        fo.write("\n" + str(postid))


if __name__ == "__main__":
    main(sys.argv[1:])
