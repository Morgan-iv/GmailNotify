import time
import vk_api
import random
import shelve
import os.path
from os import chdir
from gmailapi import GmailApi
from botauth import number, passwd


def main():
    dbname = "shelvedb"
    pathprefix = os.path.dirname(os.path.abspath(__file__))
    chdir(pathprefix)


    gmail = GmailApi()
    newmes = set(gmail.getlist())

    db = shelve.open(dbname)
    oldmes = db['ids']
    db.close()

    resultstr = ''
    for mes in newmes - oldmes:
        tmp = gmail.getmessage(mes)
        resultstr = resultstr + 'From: {}\nSubject: {}\nSnippet: {}\n\n'.format(tmp[0], tmp[1], tmp[2])
    #print (resultstr)

    db = shelve.open(dbname)
    db['ids'] = newmes
    db.close()

    if not resultstr == '':
        vk_session = vk_api.VkApi(number, passwd)
        vk_session.auth()
        vk = vk_session.get_api()
        vk.messages.send(random_id=random.randint(0, 65536), peer_id=18269018, message=resultstr)

if __name__ == '__main__':
    main()

    '''
    dbname = "shelvedb"
    db = shelve.open(dbname)
    db['ids'] = set()
    db.close()
    #'''
