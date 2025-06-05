# analysis/sentiment.py
"""
基于 SnowNLP 的中文情感分析
"""
from snownlp import SnowNLP

def analyze_sentiment(text):
    """
    分析单条文本的情感倾向
    Args:
        text: 待分析的文本
    Returns:
        str: 情感标签（正面/负面/中性）
    """
    if not text or not text.strip():
        return "中性"
    
    try:
        s = SnowNLP(str(text))
        score = s.sentiments  # 0~1 之间的得分
        if score > 0.6:
            return "正面"
        elif score < 0.4:
            return "负面"
        else:
            return "中性"
    except Exception:
        return "中性"

def analyze_sentiment_batch(texts):
    """
    批量分析文本情感
    Args:
        texts: 文本列表
    Returns:
        list: 情感标签列表
    """
    return [analyze_sentiment(text) for text in texts]
