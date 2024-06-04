from utils.log import logger
from utils.version import RedmineGPTVersion
from redminegpt import RedmineGPT
from redmine_issue_watcher import RedmineIssueWatcher
from bots.qanything_remote_bot import QanythingRemoteBot
from config import REDMINE_SERVER

'''
基于LangChain本地大模型的redmine自动技术支持方案
1. 方案背景
2. LangChain本地大模型简介
3. 本地知识库向量化
4. 自动技术支持方案设计
5. 方案实施，通过python调用redmine 的api
6. 方案效果评估
7. 方案优化与改进
8. 方案应用与推广
9. 工程师可以创建自己的常见问题解法文档，机器人自动分析并自动回复，
   节省时间，将更多的时间放在开发上。
10. 自动指派问题
11. 给出应该查阅的文档
TODO：过滤客户敏感信息
'''

if __name__ == '__main__':
    logger.info("\tThis is a tool for using chatgpt as redmine helper")
    logger.info("\tversion:%s", RedmineGPTVersion.code)
    logger.info("\tifno:%s", RedmineGPTVersion.info)
    logger.info("\tissue:%s", RedmineGPTVersion.issues)

    redmine_gpt_test = RedmineGPT(REDMINE_SERVER.get('host'),
                                  username=REDMINE_SERVER.get('user'),
                                  password=REDMINE_SERVER.get('password'))

    wacther = RedmineIssueWatcher(redmine_gpt_test)
    wacther.start()
    qanything_remote_bot = QanythingRemoteBot()
    wacther.add_bot(qanything_remote_bot)