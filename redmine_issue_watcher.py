import time
import threading
from typing import List
from utils.log import logger
from redminegpt import RedmineGPT
from bots.redmine_bot import RedmineBot

class RedmineIssueWatcher:
    def __init__(self, redmine_gpt, interval=5):
        self.redmine_gpt: RedmineGPT = redmine_gpt
        self.interval = interval
        self.stopped = False
        self.bots: List[RedmineBot] = []
        self.bot_user = 'rockchip gpt'

    def add_bot(self, bot: RedmineBot):
        self.bots.append(bot)

    def remove_bot(self, bot: RedmineBot):
        self.bots.remove(bot)

    def issue_sentence_build(self, issue):
        # 获取问题描述
        issue_description = issue.subject
        logger.info(f"issue_description: {issue_description}")
        return issue_description

    def watch_issues(self):
        while not self.stopped:
            # 获取所有项目
            projects = self.redmine_gpt.redmine.project.all()

            for project in projects:
                # 获取项目的所有打开问题
                issues = self.redmine_gpt.redmine.issue.filter(project_id=project.id, status_id='open')

                # 处理新问题
                for issue in issues:
                    not_replied_bots = self.witch_bot_not_replied(issue)
                    if not_replied_bots:
                        logger.info(f"Not answered issue detected: {issue.id}")
                        self.emit_reply(not_replied_bots, issue)

            # 休眠一段时间后继续监测
            time.sleep(self.interval)

    def _check_replied_by_bot(self, journal_notes, bot_names):
        """检查给定的journal notes是否被任一bot回复过。"""
        return not any(bot_name in journal_notes for bot_name in bot_names)

    def witch_bot_not_replied(self, issue):
        """
        检查哪些机器人没有对给定的问题作出回应，然后调用机器人进行回应。
        对于性能和可维护性进行了优化。
        """
        not_replied_bots = set()
        try:
            # 使用异常处理来增强代码的健壮性
            for bot in self.bots:
                # 使用集合检查来提高性能
                if not any(bot.name in journal.notes for journal in issue.journals):
                    not_replied_bots.add(bot)
        except AttributeError as e:
            logger.error(f"Error processing issue journals: {e}")
        return not_replied_bots
    def witch_bot_not_replied2(self, issue):
        # check witch bot not replied then call bot reply
        not_replied_bots = set()
        for journal in issue.journals:
            if journal.user != self.bot_user:
                continue
            for bot in self.bots:
                if bot.name in journal.notes:
                    logger.info(f"bot {bot.name} not replied to issue {journal.notes}")
                    continue
                else:
                    not_replied_bots.add(bot)
        return not_replied_bots 

    def format_answer(self, answer, file_list, boot_name):
        # 将文件列表转换为字符串，每个文件名前加上 "* "
        file_list_str = "None"
        if file_list is not None:
            file_list_str = "\n".join(f"* {file}" for file in file_list)
        
        # 构建格式化后的字符串
        formatted_str = (
            f"### 根据收录的历史问答，给出您以下参考：\n"
            f"----\n"
            f"```\n"
            f"{answer}\n"
            f"```\n"
            f"----\n"
            f"### 如需更详细的信息，请参考以下文件：\n"
            f"{file_list_str}\n"
            f"\n"
            f"----\n"
            f"\n"
            f"**我们的工程师将在3个工作日内给出该问题的答**\n"
            f"\n"
            f"* <span style=\"background-color:lightgreen\">该条答复由LLM机器人自动生成：</span>"
            f"<span style=\"background-color:yellow\"> {boot_name}</span>"
        )
        
        return formatted_str

    def emit_reply(self, not_replied_bots, issue):
        # call bot to reply now:
        logger.info(f"issue {issue.id} not replied by bots: {not_replied_bots}")
        for bot in not_replied_bots:
            logger.info(f"emit reply to issue {issue.id} by bot {bot.name}")
            answer = bot.query(self.issue_sentence_build(issue))
            if answer is not None and answer != "":
                logger.info(f"reply to issue {issue.id} by bot {bot.name}: {answer}")
                self.redmine_gpt.add_reply_to_issue(issue_id=issue.id,
                                                    reply_text=self.format_answer(answer, None, bot.name))
                return answer

    def start(self):
        self.stopped = False
        self.thread = threading.Thread(target=self.watch_issues)
        self.thread.start()
        logger.info("RedmineIssueWatcher started")

    def stop(self):
        self.stopped = True
        self.thread.join()