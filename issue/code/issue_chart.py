import pandas as pd
import matplotlib.pyplot as plt

# 1. 加载 Issue 数据
df = pd.read_csv('../result/issue_data.csv')

# 确保 'created_at' 和 'closed_at' 列为 datetime 类型
df['created_at'] = pd.to_datetime(df['created_at'])
df['closed_at'] = pd.to_datetime(df['closed_at'])

# 2. 绘制 Issue 状态分布图
issue_status_counts = df['state'].value_counts()

plt.figure(figsize=(8, 6))
issue_status_counts.plot(kind='bar', color=['skyblue', 'lightgreen'])
plt.title('Issue Status Distribution')
plt.xlabel('Status')
plt.ylabel('Number of Issues')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 3. 修复时间分布
# 计算修复时间（天数）
df['fix_time_days'] = (df['closed_at'] - df['created_at']).dt.days

# 仅分析已关闭的 Issue
closed_issues = df[df['state'] == 'closed']

plt.figure(figsize=(10, 6))
plt.hist(closed_issues['fix_time_days'].dropna(), bins=20, color='lightcoral', alpha=0.8, edgecolor='black')
plt.title('Issue Fix Time Distribution')
plt.xlabel('Fix Time (days)')
plt.ylabel('Number of Issues')
plt.tight_layout()
plt.show()

# 4. 标签分析
# 将标签列展开为单独的记录
all_labels = df['labels'].dropna().apply(lambda x: x.strip("[]").replace("'", "").split(", "))
all_labels_flat = [label for sublist in all_labels for label in sublist]

# 统计标签使用频率
label_counts = pd.Series(all_labels_flat).value_counts()

plt.figure(figsize=(12, 6))
label_counts.plot(kind='bar', color='orange', alpha=0.8)
plt.title('Issue Label Usage Frequency')
plt.xlabel('Labels')
plt.ylabel('Number of Issues')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
