from http_client import HttpClient
from matrix_event import MatrixEvent
from matrix_event_store import MatrixEventStore

import json

class MatrixClinet:

    MATRIX_SERVER_URL = "secretXD"
    LOGIN_URI = "/_matrix/client/r0/login"
    SYNC_URI = "/_matrix/client/r0/sync"

    ACCESS_TOKEN = ""
    USER_ID = ""
    HOME_SERVER = ""

    EVENT_STORE = MatrixEventStore()

    @staticmethod
    def do_recursive_sync(event_store, matrix_url, access_token, next_batch):
        parms = dict()
        parms["access_token"] = access_token
        parms["timeout"] = 10
        if next_batch is not None and next_batch != "":
            parms["since"] = next_batch

        json_data = HttpClient.Get(matrix_url, params=parms)
        if json_data != None:
            data = json.loads(json_data)

            next_batch_data = data["next_batch"]

            # https://github.com/matrix-org/synapse/issues/8518
            # 如果 since == next_batch，表示 Server 上面沒有推進，沒有新的 Event
            # 目前這個 Event 已經新增過了
            if "since" in parms and next_batch_data == parms["since"]:
                return

            event = MatrixEvent()
            event.Content = json_data
            event.ContentData = data
            event_store.Add(event)

            if next_batch_data is None or next_batch_data == "":
                return
            else:
                MatrixClinet.do_recursive_sync(event_store, matrix_url, access_token, next_batch_data)

    def Sync(self):
        MatrixClinet.do_recursive_sync(self.EVENT_STORE, self.MATRIX_SERVER_URL + self.SYNC_URI, self.ACCESS_TOKEN, None)

    def Login(self, username, password):
        post_data = {
            "type": "m.login.password",
            "identifier": {
                "type": "m.id.user",
                "user": username
            },
            "password": password
        }
        json_data = json.dumps(post_data)

        json_data = HttpClient.Post(self.MATRIX_SERVER_URL + self.LOGIN_URI, json_data)
        if json_data != None:
            data = json.loads(json_data)
            self.HOME_SERVER = data["home_server"]
            self.USER_ID = data["user_id"]
            self.ACCESS_TOKEN = data["access_token"]
            # print(self.ACCESS_TOKEN)
            return True

        return False
