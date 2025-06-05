"""
B站评论分析 Streamlit 应用
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
import streamlit as st
import pandas as pd

from crawler.bilibili_crawler import fetch_comments
from analysis.word_cloud import load_stopwords, generate_wordcloud, generate_wordcloud_data
from config.settings import DATA_DIR, STREAMLIT_PAGE_CONFIG

# 加载环境变量
load_dotenv(dotenv_path=project_root / '.env')

# Streamlit 页面配置
st.set_page_config(**STREAMLIT_PAGE_CONFIG)

# 页面样式美化
st.markdown(
    """
    <style>
    .block-container { max-width: 55%; margin: 0 auto; }
    [data-testid="stImageContainer"] { display: flex; justify-content: center; }
    [data-testid="stImageContainer"] img { width: 65% !important; height: auto !important; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); display: block; margin-left: auto; margin-right: auto; }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("🎥 B站评论爬取分析器")
    st.sidebar.title("🧭 功能导航")
    page = st.sidebar.selectbox(
        "选择功能",
        ["📡 评论爬取", "📊 数据分析", "📁 本地数据查看"]
    )

    if page == "📡 评论爬取":
        st.header("📡 评论爬取")
        bv = st.text_input("请输入BV号:", "")
        is_click = st.button("开始爬取")
        if is_click and bv:
            with st.spinner("正在爬取评论中..."):
                try:
                    data = fetch_comments(bv, max_pages=15)
                    if not data:
                        st.warning("没有爬取到任何评论。")
                        return
                    df = pd.DataFrame(data)
                    st.session_state['df'] = df
                    st.success(f"✅ 爬取成功，共 {len(df)} 条评论")
                    st.dataframe(df)
                    file_path = DATA_DIR / f"{bv}_comments.csv"
                    df.to_csv(file_path, index=False, encoding="utf-8-sig")
                    st.download_button("📥 下载评论 CSV 文件", data=df.to_csv(index=False, encoding="utf-8-sig"), file_name=f"{bv}_comments.csv", mime="text/csv")
                except Exception as e:
                    st.error(f"❌ 出错了：{e}")
    elif page == "📊 数据分析":
        st.header("📊 数据分析")
        if 'df' in st.session_state and st.session_state['df'] is not None:
            df = st.session_state['df']
            stopwords = load_stopwords()
            if st.button("分析词云（静态图片）"):
                text = ' '.join(df['评论内容'].astype(str))
                img = generate_wordcloud(text, stopwords)
                if img is None:
                    st.warning("分词后无有效词语，无法生成词云。")
                else:
                    st.image(img, caption="评论词云", use_container_width=True)
            if st.button("分析词云（可交互）"):
                text = ' '.join(df['评论内容'].astype(str))
                data = generate_wordcloud_data(text, stopwords)
                if not data:
                    st.warning("分词后无有效词语，无法生成词云。")
                else:
                    from streamlit_echarts import st_echarts
                    option = {
                        "backgroundColor": "#f5f7fa",
                        "tooltip": {"show": True},
                        "series": [{
                            "type": 'wordCloud',
                            "shape": 'star',
                            "gridSize": 8,
                            "sizeRange": [20, 90],
                            "rotationRange": [-45, 90],
                            "rotationStep": 15,
                            "left": "center",
                            "top": "center",
                            "width": "100%",
                            "height": "100%",
                            "textStyle": {
                                "fontFamily": "微软雅黑",
                                "fontWeight": "bold",
                                "shadowColor": "#b7e3fa",
                                "shadowBlur": 8,
                                "color": {
                                    "type": "radial",
                                    "x": 0.5,
                                    "y": 0.5,
                                    "r": 0.8,
                                    "colorStops": [
                                        {"offset": 0, "color": "#91caff"},
                                        {"offset": 0.5, "color": "#f9e79f"},
                                        {"offset": 1, "color": "#ffb3b3"}
                                    ]
                                }
                            },
                            "emphasis": {
                                "focus": "self",
                                "textStyle": {
                                    "shadowBlur": 16,
                                    "shadowColor": "#fff",
                                    "color": "#faad14"
                                }
                            },
                            "drawOutOfBound": False,
                            "data": data
                        }]
                    }
                    st_echarts(option, height="600px")
        else:
            st.info("请先爬取评论数据。")
    elif page == "📁 本地数据查看":
        st.header("📁 本地数据查看")
        import os
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        if not csv_files:
            st.info("data 目录下没有CSV文件。请先爬取或上传数据。")
        else:
            file_choice = st.selectbox("选择CSV文件", csv_files)
            if file_choice:
                df = pd.read_csv(DATA_DIR / file_choice)
                st.dataframe(df)

if __name__ == "__main__":
    main()
