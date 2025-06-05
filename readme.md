# 🎥 B站评论爬取分析工具

一个功能全面的B站评论爬取、分析和可视化工具，支持评论数据获取、词云生成、数据分析等功能。

## ✨ 功能特性

- 🚀 **评论爬取**: 支持通过BV号爬取B站视频评论
- 📊 **数据分析**: 评论数量趋势分析、时间分布统计
- ☁️ **词云生成**: 静态词云和交互式词云展示
- 🎨 **美观界面**: 基于Streamlit的现代化Web界面
- 📁 **数据管理**: CSV格式数据保存和管理
- 🔧 **模块化设计**: 清晰的项目结构，易于维护和扩展

## 🏗️ 项目结构

```
-ikun/
├── run.py                    # 🚀 主启动文件
├── main.py                   # 🧩 原始爬虫脚本
├── requirements.txt          # 📦 依赖包列表
├── .env                      # 🔑 环境变量配置
├── config/                   # ⚙️ 配置文件
│   ├── __init__.py
│   ├── settings.py          # 全局配置
│   └── stopwords.txt        # 停用词表
├── crawler/                  # 🕷️ 爬虫模块
│   ├── __init__.py
│   └── bilibili_crawler.py  # B站评论爬虫
├── analysis/                 # 📊 分析模块
│   ├── __init__.py
│   └── word_cloud.py        # 词云分析
├── report/                   # 🖼️ 报告展示模块
│   ├── __init__.py
│   ├── app.py               # Streamlit主应用
│   ├── views.py             # 页面渲染
│   ├── logic.py             # 业务逻辑
│   └── utils.py             # 工具函数
├── utils/                    # 🛠️ 通用工具
│   └── __init__.py
└── data/                     # 📁 数据存储
    ├── comments.csv         # 评论数据
    ├── wordcloud.png        # 词云图片
    └── *.csv                # 其他数据文件
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd -ikun

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件并配置B站Cookie：

```env
BILI_COOKIE=your_bilibili_cookie_here
```

### 3. 运行应用

#### 方式一：统一启动器（推荐）

```bash
python run.py
```

然后选择对应功能：
- 🚀 启动Web界面 (Streamlit)
- 📡 命令行爬取评论
- 📊 批量词云分析
- 🔧 系统检查

#### 方式二：直接启动Web界面

```bash
streamlit run report/app.py
```

#### 方式三：命令行爬虫

```bash
python crawler/bilibili_crawler.py
```

## 💡 使用方法

### Web界面使用

1. **评论爬取**
   - 输入BV号（如：BV1234567890）
   - 点击"开始爬取"
   - 等待爬取完成，支持下载CSV文件

2. **数据分析**
   - 选择已爬取的数据文件
   - 查看词云（静态/交互式）
   - 分析评论数量趋势

3. **本地数据查看**
   - 浏览本地CSV文件
   - 查看数据统计信息
   - 进行数据分析

### 命令行使用

```bash
# 爬取指定视频评论
python crawler/bilibili_crawler.py

# 分析指定CSV文件
python analysis/word_cloud.py
```

## 📊 功能模块详解

### 🕷️ 爬虫模块 (crawler/)

- **bilibili_crawler.py**: B站评论爬虫主类
  - 支持分页爬取
  - 自动处理API签名
  - 数据格式化和清洗
  - 防反爬延时机制

### 📊 分析模块 (analysis/)

- **word_cloud.py**: 词云分析功能
  - 中文分词（jieba）
  - 停用词过滤
  - 静态词云生成
  - 交互式词云数据

### 🖼️ 报告模块 (report/)

- **app.py**: Streamlit主应用
- **views.py**: 页面渲染逻辑
- **logic.py**: 业务逻辑处理
- **utils.py**: 报告工具函数

### ⚙️ 配置模块 (config/)

- **settings.py**: 全局配置管理
- **stopwords.txt**: 中文停用词表

## 🎨 界面特色

- 🌈 现代化渐变设计
- 📱 响应式布局
- 🎯 直观的功能导航
- 📊 丰富的数据可视化
- 🎪 交互式图表展示

## 🔧 技术栈

- **后端**: Python 3.7+
- **Web框架**: Streamlit
- **数据处理**: Pandas
- **网络请求**: Requests
- **词云生成**: WordCloud
- **中文分词**: jieba
- **图表可视化**: Altair, streamlit-echarts
- **环境管理**: python-dotenv

## 📋 依赖包

```txt
streamlit>=1.28.0
pandas>=1.5.0
requests>=2.28.0
wordcloud>=1.9.0
jieba>=0.42.1
streamlit-echarts>=0.4.0
altair>=4.2.0
python-dotenv>=0.19.0
```

## ⚠️ 注意事项

1. **Cookie配置**: 需要有效的B站Cookie才能正常爬取数据
2. **访问频率**: 内置了延时机制，避免过于频繁的请求
3. **数据合规**: 请遵守B站的使用条款和相关法律法规
4. **字体依赖**: 词云生成需要中文字体支持（msyh.ttc）

## 🚀 部署说明

### 本地部署
直接运行 `python run.py` 即可

### 服务器部署
```bash
# 使用nohup后台运行
nohup streamlit run report/app.py --server.port 8501 &

# 或使用systemd服务
sudo systemctl start bilibili-analyzer
```

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/bilibili-comment-analyzer/issues)

---

⭐ 如果这个项目对你有帮助，请给个 Star！
