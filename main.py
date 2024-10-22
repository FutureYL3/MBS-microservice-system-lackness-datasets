import os
from github import Github, GithubException
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "spring-petclinic"
REPO_NAME = "spring-petclinic-microservices"
AFTER_DATE_STR = "2023-12-28T00:00:00Z"

g = Github(GITHUB_TOKEN, retry=3, timeout=30)
client = OpenAI(
      base_url="https://api.gptsapi.net/v1",
      api_key=OPENAI_API_KEY
  )

def summarize_text(text):
    """
    使用 OpenAI 的 GPT 模型对文本进行摘要。

    :param text: 需要摘要的文本
    :param max_tokens: 摘要的最大长度
    :return: 摘要后的文本
    """
    try:
        response = client.chat.completions.create(
            model="o1-mini",
            messages=[
                {"role": "user", "content": f"你是一个帮助分析GitHub上某个被标记为bug的issue或pr的专业人士。"
                                            f"\n请阅读以下描述中关于此issue或pr的描述和评论，并进一步阅读描述或评论中提及的其他issue、pr或discussion，凝练地总结或回答出这个bug是什么，可能与什么有关，可能的解决途径。"
                                            f"\n注意，不需要你输出问题描述、评论分析或可能的bug原因这些内容，仅仅简短而精确地总结或回答出这个bug是什么，可能与什么有关，可能的解决途径就好了。不要长篇大论。用中文回答"
                                            f"\n\n{text}"}
            ],
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "摘要不可用"

def search_issues_and_prs(repo_owner, repo_name, after_date, label="bug"):
    """
    搜索指定仓库中带有特定标签且在指定日期之后创建的 Issues 和 PRs，并自动总结提出原因。

    :param repo_owner: 仓库所有者
    :param repo_name: 仓库名称
    :param after_date: 创建日期的下限，格式为 ISO8601 字符串
    :param label: 要过滤的标签
    :return: 包含 Issues 和 PRs 的列表
    """
    query_issue = f"repo:{repo_owner}/{repo_name} is:issue label:{label} created:>={after_date}"
    query_pr = f"repo:{repo_owner}/{repo_name} is:pull-request label:{label} created:>={after_date}"
    try:
        issues = g.search_issues(query=query_issue)
        prs = g.search_issues(query=query_pr)
    except GithubException as e:
        print(f"Error searching issues: {e.data.get('message', e)}")
        return []

    issues_list = []
    prs_list = []
    for issue in issues:
        # 获取 Issue 的主体内容
        issue_body = issue.body or ""
        # 获取 Issue 的所有评论
        comments = issue.get_comments()
        comments_text = "\n".join([f"评论 by {comment.user.login}:\n{comment.body}" for comment in comments])
        # 合并主体内容和评论
        full_text = f"{issue_body}\n\n{comments_text}"
        # 生成摘要
        summary = summarize_text(full_text)
        try:
            issues_list.append({
                'number': issue.number,
                'title': issue.title,
                'url': issue.html_url,
                'is_pr': False,
                'created_at': issue.created_at.isoformat(),
                'updated_at': issue.updated_at.isoformat(),
                'summary': summary

            })
        except Exception as e:
            print(f"Error processing issue #{issue.number}: {e}")

    for pr in prs:
        # 获取 PR 的主体内容
        pr_body = pr.body or ""
        # 获取 PR 的所有评论
        comments = pr.get_comments()
        comments_text = "\n".join([f"评论 by {comment.user.login}:\n{comment.body}" for comment in comments])
        # 合并主体内容和评论
        full_text = f"{pr_body}\n\n{comments_text}"
        # 生成摘要
        summary = summarize_text(full_text)
        try:
            prs_list.append({
                'number': pr.number,
                'title': pr.title,
                'url': pr.html_url,
                'is_pr': True,
                'created_at': pr.created_at.isoformat(),
                'updated_at': pr.updated_at.isoformat(),
                'summary': summary
            })
        except Exception as e:
            print(f"Error processing PR #{pr.number}: {e}")

    return issues_list + prs_list

def add_prefix_to_lines(text, prefix):
    return '\n'.join(prefix + line for line in text.split('\n'))

if __name__ == "__main__":
    data = search_issues_and_prs(REPO_OWNER, REPO_NAME, AFTER_DATE_STR)
    with open('/Users/yl/log.md', 'a', encoding='utf-8') as f:
        if not data:
            f.write("没有符合条件的 Issues 或 Pull Requests。\n")
        else:
            for item in data:
                summary_with_prefix = add_prefix_to_lines(item['summary'], '> ')
                type_item = "#### PR" if item['is_pr'] else "#### Issue"
                f.write(f"{type_item} #{item['number']}\n**title**: {item['title']}\n**url**: {item['url']}\n")
                f.write(f"**创建时间**: {item['created_at']}, **更新时间**: {item['updated_at']}\n")
                f.write(f"**提出原因摘要**:\n{summary_with_prefix}\n")
