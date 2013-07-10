from blitz.sprint import Sprint
# from scripts.search import Search
from scripts.users import User

USER_ID = 'test@edx.org'
API_KEY = 'PUT_YOUR_API_KEY_HERE'


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

    steps.append(User(api_call='get_user'))

    for step in steps:
        param_list = '&'.join(['%s=%s' % (k, v) for k, v in step.params.items()])
        step_list.append({
            'method': step.method, 'url': '%s?%s' % (step.url, param_list), 'timeout': 10000})

    options = {'steps': step_list}

    s = Sprint(USER_ID, API_KEY)
    print options['steps']
    s.execute(options, callback)

if __name__ == '__main__':
    main()
