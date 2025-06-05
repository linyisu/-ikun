"""
词云与分词分析模块
"""
import jieba
from wordcloud import WordCloud
from collections import Counter
from config.settings import STOPWORDS_PATH, DEFAULT_STOPWORDS, WORDCLOUD_CONFIG

def load_stopwords(filepath=None):
    stopwords = set()
    if filepath is None:
        filepath = STOPWORDS_PATH
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                stopwords.add(line.strip())
    except FileNotFoundError:
        stopwords = DEFAULT_STOPWORDS.copy()
    return stopwords

def generate_wordcloud(text, stopwords=None):
    if stopwords is None:
        stopwords = load_stopwords()
    words = [w for w in jieba.cut(text) if w not in stopwords and len(w) > 1]
    if not words:
        return None
    result = ' '.join(words)
    wc = WordCloud(
        font_path=WORDCLOUD_CONFIG['font_path'],
        background_color=WORDCLOUD_CONFIG['background_color'],
        width=WORDCLOUD_CONFIG['width'],
        height=WORDCLOUD_CONFIG['height'],
        max_words=WORDCLOUD_CONFIG['max_words'],
        colormap=WORDCLOUD_CONFIG['colormap']
    )
    wc.generate(result)
    return wc.to_array()

def generate_wordcloud_data(text, stopwords=None, top_n=200):
    if stopwords is None:
        stopwords = load_stopwords()
    words = [w for w in jieba.cut(text) if w not in stopwords and len(w) > 1]
    if not words:
        return []
    word_freq = Counter(words)
    return [{"name": k, "value": v} for k, v in word_freq.most_common(top_n)]
