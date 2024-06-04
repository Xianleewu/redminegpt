from bots.redmine_bot import RedmineBot
from utils.AuthV3Util import addAuthParams
import json
import requests
from utils.log import logger
from config import QANYTHING_REMOTE_SERVER
import os


class QanythingRemoteBot(RedmineBot):
    def __init__(self) -> None:
        super().__init__()
        self.server_addr = os.environ.get("SERVER_ADDR", "")
        self.server_port = os.environ.get("SERVER_PORT", "")
        self.app_key = QANYTHING_REMOTE_SERVER.get('app_key')
        self.app_secret = QANYTHING_REMOTE_SERVER.get('app_secret')
        self.kb_id = QANYTHING_REMOTE_SERVER.get('kb_id')
        self.name = "QAnythingRemoteBot"

    def doCall(self, url, header, params, method):
        if 'get' == method:
            return requests.get(url, params)
        elif 'post' == method:
            return requests.post(url, params, headers=header)

    def chat(self, kbId, q):
        data = {'q': '请在知识库中查找该问题的答案:' + q, 'kbIds': [kbId]}
        addAuthParams(self.app_key, self.app_secret, data)
        header = {'Content-Type': 'application/json'}
        res = self.doCall('https://openapi.youdao.com/q_anything/paas/chat', header, json.dumps(data), 'post')
        logger.info(str(res.content, 'utf-8'))
        res_json = json.loads(str(res.content, 'utf-8'))
        logger.info(f"answer summary: {res_json['result']['response']}")
        return res_json['result']['response']
    def query(self, question: str):
        return self.chat(self.kb_id, question)