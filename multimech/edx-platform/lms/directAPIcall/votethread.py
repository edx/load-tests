import requests
import sys
import getopt
import random


def main(argv):
    # Defaults
    userid = "4"
    anonymous = "False"
    key = "PUT_YOUR_API_KEY_HERE"
    portnumber = "4567"
    hostname = "http://localhost"
    updown = "up"
    threadid = ""
    while threadid == "":
        threadid = random.choice(open('threadids.txt').readlines())
        threadid = threadid.replace("\n", "")
        print repr(threadid)
    try:
        opts, args = getopt.getopt(argv, "c:p:o:r:u:k:a:h:i:f:n:")
    except getopt.GetoptError:
        print '-a <anonymous (t/f)> -c <coursename> -f <"up" or "down" flag> -i <threadid> -k <apiKey> -n <hostName> -o <orgname> -p <portnumber> -r <runtime> -u <UserID>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print '-a <anonymous (t/f)> -c <coursename> -f <"up" or "down" flag> -i <threadid> -k <apiKey> -n <hostName> -o <orgname> -p <portnumber> -r <runtime> -u <UserID>'
            sys.exit()
        elif opt in ("-a"):
            if arg == 't':
                anonymous = "True"
        elif opt in ("-c"):
            coursename = arg
        elif opt in ("-f"):
            updown = arg
        elif opt in ("-i"):
            threadid = arg
        elif opt in ("-k"):
            key = arg
        elif opt in ("-n"):
            hostname = arg
        elif opt in ("-o"):
            orgname = arg
        elif opt in ("-p"):
            portnumber = arg
        elif opt in ("-r"):
            runtime = arg
        elif opt in ("-u"):
            userid = arg
    data = {"api_key": key, "user_id": userid, "value": updown, "splat": [], "captures": [threadid], "thread_id": threadid}
    result = requests.put(hostname+ ":" + portnumber + "/api/v1/threads/" + threadid + "/votes", data=data)
    text = result.text


if __name__ == "__main__":
    main(sys.argv[1:])
