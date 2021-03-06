from six import text_type
from typing import Optional, Any

SUBJECT_WITH_BRANCH_TEMPLATE = u'{repo} / {branch}'
SUBJECT_WITH_PR_OR_ISSUE_INFO_TEMPLATE = u'{repo} / {type} #{id} {title}'

EMPTY_SHA = '0000000000000000000000000000000000000000'

COMMITS_LIMIT = 10
COMMIT_ROW_TEMPLATE = u'* [{commit_short_sha}]({commit_url}): {commit_msg}\n'
COMMITS_MORE_THAN_LIMIT_TEMPLATE = u"[and {commits_number} more commit(s)]"

PUSH_PUSHED_TEXT_WITH_URL = u"[pushed]({compare_url})"
PUSH_PUSHED_TEXT_WITHOUT_URL = u"pushed"
PUSH_COMMITS_MESSAGE_TEMPLATE = u"""{user_name} {pushed_text} to branch {branch_name}

{commits_data}
"""

FORCE_PUSH_COMMITS_MESSAGE_TEMPLATE = u"{user_name} [force pushed]({url}) to branch {branch_name}. Head is now {head}"
REMOVE_BRANCH_MESSAGE_TEMPLATE = u"{user_name} deleted branch {branch_name}"

PULL_REQUEST_OR_ISSUE_MESSAGE_TEMPLATE = u"{user_name} {action} [{type}]({url})"
PULL_REQUEST_OR_ISSUE_ASSIGNEE_INFO_TEMPLATE = u"(assigned to {assignee})"
PULL_REQUEST_BRANCH_INFO_TEMPLATE = u"\nfrom `{target}` to `{base}`"
PULL_REQUEST_OR_ISSUE_CONTENT_MESSAGE_TEMPLATE = u"\n~~~ quote\n{message}\n~~~"

def get_push_commits_event_message(user_name, compare_url, branch_name, commits_data):
    # type: (text_type, Optional[text_type], text_type, List[Dict[str, Any]]) -> text_type
    if compare_url:
        pushed_text_message = PUSH_PUSHED_TEXT_WITH_URL.format(compare_url=compare_url)
    else:
        pushed_text_message = PUSH_PUSHED_TEXT_WITHOUT_URL

    return PUSH_COMMITS_MESSAGE_TEMPLATE.format(
        user_name=user_name,
        pushed_text=pushed_text_message,
        branch_name=branch_name,
        commits_data=get_commits_content(commits_data),
    ).rstrip()

def get_force_push_commits_event_message(user_name, url, branch_name, head):
    # type: (text_type, text_type, text_type, text_type) -> text_type
    return FORCE_PUSH_COMMITS_MESSAGE_TEMPLATE.format(
        user_name=user_name,
        url=url,
        branch_name=branch_name,
        head=head
    )

def get_remove_branch_event_message(user_name, branch_name):
    # type: (text_type, text_type) -> text_type
    return REMOVE_BRANCH_MESSAGE_TEMPLATE.format(
        user_name=user_name,
        branch_name=branch_name,
    )

def get_pull_request_event_message(
        user_name, action, url,
        target_branch=None, base_branch=None,
        message=None, assignee=None, type='PR'
):
    # type: (text_type, text_type, text_type, Optional[text_type], Optional[text_type], Optional[text_type], Optional[text_type], Optional[text_type]) -> text_type
    main_message = PULL_REQUEST_OR_ISSUE_MESSAGE_TEMPLATE.format(
        user_name=user_name,
        action=action,
        type=type,
        url=url
    )
    if assignee:
        main_message += PULL_REQUEST_OR_ISSUE_ASSIGNEE_INFO_TEMPLATE.format(assignee=assignee)

    if target_branch and base_branch:
        main_message += PULL_REQUEST_BRANCH_INFO_TEMPLATE.format(
            target=target_branch,
            base=base_branch
        )
    if message:
        main_message += '\n' + PULL_REQUEST_OR_ISSUE_CONTENT_MESSAGE_TEMPLATE.format(message=message)
    return main_message.rstrip()

def get_issue_event_message(user_name, action, url, message=None, assignee=None):
    # type: (text_type, text_type, text_type, Optional[text_type], Optional[text_type]) -> text_type
    return get_pull_request_event_message(
        user_name,
        action,
        url,
        message=message,
        assignee=assignee,
        type='Issue'
    )

def get_commits_content(commits_data):
    # type: (List[Dict[str, Any]]) -> text_type
    commits_content = u''
    for commit in commits_data[:COMMITS_LIMIT]:
        commits_content += COMMIT_ROW_TEMPLATE.format(
            commit_short_sha=commit.get('sha')[:7],
            commit_url=commit.get('url'),
            commit_msg=commit.get('message').partition('\n')[0]
        )

    if len(commits_data) > COMMITS_LIMIT:
        commits_content += COMMITS_MORE_THAN_LIMIT_TEMPLATE.format(
            commits_number=len(commits_data) - COMMITS_LIMIT)
    return commits_content.rstrip()
