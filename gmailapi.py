from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os.path

class GmailApi():

    """Main class that provides auth, getlist and getmessage"""

    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

    def __init__(self, tokenname='token.json', credsname='credentials.json'):
        store = file.Storage(tokenname)
        creds = store.get()
        if not creds or creds.invalid:
            print ('we fucked up')
            flow = client.flow_from_clientsecrets(credsname, self.SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('gmail', 'v1', http=creds.authorize(Http()))

    def getlist(self):
        response = self.service.users().messages().list(userId='me', q="is:unread newer_than:1d").execute()
        result = []
        if response['resultSizeEstimate'] == 0:
            return result
        for mes in response['messages']:
            result.append(mes['id'])
        return result

    def getmessage(self, messageID):
        message = self.service.users().messages().get(userId='me',
                                                      id=messageID,
                                                      format="metadata",
                                                      metadataHeaders=['Subject', 'From']).execute()
        subject = message['payload']['headers'][0]['value']
        sender = message['payload']['headers'][1]['value']
        if message['payload']['headers'][1]['name'] == 'Subject':
            subject, sender = sender, subject
        snippet = message['snippet']
        return sender, subject, snippet

def main():
    pass

if __name__ == '__main__':
    main()
