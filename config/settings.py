"""
应用程序配置模块。
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
# 项目根目录 (假设 settings.py 在 config 文件夹中)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

# --- 路径配置 ---
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
STOPWORDS_PATH = CONFIG_DIR / "stopwords.txt"

# --- B站API配置 ---
BILIBILI_API_SETTINGS = {
    "video_info_url": "https://api.bilibili.com/x/web-interface/view",
    "comment_api_url": "https://api.bilibili.com/x/v2/reply/wbi/main", # 使用带WBI签名的新版API
    "comment_api_salt": "ea1db124af3c7062474693fa704f4ff8", # WBI签名的salt，可能会变动
    "user_agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
}

# --- 默认停用词 ---
# 如果停用词文件加载失败，则使用此列表
DEFAULT_STOPWORDS = set([
    '的', '了', '和', '是', '我', '也', '就', '都', '而', '及', '与', '着', '或', '一个',
    '没有', '我们', '你', '你们', '他', '她', '它', '啊', '吧', '吗', '呢', '哈', '噢', '哦',
    '嗯', '嘿', '哼', '啦', '呀', '喂', '哎', '哎呀', '唉', '这个', '那个', '这些', '那些',
    '什么', '为什么', '怎么', '因为', '所以', '但是', '然而', '如果', '那么', '然后',
    '不是', '不要', '不行', '不了', '还有', '就是', '比如', '其他', '另外', '一种',
    '一样', '时候', '地方', '这里', '那里', '大家', '自己', '知道', '看到', '觉得',
    '一个', '一些', '有点', '这种', '这么', '那么', '如何', '可能', '应该', '必须',
    '可以', '不能', '需要', '感觉', '问题', '情况', '表示', '来说', '出来', '起来',
    '进行', '方面', '现在', '以后', '之前', '还是', '还有', '以上', '以下', '左右',
    '关于', '对于', '时候', '时候', '时候', '真的', '确实', ' اصلا', 'nbsp', ' ', '\n', '\r\n'
])

# --- Streamlit UI 配置 ---
STREAMLIT_PAGE_CONFIG = {
    "page_title": "B站评论分析器 Pro",
    "page_icon": "📊",
    "layout": "wide", # "centered" 或 "wide"
    "initial_sidebar_state": "expanded" # "auto", "expanded", "collapsed"
}

# --- 爬虫相关配置 ---
CRAWLER_CONFIG = {
    "max_pages_to_fetch": 100, # 默认最大爬取页数
    "fetch_delay_seconds": 0.5, # 爬取每页后的延时
    "default_bv_example": "BV1fb4y1u7p6" # Streamlit界面中BV号输入框的示例
}

# --- 词云配置 ---
WORDCLOUD_CONFIG = {
    "font_path": "msyh.ttc",  # 词云字体路径，确保系统中有此字体或更换为可用字体
    "background_color": "white",
    "width": 900,
    "height": 500,
    "max_words": 200,
    "colormap": "viridis", # 可选: 'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'rainbow', 'jet'等
    "stopwords_file": STOPWORDS_PATH,
    "default_stopwords": DEFAULT_STOPWORDS
}

# --- ECharts 交互词云配置 ---
ECHARTS_WORDCLOUD_OPTIONS = {
    "backgroundColor": "#f5f7fa",
    "tooltip": {"show": True},
    "series": [{
        "type": 'wordCloud',
        "shape": 'diamond', # 'circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star'
        "gridSize": 6,
        "sizeRange": [15, 80],
        "rotationRange": [-45, 45],
        "rotationStep": 15,
        "left": "center",
        "top": "center",
        "width": "95%",
        "height": "95%",
        "textStyle": {
            "fontFamily": "Microsoft YaHei", # 微软雅黑
            "fontWeight": "normal",
            "color": { # 随机颜色函数
                "type": "radial", "x": 0.5, "y": 0.5, "r": 0.5,
                "colorStops": [
                    {"offset": 0, "color": "#1f77b4"}, # 蓝色系
                    {"offset": 0.25, "color": "#ff7f0e"}, # 橙色系
                    {"offset": 0.5, "color": "#2ca02c"}, # 绿色系
                    {"offset": 0.75, "color": "#d62728"}, # 红色系
                    {"offset": 1, "color": "#9467bd"}  # 紫色系
                ]
            }
        },
        "emphasis": {
            "focus": "self",
            "textStyle": {"shadowBlur": 10, "shadowColor": "#333"}
        },
        "drawOutOfBound": False,
        # data: 将由程序动态填充
    }]
}


# --- Altair 图表配置 ---
ALTAIR_CHART_CONFIG = {
    "line_color_crawler": "#409EFF",
    "line_color_csv": "#13c2c2",
    "point_color_crawler": "#FF6B6B",
    "point_color_csv": "#4ECDC4",
    "chart_width": 700, # 在Streamlit中通常用 use_container_width=True
    "chart_height": 350
}


def get_bilibili_cookie():
    """从环境变量获取B站Cookie"""
    cookie = os.getenv('BILI_COOKIE')
    if not cookie:
        # st.warning("警告：未在 .env 文件中配置 BILI_COOKIE。爬虫功能可能受限或失败。")
        print("警告：未在 .env 文件中配置 BILI_COOKIE。爬虫功能可能受限或失败。")
    return cookie

def get_request_headers():
    """获取包含Cookie和User-Agent的请求头"""
    return {
        "Cookie": get_bilibili_cookie(),
        "User-Agent": BILIBILI_API_SETTINGS["user_agent"]
    }

# 确保data目录存在
if not DATA_DIR.exists():
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        print(f"数据目录 {DATA_DIR} 已创建。")
    except Exception as e:
        print(f"创建数据目录 {DATA_DIR} 失败: {e}")

