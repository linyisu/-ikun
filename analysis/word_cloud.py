import pandas as pd
import jieba
from wordcloud import WordCloud

# 读取停用词表
def load_stopwords(filepath='stopwords.txt'):
    stopwords = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                stopwords.add(line.strip())
    except FileNotFoundError:
        # 默认常见停用词
        stopwords = set(['的', '了', '和', '是', '我', '也', '就', '都', '而', '及', '与', '着', '或', '一个', '没有', '我们', '你', '你们', '他', '她', '它', '啊', '吧', '吗', '呢'])
    return stopwords

stopwords = load_stopwords()

# 读取 CSV 文件
df = pd.read_csv('data/comments.csv')
text = ' '.join(df['评论内容'].astype(str))

# 中文分词并去除停用词和单字
words = [w for w in jieba.cut(text) if w not in stopwords and len(w) > 1]
result = ' '.join(words)

# 创建词云对象
wc = WordCloud(
    font_path='msyh.ttc',
    background_color='white',
    width=800,
    height=600
)

# 生成词云
wc.generate(result)

# 保存词云图片
wc.to_file('data/wordcloud.png')
print('词云已保存到 data/wordcloud.png')
