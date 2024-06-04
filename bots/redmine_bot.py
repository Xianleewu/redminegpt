import os
import time
import requests
from typing import List
from utils.log import logger
import json


class RedmineBot:
    def __init__(self) -> None:
        self.server_addr = os.environ.get("SERVER_ADDR", "")
        self.server_port = os.environ.get("SERVER_PORT", "")
        self.user_id = os.environ.get("USER_ID", "")
        self.password = os.environ.get("PASSWORD", "")
        self.api_key = os.environ.get("API_KEY", "")
        self.knowledge_library = ""
        self.name = "QAnything"
        pass

    def connect(self):
        pass

    def learn_knowledge(self, knowledge: List):
        pass
    def delete_knowledge(self, knowledge: List):
        pass

    def warmup(self):
        pass 

    def teardown(self):
        pass
    
    def query(self, question: str):
        pass

    def format_response(self, response: str, file_list: List):
        # format response, adding some markdown
        # adding: This answer is from QAnything, a knowledge-based chatbot
        # and show the file list, witch answer from
        return f"{response}\n\nThis answer is from QAnything, a knowledge-based chatbot." 
