import requests
import pandas as pd

# 设置 GitHub API Token 和请求头
GITHUB_TOKEN = '替换为你的 GitHub Token'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

# 设置目标 GitHub 仓库
OWNER = 'pagefaultgames'
REPO = 'pokerogue'
BASE_URL = f'https://api.github.com/repos/{OWNER}/{REPO}/issues'


# 获取 Issue 数据
def fetch_issues(page=1):
    url = f'{BASE_URL}?state=all&page={page}&per_page=100'  # 每页获取 100 条数据
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching issues: {response.status_code}")
        return []


# 提取 Issue 信息
def extract_issue_data(issues):
    issue_data = []
    for issue in issues:
        if 'pull_request' not in issue:  # 过滤掉 PR（只保留 Issue）
            issue_data.append({
                'id': issue.get('id'),
                'number': issue.get('number'),
                'title': issue.get('title'),
                'state': issue.get('state'),
                'created_at': issue.get('created_at'),
                'closed_at': issue.get('closed_at'),
                'labels': [label['name'] for label in issue.get('labels', [])]
            })
    return issue_data


# 获取所有 Issue 数据
def get_all_issues():
    all_issues = []
    page = 1
    while True:
        issues = fetch_issues(page)
        if not issues:
            break
        all_issues.extend(extract_issue_data(issues))
        page += 1
    return all_issues


# 转换为 DataFrame 并保存为 CSV
def save_issues_to_csv():
    issues_data = get_all_issues()

    if not issues_data:
        print("No issue data found.")
        return None

    df = pd.DataFrame(issues_data)

    # 保存为 CSV 文件
    df.to_csv('issue_data.csv', index=False)
    print("Issue data saved to 'issue_data.csv'")
    print(df.head())  # 显示前几行数据


# 主程序
if __name__ == '__main__':
    save_issues_to_csv()
