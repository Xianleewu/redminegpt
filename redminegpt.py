from redminelib import Redmine
from utils.log import logger
from tqdm import tqdm
from io import BytesIO
from typing import List
import datetime
import time


class RedmineGPT:
    def __init__(self, url, username, password) -> None:
        self.redmine: Redmine = Redmine(url=url, username=username, password=password)
        self.projects = None
        self.sb_mode_enabled = True
        self.ov_mode_enabled = False

    def add_reply_to_issue(self, issue_id: int, reply_text: str) -> None:
        try:
            # 获取指定 ID 的问题
            issue = self.redmine.issue.get(issue_id)

            # 更新问题，添加注释
            issue.notes = reply_text
            issue.save()

            # 打印成功消息
            logger.info(f"Reply added to issue {issue_id} successfully.")
        
        except Exception as e:
            logger.error(f"Failed to add reply to issue {issue_id}: {e}")

    def enable_observer_mode(self, enable: bool):
        self.ov_mode_enabled = enable

    def enable_subscribe_mode(self, enable: bool):
        self.ov_mode_enabled = enable

    def export_all_project(self):
        self.projects = self.redmine.project.all()
        for project in self.projects:
            print(project)

    def export_all_issues(self):
        self.projects = self.redmine.project.all()
        for project in self.projects:
            print(project)

    def export_issue(self):
        pass

    def observe_new_issue(self):
        pass

    def observe_new_note(self):
        pass

    def parse_issue_info(self):
        pass

    def auto_reply(self):
        pass

    def on_new_issues(self):
        pass

    def callback(self, new_issue):
        print("New issue received:")
        print(f"Issue ID: {new_issue.id}")
        print(f"Subject: {new_issue.subject}")
        print(f"------------------")
        # 在这里添加你的处理逻辑，比如发送邮件通知等
        print(dir(new_issue))
        new_issue.notes.create(body="Thank you for submitting this issue! We will look into it.")
        print(f"++++++++++++++++++")


    def check_new_issues(self):
        last_issue_id = None
        while True:
            # 获取最新的问题
            try:
                latest_issue = self.redmine.issue.filter(status_id='open', limit=1)[0]
                #  latest_issue = redmine.issue.filter(status_id='open', sort='created_on:desc', limit=1)[0]
                print(f"last id:{last_issue_id}, neweset id:{latest_issue.id}")
                if last_issue_id is None:
                    last_issue_id = latest_issue.id
                elif latest_issue.id != last_issue_id:
                    # 如果有新的问题提交，则调用回调函数进行处理
                    self.callback(latest_issue)
                    last_issue_id = latest_issue.id
            except Exception as e:
                print(f"{str(e)}")

            time.sleep(5)

    def create_new_issue(self, files: List[str] = []):
        issue = self.redmine.issue.new()
        issue.project_id = 'vacation'
        issue.subject = 'Vacation'
        issue.tracker_id = 8
        issue.description = 'foo'
        issue.status_id = 3
        issue.priority_id = 7
        issue.assigned_to_id = 123
        issue.watcher_user_ids = [123]
        issue.parent_issue_id = 345
        issue.start_date = datetime.date(2014, 1, 1)
        issue.due_date = datetime.date(2014, 2, 1)
        issue.estimated_hours = 4
        issue.done_ratio = 40
        issue.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
        if len(files) > 0:
            issue.uploads = files
        issue.save()

    def add_note_to_issue(self, issue_id, note):
        try:
            # 获取指定 ID 的问题
            issue = self.redmine.issue.get(issue_id)

            # 打印问题的描述信息
            print("Issue Description:", issue.description)

            issue.update(1, notes='new notes')
            issue.save()

            # 添加新的注释
            print(dir(issue))
            for journal in issue.journals:
                journal.save(notes=note)

            print("Note added successfully.")
        except Exception as e:
            print("An error occurred:", str(e))