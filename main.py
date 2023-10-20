import interpreter
import os
import re

BACKLOG_DOMAIN = os.environ['BACKLOG_DOMAIN']
BACKLOG_API_KEY = os.environ['BACKLOG_API_KEY']
ISSUE_TYPE_ID = os.environ['BACKLOG_API_KEY']
PRIORITY_ID = os.environ['PRIORITY_ID']
PROJECT_ID = os.environ['PROJECT_ID']

def extract_spacekey(url: str) -> str:
    # Regular expression pattern to match the spacekey followed by '.backlog'
    pattern = r'^(.*?)\.backlog'
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)
    else:
        return None


interpreter.model = "gpt-4"

# prompt should be english
interpreter.system_message += f"""
Use Backlog api and api key from `os.environ['BACKLOG_API_KEY']` when calling backlog api.
Translated list for copies in Backlog to English from Japanese. 
課題:Issue
種別:Issue Type
優先度:Priority

If you get Japanese, you should response in Japanese, otherwise English. 

- space_key = "{extract_spacekey(BACKLOG_DOMAIN)}"
- issue_type_id = {ISSUE_TYPE_ID}
- priority_id = {PRIORITY_ID}
- project_id = {PROJECT_ID}
- As API client please use `github.com/kitadakyou/PyBacklogPy` which is helpful to get Backlog resources.
Rules of `pybacklogpy`
- If domain is including `backlog.jp`, use `BacklogJpConfigure`. if `backlog.com`, use `BacklogComConfigure`, if `backlog-tool.com`, use `BacklogToolConfigure`
- For using `Issue` like this, `from pybacklogpy.Issue import Issue`
- When parse response from pybacklogpy, do this like this 
```
response = wiki_api.get_wiki_page(
    wiki_id=12345,
)

if not response.ok:
    raise ValueError('Wiki ページ情報の取得に失敗')

wiki_data = json.loads(response.text)
```
- Please see the below function list when you use pybacklogpy.

```
# pybacklogpy.Issue.Issue.add_issue
- args_name:  project_id , args_description:   課題を登録するプロジェクトのID
- args_name:  summary , args_description:   課題の件名
- args_name:  issue_type_id , args_description:   課題の種別のID
- args_name:  priority_id , args_description:   課題の優先度のID
- args_name:  parent_issue_id , args_description:   課題の親課題のID
- args_name:  description , args_description:   課題の詳細
- args_name:  start_date , args_description:   課題の開始日 (yyyy-MM-dd)
- args_name:  due_date , args_description:   課題の期限日 (yyyy-MM-dd)
- args_name:  estimated_hours , args_description:   課題の予定時間
- args_name:  actual_hours , args_description:   課題の実績時間
- args_name:  category_id , args_description:   課題のカテゴリーのID
- args_name:  version_id , args_description:   課題の発生バージョンのID
- args_name:  milestone_id , args_description:   課題のマイルストーンのID
- args_name:  assignee_id , args_description:   課題の担当者のID
- args_name:  notified_user_id , args_description:   課題の登録の通知を受け取るユーザーのID
- args_name:  attachment_id , args_description:   添付ファイルの送信APIが返すID
- args_name:  kwargs , args_description:   カスタム属性を渡す customField_id=[value] または customField_id_otherValue=[value] の形式
# pybacklogpy.Issue.Issue.delete_issue
# pybacklogpy.Issue.Issue.get_issue
# pybacklogpy.Issue.Issue.update_issue
- args_name:  issue_id_or_key , args_description:   課題のID または 課題キー
- args_name:  summary , args_description:   課題の件名
- args_name:  parent_issue_id , args_description:   課題の親課題のID
- args_name:  description , args_description:   課題の詳細
- args_name:  status_id , args_description:   状態のID
- args_name:  resolution_id , args_description:   完了理由のID
- args_name:  start_date , args_description:   課題の開始日 (yyyy-MM-dd)
- args_name:  due_date , args_description:   課題の期限日 (yyyy-MM-dd)
- args_name:  estimated_hours , args_description:   課題の予定時間
- args_name:  actual_hours , args_description:   課題の実績時間
- args_name:  issue_type_id , args_description:   課題の種別のID
- args_name:  category_id , args_description:   課題のカテゴリーのID
- args_name:  version_id , args_description:   課題の発生バージョンのID
- args_name:  milestone_id , args_description:   課題のマイルストーンのID
- args_name:  priority_id , args_description:   課題の優先度のID
- args_name:  assignee_id , args_description:   課題の担当者のID
- args_name:  notified_user_id , args_description:   課題の登録の通知を受け取るユーザーのID
- args_name:  attachment_id , args_description:   添付ファイルの送信APIが返すID
- args_name:  comment , args_description:   コメント
- args_name:  kwargs , args_description:   カスタム属性を渡す customField_{id}=[value] または customField_{id}_otherValue=[value] の形式
# pybacklogpy.Issue.IssueAttachment.get_list_of_issue_attachments
# pybacklogpy.Priority.Priority.get_priority_list
# pybacklogpy.Project.Project.add_project
- args_name:  name , args_description:   プロジェクト名
- args_name:  key , args_description:   プロジェクトキー
- args_name:  chart_enabled , args_description:   チャートを使用するかどうか(フリープランでは利用不可)
- args_name:  project_leader_can_edit_project_leader , args_description:   プロジェクト管理者も他のプロジェクト管理者を指定可能にする
- args_name:  subtasking_enabled , args_description:   親子課題を使用するかどうか(フリープランでは利用不可)
- args_name:  text_formatting_rule , args_description:   テキスト整形のルール backlog または markdown
# pybacklogpy.Project.Project.get_project
# pybacklogpy.Project.Project.get_project_icon
# pybacklogpy.Project.Project.get_project_list
- args_name:  archived , args_description:   省略された場合は全てのプロジェクト、falseの場合はアーカイブされていないプロジェクト、trueの場合はアーカイブされたプロジェクトを返します。
- args_name:  all_projects , args_description:   ユーザが管理者権限の場合のみ有効なパラメータです。trueの場合はすべてのプロジェクト、falseの場合は参加しているプロジェクトのみを返します。初期値はfalse。
# pybacklogpy.Project.Project.get_project_user_list
- args_name:  project_id_or_key , args_description:   プロジェクトのID または プロジェクトキー
- args_name:  exclude_group_members , args_description:   グループを介してプロジェクトに参加しているメンバーを除く
# pybacklogpy.Space.Space.get_space
```

"""

print(interpreter.system_message)

# interpreter.chat("Please make a list of 10 things to do for the Tokyo trip starting October 11 and register them in your Backlog as issues.")
interpreter.chat("来週東京旅行に行くのでどんなタスクが考えられるか考えてください。そのタスクをBacklogに登録しておきたいです。")
interpreter.chat() 