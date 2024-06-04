from bots.redmine_bot import RedmineBot
from utils.log import logger

class QwenBot(RedmineBot):
    def __init__(self) -> None:
        super().__init__()
        logger.info("QAnything bot init...")

    def learn_knowledge(self, knowledge: List) -> None:
        pass

    def delete_knowledge(self, knowledge: List) -> None:
        pass

    def warmup(self) -> None:
        pass

    def teardown(self) -> None:
        pass

    def query(self, question: str) -> str:
        url = 'http://127.0.0.1:8777/api/local_doc_qa/local_doc_chat'
        url = f"{url}"
        headers = {
            'content-type': 'application/json'
        }
        data = {
            "user_id": "zzp",
            "kb_ids": ["KB8b3c3daac0e54d5aa44dcbefd335bb05"],
            "question": question,
        }
        print(data)
        try:
            start_time = time.time()
            response = requests.post(url=url, headers=headers, json=data, timeout=60)
            end_time = time.time()
            res = response.json()
            print(f"--->answer:{res['response']}")
            print(f"响应状态码: {response.status_code}, 响应时间: {end_time - start_time}秒")
        except Exception as e:
            print(f"请求发送失败: {e}")