import requests

def get_subscount(user, api_key):
    try:
        req = 'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={}&key={}'.format(user, api_key)
        response = requests.get(req)
        if response.status_code != 200:
            return None
        res = response.json()
    except RequestException:
        return None
    if len(res['items']) == 0:
        return None
    subscount = int(res['items'][0]['statistics']['subscriberCount'])
    return subscount

def get_difference(user1, user2, api_key):
    subs1 = get_subscount(user1, api_key)
    if subs1 == None:
        return '{} statistics get failed'.format(user1)
    subs2 = get_subscount(user2, api_key)
    if subs2 == None:
        return '{} statistics get failed'.format(user2)
    return str(subs1 - subs2)
