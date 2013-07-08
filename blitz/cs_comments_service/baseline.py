from blitz.sprint import Sprint
from scripts.search import Search
from scripts.users import User

USER_ID = 'zoldak@edx.org'
API_KEY = '4d45fc15-539c4c39-eb0064d8-4d75cc78'


def callback(result):
    print("> Result:")
    print("\tregion: " + result.region)
    print("\tduration: " + str(result.duration))
    for step in result.steps:
        print("> Step:")
        print("\tstatus: " + str(step.response.status))
        print("\tduration: " + str(step.duration))
        print("\tconnect: " + str(step.connect))


def main():
    steps = []
    step_list = []

    # steps.append(Search(api_call='get_search_threads'))
    steps.append(User(api_call='get_user'))

    for step in steps:
        step_list.append({'method': step.method, 'url': step.url, 'content': step.content})

    options = {'steps': step_list}

    s = Sprint(USER_ID, API_KEY)

    from pdb import set_trace; set_trace()
    s.execute(options, callback)

if __name__ == '__main__':
    main()
