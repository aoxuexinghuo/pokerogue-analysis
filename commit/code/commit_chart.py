import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import re

# 1. 加载 CSV 数据
df = pd.read_csv('../result/commit_data.csv')

# 确保 'date' 列为 datetime 类型
df['date'] = pd.to_datetime(df['date'])

# 2. 每月提交次数统计
df['month'] = df['date'].dt.to_period('M')  # 按月分组
monthly_commits = df.groupby('month').size()  # 每月提交次数

# 绘制每月提交次数图
plt.figure(figsize=(12, 6))
monthly_commits.plot(kind='bar', color='skyblue', alpha=0.8)
plt.title('Monthly Commits')
plt.xlabel('Month')
plt.ylabel('Number of Commits')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. 提交信息关键词统计
# 合并提交消息为一个字符串
all_messages = ' '.join(df['message'].dropna())

# 文本清洗：只保留字母和数字
cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', all_messages)

# 分词并统计词频
words = cleaned_text.lower().split()
word_counts = Counter(words)

# 提取最常见的前 20 个词
top_words = word_counts.most_common(20)
word_df = pd.DataFrame(top_words, columns=['word', 'count'])

# 绘制关键词分布图
plt.figure(figsize=(12, 6))
plt.bar(word_df['word'], word_df['count'], color='lightgreen')
plt.title('Top 20 Most Frequent Words in Commit Messages')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
