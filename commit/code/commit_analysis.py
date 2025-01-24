import requests
import pandas as pd
from datetime import datetime

# 1. 设置 GitHub API 请求头，包含认证 token
GITHUB_TOKEN = '替换为你的 GitHub Token'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

# 2. 设置目标 GitHub 仓库
OWNER = 'pagefaultgames'
REPO = 'pokerogue'
BASE_URL = f'https://api.github.com/repos/{OWNER}/{REPO}/commits'


# 3. 获取所有 commits 数据
def fetch_commits(page=1):
    url = f'{BASE_URL}?page={page}&per_page=100'  # 每页获取 100 条数据
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching commits: {response.status_code}")
        return []


# 4. 提取 commit 信息并存储
def extract_commit_data(commits):
    commit_data = []
    for commit in commits:
        commit_info = commit.get('commit', {})
        commit_data.append({
            'sha': commit.get('sha'),
            'author_name': commit_info.get('author', {}).get('name'),
            'author_email': commit_info.get('author', {}).get('email'),
            'date': commit_info.get('author', {}).get('date'),
            'message': commit_info.get('message')
        })
    return commit_data


# 5. 获取所有 commit 数据（分页处理）
def get_all_commits():
    all_commits = []
    page = 1
    while True:
        commits = fetch_commits(page)
        if not commits:
            break
        all_commits.extend(extract_commit_data(commits))
        page += 1
    return all_commits


# 6. 转换为 DataFrame 并清洗数据
def process_commits_data():
    commit_data = get_all_commits()

    if not commit_data:
        print("No commit data found.")
        return None

    df = pd.DataFrame(commit_data)

    # 6.1 转换日期格式为 datetime 类型
    df['date'] = pd.to_datetime(df['date'])

    # 6.2 按日期排序
    df = df.sort_values(by='date', ascending=True)

    # 6.3 额外的清洗或处理（如：去掉空白信息、去除无效提交等）
    df = df.dropna(subset=['sha', 'author_name', 'date'])

    return df


# 7. 输出结果
def save_to_csv():
    df = process_commits_data()

    if df is not None:
        # 将结果保存为 CSV 文件
        df.to_csv('commit_data.csv', index=False)
        print("Commit data saved to 'commit_data.csv'")
        print(df.head())  # 显示前几行数据
    else:
        print("No data to save.")


if __name__ == '__main__':
    save_to_csv()
