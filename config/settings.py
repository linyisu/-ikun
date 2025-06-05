"""
配置文件模块
"""
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"

# 停用词文件路径
STOPWORDS_PATH = CONFIG_DIR / "stopwords.txt"

# B站API相关配置
BILIBILI_API = {
    'video_info': 'https://api.bilibili.com/x/web-interface/view',
    'comment_api': 'https://api.bilibili.com/x/v2/reply/main',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

# 默认停用词列表
DEFAULT_STOPWORDS = {
    '的', '了', '和', '是', '我', '也', '就', '都', '而', '及', '与', '着', '或', 
    '一个', '没有', '我们', '你', '你们', '他', '她', '它', '啊', '吧', '吗', '呢',
    '这个', '那个', '这样', '那样', '什么', '怎么', '为什么', '因为', '所以', '但是',
    '然后', '如果', '不过', '可是', '虽然', '尽管', '即使', '无论', '不管', '除了',
    '哈哈', '呵呵', '嘿嘿', '嘻嘻', '哇', '哎', '唉', '额', '嗯', '哦', '咦', '咳'
}

def get_cookie():
    """获取B站Cookie"""
    return os.getenv('BILI_COOKIE', '')

def get_headers():
    """获取请求头"""
    return {
        "Cookie": get_cookie(),
        "User-Agent": BILIBILI_API['user_agent']
    }
