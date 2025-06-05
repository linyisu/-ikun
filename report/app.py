"""
B站评论分析 Streamlit 应用
"""
import streamlit as st
from dotenv import load_dotenv
import sys
import os
from pathlib import Path

# 将项目根目录添加到sys.path
# 定位到 d:\Projects\Python\-ikun\report\app.py
# Path(__file__) -> d:\Projects\Python\-ikun\report\app.py
# .parent -> d:\Projects\Python\-ikun\report
# .parent -> d:\Projects\Python\-ikun
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from report.views import render_crawler_section, render_analysis_section, render_csv_section

# 加载环境变量
load_dotenv(dotenv_path=project_root / '.env') # 指定.env文件路径

# ========== 页面样式美化 ==========
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
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stTitle {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem !important;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .stSubheader {
        color: #A23B72;
        border-bottom: 2px solid #F18F01;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #4ECDC4;
        padding: 0.5rem 1rem;
    }
    .stSelectbox > div > div > select {
        border-radius: 15px;
        border: 2px solid #FF6B6B;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    """主函数"""
    st.title("🎥 B站评论爬取分析器")
    
    # 侧边栏导航
    st.sidebar.title("🧭 功能导航")
    page = st.sidebar.selectbox(
        "选择功能",
        ["📡 评论爬取", "📊 数据分析", "📁 本地数据查看"]
    )
    
    # 根据选择渲染不同页面
    if page == "📡 评论爬取":
        render_crawler_section()
    elif page == "📊 数据分析":
        render_analysis_section()
    elif page == "📁 本地数据查看":
        render_csv_section()
    
    # 页脚信息
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        🌟 B站评论分析工具 | 支持评论爬取、词云分析、数据可视化
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
