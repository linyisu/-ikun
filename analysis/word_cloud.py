"""
词云分析模块
"""
import pandas as pd
import jieba
from wordcloud import WordCloud
from collections import Counter
from config.settings import STOPWORDS_PATH, DEFAULT_STOPWORDS, DATA_DIR

def load_stopwords(filepath=None):
    """读取停用词表"""
    if filepath is None:
        filepath = STOPWORDS_PATH
    
    stopwords = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    stopwords.add(word)
    except FileNotFoundError:
        print(f"停用词文件 {filepath} 未找到，使用默认停用词")
        stopwords = DEFAULT_STOPWORDS.copy()
    
    return stopwords

def preprocess_text(text, stopwords):
    """文本预处理：分词并去除停用词"""
    words = [w for w in jieba.cut(text) if w not in stopwords and len(w) > 1]
    return words

def generate_wordcloud(text, stopwords=None, save_path=None):
    """生成词云图片"""
    if stopwords is None:
        stopwords = load_stopwords()
    
    words = preprocess_text(text, stopwords)
    if not words:
        return None
    
    result = ' '.join(words)
    
    # 创建词云对象
    wc = WordCloud(
        font_path='msyh.ttc',
        background_color='white',
        width=900,
        height=500,
        max_words=200,
        colormap='rainbow',  # 彩虹色
        prefer_horizontal=0.9,
        scale=2,
        contour_width=2,
        contour_color='steelblue',
        random_state=42
    )
    
    # 生成词云
    wc.generate(result)
    
    # 保存词云图片
    if save_path:
        wc.to_file(save_path)
        print(f'词云已保存到 {save_path}')
    
    return wc.to_array()

def generate_wordcloud_data(text, stopwords=None, top_n=50):
    """生成词云数据（用于交互式词云）"""
    if stopwords is None:
        stopwords = load_stopwords()
    
    words = preprocess_text(text, stopwords)
    if not words:
        return []
    
    word_freq = Counter(words)
    # 返回前N个高频词
    return [{"name": word, "value": freq} for word, freq in word_freq.most_common(top_n)]

def analyze_comments_from_csv(csv_path, content_column='content'):
    """从CSV文件分析评论生成词云"""
    try:
        df = pd.read_csv(csv_path)
        if content_column not in df.columns:
            # 尝试常见的列名
            possible_columns = ['content', '评论内容', 'message', 'comment']
            for col in possible_columns:
                if col in df.columns:
                    content_column = col
                    break
            else:
                print(f"未找到评论内容列，可用列名: {list(df.columns)}")
                return None, None
        
        # 合并所有评论内容
        text = ' '.join(df[content_column].astype(str))
        
        # 加载停用词
        stopwords = load_stopwords()
        
        # 生成词云图片
        wordcloud_array = generate_wordcloud(text, stopwords, DATA_DIR / 'wordcloud.png')
        
        # 生成词云数据
        wordcloud_data = generate_wordcloud_data(text, stopwords)
        
        return wordcloud_array, wordcloud_data
        
    except Exception as e:
        print(f"分析评论时出错: {e}")
        return None, None

if __name__ == "__main__":
    # 示例用法
    result = analyze_comments_from_csv(DATA_DIR / 'comments.csv')
    if result[0] is not None:
        print("词云分析完成！")
    else:
        print("词云分析失败！")
