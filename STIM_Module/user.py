import json


def save_user(username):
    user = {'name': username}

    with open("user_settings\\user_%s.json" % username, 'w') as outfile:
        json.dump(user, outfile)


def load_user(username):
    with open("user_settings\\user_%s.json" % username, 'r') as file:
        return json.load(file)
