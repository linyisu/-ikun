"""
B站评论分析 Streamlit 应用
"""
import sys
from pathlib import Path

# 将项目根目录添加到 sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
from config.settings import STREAMLIT_PAGE_CONFIG, DATA_DIR # MODIFIED

# ✅ 最先设置 Stremlit 页面配置（必须在任何 Streamlit 调用之前）
st.set_page_config(**STREAMLIT_PAGE_CONFIG)

import time
import os
import pandas as pd
import plotly.express as px
import altair as alt
from dotenv import load_dotenv

from crawler.bilibili_crawler import fetch_comments
from analysis.word_cloud import load_stopwords, generate_wordcloud, generate_wordcloud_data
from analysis.sentiment import analyze_sentiment_batch

# 加载环境变量
load_dotenv(dotenv_path=project_root / '.env')

# 页面样式美化
st.markdown(
    """
    <style>
    .block-container { max-width: 55%; margin: 0 auto; }
    [data-testid="stImageContainer"] { display: flex; justify-content: center; }
    [data-testid="stImageContainer"] img { width: 100% !important; height: auto !important; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); display: block; margin-left: auto; margin-right: auto; }
    .st-echarts-canvas, .stEcharts > div > canvas, canvas, [data-zr-dom-id^="zr_"] {
        border-radius: 20px !important;
        border: 2px solid #333 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def render_trend_chart(df, key_prefix, animated=False):
    df['评论时间'] = pd.to_datetime(df['评论时间'])
    min_date = df['评论时间'].min().date()
    max_date = df['评论时间'].max().date()
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        start_date = st.date_input("起始日期", min_value=min_date, max_value=max_date, value=min_date, key=f"{key_prefix}_start")
    with col2:
        end_date = st.date_input("结束日期", min_value=min_date, max_value=max_date, value=max_date, key=f"{key_prefix}_end")
    with col3:
        freq = st.radio("聚合粒度", ["按天", "按自然周"], horizontal=True, key=f"{key_prefix}_freq")

    mask = (df['评论时间'].dt.date >= start_date) & (df['评论时间'].dt.date <= end_date)
    df_filtered = df.loc[mask].copy()
    if df_filtered.empty:
        st.warning("所选区间内无评论数据！")
        return

    if freq == "按天":
        df_filtered['日期'] = df_filtered['评论时间'].dt.strftime('%Y-%m-%d')
        count_df = df_filtered.groupby('日期').size().reset_index(name='评论数')
        x_col = '日期'
    else:
        df_filtered['周区间'] = ((df_filtered['评论时间'].dt.date - start_date).apply(lambda x: x.days // 7))
        df_filtered['周起'] = df_filtered['周区间'].apply(lambda w: (start_date + pd.Timedelta(days=w * 7)))
        df_filtered['周止'] = df_filtered['周起'] + pd.Timedelta(days=6)
        df_filtered['周区段'] = df_filtered['周起'].astype(str) + '~' + df_filtered['周止'].astype(str)
        count_df = df_filtered.groupby('周区段').size().reset_index(name='评论数')
        x_col = '周区段'

    if count_df.empty:
        st.warning("聚合后无数据显示，无法生成趋势图。")
        return

    if animated:
        placeholder = st.empty()
        for i in range(1, len(count_df) + 1):
            temp_df = count_df.iloc[:i]
            chart = alt.Chart(temp_df).mark_line(point=True, interpolate='monotone').encode(
                x=alt.X(x_col, title="时间"),
                y=alt.Y('评论数', title="评论数量"),
                tooltip=[x_col, '评论数']
            ).properties(width=700, height=350)
            placeholder.altair_chart(chart, use_container_width=True)
            time.sleep(0.05)
        st.altair_chart(chart, use_container_width=True)
    else:
        chart = alt.Chart(count_df).mark_line(point=True, interpolate='monotone').encode(
            x=alt.X(x_col, title="时间"),
            y=alt.Y('评论数', title="评论数量"),
            tooltip=[x_col, '评论数']
        ).properties(width=700, height=350).interactive()
        st.altair_chart(chart, use_container_width=True)

def sentiment_analysis(df, key):
    if st.button("情感分析", key=key):
        with st.spinner("正在分析情感..."):
            sentiments = analyze_sentiment_batch(df['评论内容'].astype(str).tolist())
            df['情感'] = sentiments
            st.success("情感分析完成！")
    if '情感' in df.columns:
        st.dataframe(df)
        sentiment_count = df['情感'].value_counts().to_dict()
        fig = px.pie(names=list(sentiment_count.keys()), values=list(sentiment_count.values()), title="情感分布")
        st.plotly_chart(fig, use_container_width=True)

def show_analysis(df, key_prefix, animated=False):
    st.dataframe(df)
    st.subheader("🔎 评论数据分析")
    stopwords = load_stopwords()

    if st.button("分析词云（静态图片）", key=f"cloud_{key_prefix}"):
        text = ' '.join(df['评论内容'].astype(str))
        img = generate_wordcloud(text, stopwords)
        st.session_state[f'cloud_{key_prefix}_img'] = img
    arr = st.session_state.get(f'cloud_{key_prefix}_img', None)
    if arr is not None and arr.any():
        st.image(st.session_state[f'cloud_{key_prefix}_img'], caption="评论词云", use_container_width=True)

    if st.button("分析词云（可交互）", key=f"cloud_{key_prefix}_echarts"):
        text = ' '.join(df['评论内容'].astype(str))
        data = generate_wordcloud_data(text, stopwords)
        st.session_state[f'cloud_{key_prefix}_data'] = data
    if st.session_state.get(f'cloud_{key_prefix}_data', None):
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
                "data": st.session_state[f'cloud_{key_prefix}_data']
            }]
        }
        st_echarts(option, height="600px")

    st.markdown("---")
    st.subheader("📈 评论数量随时间变化曲线")
    if '评论时间' in df.columns:
        render_trend_chart(df, key_prefix, animated)

    st.markdown("---")
    sentiment_analysis(df, f"sentiment_{key_prefix}")

def main():
    st.title("🎥 B站评论爬取分析器")
    st.sidebar.title("🧭 功能导航")
    page = st.sidebar.selectbox("选择功能", ["📡 在线爬取与分析", "📁 本地数据分析"])

    if page == "📡 在线爬取与分析":
        st.header("📡 在线爬取与分析")
        bv = st.text_input("请输入BV号:", "")
        is_click = st.button("开始爬取")
        df = st.session_state.get('df_online', None)
        if is_click and bv:
            with st.spinner("正在爬取评论中..."):
                try:
                    data = fetch_comments(bv, max_pages=20)
                    if not data:
                        st.warning("没有爬取到任何评论。")
                    else:
                        df = pd.DataFrame(data)
                        st.session_state['df_online'] = df
                        st.success(f"✅ 爬取成功，共 {len(df)} 条评论")
                        file_path = DATA_DIR / f"{bv}_comments.csv"
                        df.to_csv(file_path, index=False, encoding="utf-8-sig")
                        st.download_button("📥 下载评论 CSV 文件", data=df.to_csv(index=False, encoding="utf-8-sig"), file_name=f"{bv}_comments.csv", mime="text/csv")
                except Exception as e:
                    st.error(f"❌ 出错了：{e}")
        if df is not None:
            show_analysis(df, key_prefix='online', animated=True)
        else:
            st.info("请先爬取评论数据后再分析。")

    elif page == "📁 本地数据分析":
        st.header("📁 本地数据分析")
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        file_choice = st.selectbox("选择CSV文件", csv_files) if csv_files else None
        if file_choice:
            df = pd.read_csv(DATA_DIR / file_choice)
            st.session_state['df_local'] = df
        df = st.session_state.get('df_local', None)
        if df is not None:
            show_analysis(df, key_prefix='local', animated=False)
        elif csv_files:
            st.info("请选择一个CSV文件后再分析。")
        else:
            st.info("data 目录下没有CSV文件。请先爬取或上传数据。")

if __name__ == "__main__":
    main()