import time
import vk_api
import random
import shelve
import os.path
import sys
import pewds
from os import chdir
from gmailapi import GmailApi
from botauth import vk_token, yt_token
from cutexcess import whitelist, blacklist

def vk_send(token, peer_id, message):
    vk_session = vk_api.VkApi(token=token)
    vk_session.method('messages.send', {'random_id' : random.randint(0, 65536), 'peer_id' : peer_id, 'message' : message})

def main():
    dbname = "shelvedb"
    max_vk_message = 4096
    peer_id = 18269018
    pathprefix = os.path.dirname(os.path.abspath(__file__))
    chdir(pathprefix)

    gmail = GmailApi()
    if gmail.innerstate() != 0:
        vk_send(vk_token, peer_id, 'something wrong')
        open('stopfile', 'w').close()
        sys.exit(1)
    newmes = set(gmail.getlist())

    db = shelve.open(dbname)
    oldmes = db['ids']
    db.close()

    resultstr = 'new day\n\n' if (time.localtime().tm_hour == 0) else ''
    length = len(resultstr)

    '''
    resultstr += 'PewDiePie vs T-Series:\n'
    resultstr += pewds.get_difference('PewDiePie', 'TSeries', yt_token) + '\n\n'
    length = len(resultstr)
    '''

    for mes in newmes - oldmes:
        tmp = gmail.getmessage(mes)

        flag = True
        for b in blacklist:
            flag = b not in tmp[1]
            if not flag:
                break
        if not flag:
            for w in whitelist:
                flag = w in tmp[1]
                if flag:
                    break

        if flag:
            gotemail = 'From: {}\nSubject: {}\nSnippet: {}\n\n'.format(tmp[0], tmp[1], tmp[2])
            if length + len(gotemail) < 4096:
                length = length + len(gotemail)
                resultstr = resultstr + gotemail
            else:
                vk_send(vk_token, peer_id, resultstr)
                resultstr = gotemail
                length = len(gotemail)
                time.sleep(5)

    db = shelve.open(dbname)
    db['ids'] = newmes
    db.close()

    if not resultstr == '':
        vk_send(vk_token, peer_id, resultstr)

if __name__ == '__main__':
    main()
