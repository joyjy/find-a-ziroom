# -*- coding: utf-8 -*-

import os
import httplib2
import socks
import socket

from apiclient import discovery
from oauth2client.file import Storage

spreadsheetId = '1ryRmAmexspvqCYqe_SvWBOCSgCGkKpFqmSZ_CqC2atU'

class GoogleSheetPipeline(object):
    def get_credentials(self):
        credential_path = os.path.abspath('sheets.googleapis.com-find-a-ziroom.json')
        store = Storage(credential_path)
        credentials = store.get()
        return credentials

    def __init__(self):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
        socket.socket = socks.socksocket

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
        self.service.spreadsheets().values().clear(
            spreadsheetId=spreadsheetId, range='Sheet1!A:J', body={}
        ).execute()
        header = [u'距离',u'朝向',u'说明',u'价格',u'层高',u'链接',u'地铁',u'楼高',u'户型',u'面积']
        result = self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId, range='Sheet1', valueInputOption='USER_ENTERED',
            body={ 'values': [header]}).execute()

    def process_item(self, item, spider):
        result = self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheetId, range='Sheet1', valueInputOption='USER_ENTERED',
            body={ 'values': [list(item.values())] }).execute()
        return item