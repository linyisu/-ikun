"""
页面渲染模块
"""
import streamlit as st
from report.logic import fetch_comments
from analysis.word_cloud import load_stopwords, generate_wordcloud, generate_wordcloud_data
import pandas as pd
import os
from config.settings import DATA_DIR

def render_crawler_section():
    """评论爬取区块"""
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
                with st.container():
                    st.dataframe(df, key="comments_df")
                    file_path = DATA_DIR / f"{bv}_comments.csv"
                    df.to_csv(file_path, index=False, encoding="utf-8-sig")
                    st.session_state['file_path'] = file_path
                    st.download_button("📥 下载评论 CSV 文件", data=df.to_csv(index=False, encoding="utf-8-sig"), file_name=f"{bv}_comments.csv", mime="text/csv", key="download_btn")
            except Exception as e:
                st.error(f"❌ 出错了：{e}")
                import traceback
                st.text(traceback.format_exc())
                return

def render_analysis_section():
    """评论分析与可视化区块"""
    if 'df' in st.session_state and st.session_state['df'] is not None:
        df = st.session_state['df']
        stopwords = load_stopwords()
        with st.container():
            # 静态词云
            if st.button("分析词云（静态图片）"):
                st.info("正在生成词云，请稍候...")
                if '评论内容' not in df.columns:
                    st.error("没有可用的评论内容，无法生成词云。")
                else:
                    text = ' '.join(df['评论内容'].astype(str))
                    img = generate_wordcloud(text, stopwords)
                    if img is None:
                        st.warning("分词后无有效词语，无法生成词云。")
                    else:
                        st.image(img, caption="评论词云", use_container_width=True)
            # 交互词云
            if st.button("分析词云（可交互）"):
                if '评论内容' not in df.columns:
                    st.error("没有可用的评论内容，无法生成词云。")
                else:
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
        # 评论数量随时间变化曲线
        st.markdown("---")
        st.subheader("📈 评论数量随时间变化曲线（可选区间）")
        if '评论时间' in df.columns:
            df['评论时间'] = pd.to_datetime(df['评论时间'])
            min_date = df['评论时间'].min().date()
            max_date = df['评论时间'].max().date()
            col1, col2, col3 = st.columns([2,2,2])
            with col1:
                start_date = st.date_input("起始日期", min_value=min_date, max_value=max_date, value=min_date, key="start_date")
            with col2:
                end_date = st.date_input("结束日期", min_value=min_date, max_value=max_date, value=max_date, key="end_date")
            with col3:
                freq = st.radio("聚合粒度", ["按天", "按小时"], horizontal=True, key="agg_freq")
            mask = (df['评论时间'].dt.date >= start_date) & (df['评论时间'].dt.date <= end_date)
            df_filtered = df.loc[mask].copy()
            if df_filtered.empty:
                st.warning("所选区间内无评论数据！")
            else:
                import altair as alt
                if freq == "按天":
                    df_filtered['日期'] = df_filtered['评论时间'].dt.date
                    count_df = df_filtered.groupby('日期').size().reset_index(name='评论数')
                    x = count_df['日期'].astype(str)
                else:
                    df_filtered['小时'] = df_filtered['评论时间'].dt.strftime('%Y-%m-%d %H:00')
                    count_df = df_filtered.groupby('小时').size().reset_index(name='评论数')
                    x = count_df['小时']
                chart = alt.Chart(count_df).mark_line(point=True, color="#409EFF").encode(
                    x=alt.X(x.name, title="时间"),
                    y=alt.Y('评论数', title="评论数量"),
                    tooltip=[x.name, '评论数']
                ).properties(
                    width=700,
                    height=350
                ).interactive()
                st.altair_chart(chart, use_container_width=True)
    else:
        st.info("请先爬取评论数据。")

def render_csv_section():
    """本地CSV分析区块"""
    import pandas as pd
    import os
    from analysis.word_cloud import load_stopwords, generate_wordcloud, generate_wordcloud_data
    from streamlit_echarts import st_echarts
    st.markdown("---")
    st.subheader("📂 或直接展示本地 comments.csv 数据")
    if st.button("展示CSV图表", key="show_csv_btn"):
        csv_path = "comments.csv"
        if not os.path.exists(csv_path):
            st.error("当前目录下未找到 comments.csv 文件！")
        else:
            df_csv = pd.read_csv(csv_path)
            st.success(f"已加载 comments.csv，共 {len(df_csv)} 条评论")
            st.dataframe(df_csv)
            # 评论数量随时间变化曲线
            if '评论时间' in df_csv.columns:
                df_csv['评论时间'] = pd.to_datetime(df_csv['评论时间'], errors='coerce')
                min_date = df_csv['评论时间'].min().date()
                max_date = df_csv['评论时间'].max().date()
                col1, col2, col3 = st.columns([2,2,2])
                with col1:
                    start_date = st.date_input("起始日期", min_value=min_date, max_value=max_date, value=min_date, key="csv_start_date")
                with col2:
                    end_date = st.date_input("结束日期", min_value=min_date, max_value=max_date, value=max_date, key="csv_end_date")
                with col3:
                    freq = st.radio("聚合粒度", ["按天", "按星期"], horizontal=True, key="csv_agg_freq")
                mask = (df_csv['评论时间'].dt.date >= start_date) & (df_csv['评论时间'].dt.date <= end_date)
                df_filtered = df_csv.loc[mask].copy()
                if df_filtered.empty:
                    st.warning("所选区间内无评论数据！")
                else:
                    import altair as alt
                    if freq == "按天":
                        df_filtered['日期'] = df_filtered['评论时间'].dt.date
                        count_df = df_filtered.groupby('日期').size().reset_index(name='评论数')
                        x = count_df['日期'].astype(str)
                    else:  # 按星期
                        df_filtered['星期'] = df_filtered['评论时间'].dt.dayofweek
                        week_map = {0: '周一', 1: '周二', 2: '周三', 3: '周四', 4: '周五', 5: '周六', 6: '周日'}
                        df_filtered['星期'] = df_filtered['星期'].map(week_map)
                        count_df = df_filtered.groupby('星期').size().reindex(['周一','周二','周三','周四','周五','周六','周日']).reset_index(name='评论数').fillna(0)
                        x = count_df['星期']
                    chart = alt.Chart(count_df).mark_line(point=True, color="#13c2c2").encode(
                        x=alt.X(x.name, title="时间"),
                        y=alt.Y('评论数', title="评论数量"),
                        tooltip=[x.name, '评论数']
                    ).properties(
                        width=700,
                        height=350
                    ).interactive()
                    st.altair_chart(chart, use_container_width=True)
            # 词云（静态/交互）
            if st.button("生成词云（静态）", key="csv_wc_static"):
                if '评论内容' not in df_csv.columns:
                    st.error("CSV中无评论内容字段，无法生成词云。")
                else:
                    text = ' '.join(df_csv['评论内容'].astype(str))
                    stopwords = load_stopwords()
                    img = generate_wordcloud(text, stopwords)
                    if img is None:
                        st.warning("分词后无有效词语，无法生成词云。")
                    else:
                        st.image(img, caption="评论词云", use_container_width=True)
            if st.button("生成词云（交互）", key="csv_wc_echarts"):
                if '评论内容' not in df_csv.columns:
                    st.error("CSV中无评论内容字段，无法生成词云。")
                else:
                    text = ' '.join(df_csv['评论内容'].astype(str))
                    stopwords = load_stopwords()
                    data = generate_wordcloud_data(text, stopwords)
                    if not data:
                        st.warning("分词后无有效词语，无法生成词云。")
                    else:
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
