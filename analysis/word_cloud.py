import pandas as pd
import jieba
from wordcloud import WordCloud

# 读取 CSV 文件
df = pd.read_csv('data/comments.csv')
text = ' '.join(df['评论内容'].astype(str))

# 中文分词
words = jieba.cut(text)
result = ' '.join(words)

# 创建词云对象
wc = WordCloud(
    font_path='msyh.ttc',  # 微软雅黑
    background_color='white',
    width=800,
    height=600
)

# 生成词云
wc.generate(result)

# 保存词云图片
wc.to_file('data/wordcloud.png')
print('词云已保存到 data/wordcloud.png')
