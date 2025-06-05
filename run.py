#!/usr/bin/env python3
"""
B站评论爬取分析工具主启动文件
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """主函数"""
    print("🎥 欢迎使用B站评论爬取分析工具")
    print("=" * 50)
    
    while True:
        print("\n请选择功能:")
        print("1. 🚀 启动Web界面 (Streamlit)")
        print("2. 📡 命令行爬取评论")
        print("3. 📊 批量词云分析")
        print("4. 🔧 系统检查")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-4): ").strip()
        
        if choice == "1":
            start_web_app()
        elif choice == "2":
            start_crawler()
        elif choice == "3":
            batch_analysis()
        elif choice == "4":
            system_check()
        elif choice == "0":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请重新输入")

def start_web_app():
    """启动Streamlit Web应用"""
    print("🚀 正在启动Web界面...")
    os.system(f"streamlit run {project_root}/report/app.py")

def start_crawler():
    """启动命令行爬虫"""
    print("📡 启动命令行爬虫")
    from crawler.bilibili_crawler import main as crawler_main
    crawler_main()

def batch_analysis():
    """批量词云分析"""
    print("📊 批量词云分析")
    from analysis.word_cloud import analyze_comments_from_csv
    from config.settings import DATA_DIR
    
    # 查找CSV文件
    csv_files = list(DATA_DIR.glob("*.csv"))
    if not csv_files:
        print("❌ 未找到CSV文件")
        return
    
    print(f"📁 找到 {len(csv_files)} 个CSV文件:")
    for i, file in enumerate(csv_files, 1):
        print(f"  {i}. {file.name}")
    
    try:
        choice = int(input("\n选择要分析的文件 (输入序号): "))
        if 1 <= choice <= len(csv_files):
            selected_file = csv_files[choice - 1]
            print(f"🔍 正在分析: {selected_file.name}")
            
            result = analyze_comments_from_csv(selected_file)
            if result[0] is not None:
                print("✅ 词云分析完成！")
                print(f"📊 词云图片已保存到: {DATA_DIR}/wordcloud.png")
            else:
                print("❌ 词云分析失败")
        else:
            print("❌ 无效选择")
    except ValueError:
        print("❌ 请输入有效数字")

def system_check():
    """系统检查"""
    print("🔧 系统检查")
    print("-" * 30)
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    
    # 检查必要的包
    required_packages = [
        'streamlit', 'pandas', 'requests', 'wordcloud', 
        'jieba', 'streamlit-echarts', 'altair', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}: 已安装")
        except ImportError:
            print(f"❌ {package}: 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  缺少以下包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
    
    # 检查环境变量
    print(f"\n🔑 环境变量检查:")
    bili_cookie = os.getenv('BILI_COOKIE')
    if bili_cookie:
        print("✅ BILI_COOKIE: 已配置")
    else:
        print("❌ BILI_COOKIE: 未配置 (需要在.env文件中设置)")
    
    # 检查目录结构
    print(f"\n📁 目录结构检查:")
    required_dirs = ['data', 'config', 'analysis', 'report', 'crawler']
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/: 存在")
        else:
            print(f"❌ {dir_name}/: 不存在")
    
    print("\n🏁 检查完成")

if __name__ == "__main__":
    main()
