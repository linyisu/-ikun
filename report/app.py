import streamlit as st
import pandas as pd
import os
import csv
import time
import json
import hashlib
import urllib
import re
import requests
from datetime import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

st.markdown(
    """
    <style>
    .block-container {
        max-width: 55%;
        margin: 0 auto;
    }
    [data-testid="stImageContainer"] {
        display: flex;
        justify-content: center;
    }
    [data-testid="stImageContainer"] img {
        width: 65% !important;
        height: auto !important;
        border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ========== 工具函数 ==========
def get_Header():
    cookie = os.getenv('BILI_COOKIE')
    header = {
        "Cookie": cookie,
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    }
    return header

def get_avid_from_bv(bv):
    url = f'https://api.bilibili.com/x/web-interface/view?bvid={bv}'
    response = requests.get(url, headers=get_Header())
    data = response.json()
    if data.get('code', 0) != 0:
        raise Exception(f"获取avid失败: {data.get('message', '未知错误')}")
    return data['data']['aid']

def md5(code):
    return hashlib.md5(code.encode('utf-8')).hexdigest()

def fetch_comments(bv, is_second=True, max_pages=1000):
    aid = get_avid_from_bv(bv)
    pagination_str = ''
    count = 0
    comments = []

    for page in range(max_pages):
        wts = int(time.time())
        offset = f'"offset":"{pagination_str}"' if pagination_str else '"offset":""'
        payload = f"mode=2&oid={aid}&pagination_str=%7B{offset}%7D&plat=1&type=1&web_location=1315875&wts={wts}"
        w_rid = md5(payload + 'ea1db124af3c7062474693fa704f4ff8')
        url = f"https://api.bilibili.com/x/v2/reply/wbi/main?oid={aid}&type=1&mode=2&pagination_str=%7B{offset}%7D&plat=1&web_location=1315875&w_rid={w_rid}&wts={wts}"

        res = requests.get(url, headers=get_Header()).json()
        replies = res.get("data", {}).get("replies", [])
        if not replies:
            break

        for r in replies:
            count += 1
            comments.append({
                "用户名": r["member"]["uname"],
                "评论内容": r["content"]["message"],
                "点赞数": r["like"],
                "评论时间": datetime.fromtimestamp(r["ctime"]).strftime('%Y-%m-%d %H:%M:%S'),
            })

        pagination_str = res['data']['cursor']['pagination_reply'].get('next_offset', 0)
        if not pagination_str:
            break
        time.sleep(0.5)
    
    return comments

# ========== Streamlit App ==========
def main():
    load_dotenv()
    st.title("🎥 B站评论爬取器")

    bv = st.text_input("请输入BV号:", "")
    is_click = st.button("开始爬取")

    df = None
    file_path = None

    if is_click and bv:
        with st.spinner("正在爬取评论中..."):
            try:
                data = fetch_comments(bv)  # 只爬18页防止太慢
                # cy
                if not data:
                    st.warning("没有爬取到任何评论。")
                    return
                df = pd.DataFrame(data)
                st.session_state['df'] = df  # 存入session_state
                st.success(f"✅ 爬取成功，共 {len(df)} 条评论")
                # 只显示一次评论区和下载按钮
                with st.container():
                    st.dataframe(df, key="comments_df")
                    file_path = f"data/{bv}_comments.csv"
                    df.to_csv(file_path, index=False, encoding="utf-8-sig")
                    st.session_state['file_path'] = file_path  # 存入session_state
                    st.download_button("📥 下载评论 CSV 文件", data=df.to_csv(index=False, encoding="utf-8-sig"), file_name=f"{bv}_comments.csv", mime="text/csv", key="download_btn")
            except Exception as e:
                st.error(f"❌ 出错了：{e}")
                import traceback
                st.text(traceback.format_exc())
                return
    # 只在有评论数据后才显示分析词云按钮
    if 'df' in st.session_state and st.session_state['df'] is not None:
        # 用st.container()分组，保证词云和评论区内容并存
        with st.container():
            if st.button("分析词云"):
                st.info("正在生成词云，请稍候...")
                df = st.session_state.get('df', None)
                file_path = st.session_state.get('file_path', None)
                if df is None and file_path:
                    df = pd.read_csv(file_path)
                if df is None or '评论内容' not in df.columns:
                    st.error("没有可用的评论内容，无法生成词云。")
                    return
                text = ' '.join(df['评论内容'].astype(str))
                # 加载停用词
                stopwords = set()
                try:
                    with open('stopwords.txt', 'r', encoding='utf-8') as f:
                        for line in f:
                            stopwords.add(line.strip())
                except FileNotFoundError:
                    stopwords = set(['的', '了', '和', '是', '我', '也', '就', '都', '而', '及', '与', '着', '或', '一个', '没有', '我们', '你', '你们', '他', '她', '它', '啊', '吧', '吗', '呢'])
                # 分词并去除停用词和单字
                words = [w for w in jieba.cut(text) if w not in stopwords and len(w) > 1]
                if not words:
                    st.warning("分词后无有效词语，无法生成词云。")
                    return
                result = ' '.join(words)
                wc = WordCloud(font_path='msyh.ttc', background_color='white', width=800, height=600)
                try:
                    wc.generate(result)
                    st.image(wc.to_array(), caption="评论词云", use_container_width=True)
                except Exception as e:
                    st.error(f"词云生成失败：{e}")
                    import traceback
                    st.text(traceback.format_exc())

if __name__ == "__main__":
    main()
