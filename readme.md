# 🎥 B站评论爬取与分析系统

一个功能完整的B站评论数据采集、分析和可视化系统，支持在线爬取、本地数据分析、词云生成、情感分析和趋势分析等功能。

## ✨ 主要功能

- 🚀 **在线评论爬取**：输入BV号即可爬取B站视频评论数据
- 📊 **数据可视化**：生成静态和交互式词云图
- 📈 **趋势分析**：按天/周统计评论数量变化
- 🎭 **情感分析**：基于SnowNLP的中文情感分析
- 💾 **本地数据分析**：支持本地CSV文件分析
- 🎨 **美观界面**：基于Streamlit的现代化Web界面

## 🏗️ 项目结构

```shell
-ikun/
├── README.md                # 项目说明文档
├── requirements.txt         # Python依赖包列表
├── .env                    # 环境变量配置文件
├── main.py                 # 命令行爬虫主程序
├── stopwords.txt           # 中文停用词表
├── report/                 # Web应用目录
│   └── app.py             # Streamlit Web界面
├── analysis/               # 数据分析模块
│   └── word_cloud.py      # 词云生成和文本分析
└── data/                   # 数据存储目录
    ├── comments.csv        # 评论数据
    ├── wordcloud.png       # 生成的词云图片
    └── *.csv              # 其他数据文件
```

## 🛠️ 环境要求

- Python 3.7+
- 有效的B站Cookie（用于数据爬取）

## 📦 安装指南

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd -ikun
```

### 2. 创建虚拟环境
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
在项目根目录创建 `.env` 文件：
```env
# B站Cookie（必填，用于爬取评论）
BILI_COOKIE=你的B站Cookie

# 默认BV号（可选）
BILI_BV=BV1qC4y1E7oU
```

#### 如何获取B站Cookie：
1. 打开浏览器，登录B站
2. 按F12打开开发者工具
3. 切换到Network标签
4. 刷新页面，找到任意请求
5. 在Request Headers中复制Cookie值

## 🚀 使用方法

### 方式一：Web界面（推荐）

启动Streamlit应用：
```bash
streamlit run report/app.py
```

浏览器会自动打开 `http://localhost:8501`，你将看到两个主要功能：

#### 📡 在线爬取与分析
1. 输入B站视频BV号（如：BV1qC4y1E7oU）
2. 点击"开始爬取"按钮
3. 等待爬取完成，查看数据表格
4. 使用以下分析功能：
   - **静态词云**：生成传统词云图片
   - **交互词云**：生成可交互的词云图表
   - **趋势分析**：查看评论数量随时间变化
   - **情感分析**：分析评论情感倾向

#### 📁 本地数据分析
1. 选择data目录下的CSV文件
2. 查看数据预览
3. 使用相同的分析工具分析本地数据

### 方式二：命令行工具

运行命令行爬虫：
```bash
python main.py
```

按提示输入BV号，程序会自动爬取评论并保存到 `data/comments.csv`

## 📊 功能详解

### 词云分析
- **静态词云**：使用WordCloud库生成传统词云图片
- **交互词云**：基于ECharts的可交互词云，支持缩放、悬停效果
- **智能过滤**：自动过滤停用词和无意义词汇

### 趋势分析
- **时间聚合**：支持按天或按自然周统计
- **日期筛选**：可选择分析的时间区间
- **交互图表**：基于Altair的交互式折线图

### 情感分析
- **中文适配**：基于SnowNLP的中文情感分析引擎
- **三分类**：正面、负面、中性情感分类
- **可视化**：饼图展示情感分布

## ⚙️ 配置说明

### 停用词配置
编辑 `stopwords.txt` 文件可以自定义停用词列表，一行一个词。

### 爬虫参数调整
在 `main.py` 中可以调整以下参数：
- `mode`：评论排序方式（2=最新，3=热门）
- `is_second`：是否爬取二级评论
- 请求间隔时间等

### 界面样式
在 `report/app.py` 中的CSS部分可以自定义界面样式。

## 🔧 故障排除

### 常见问题

1. **Cookie失效**
   - 现象：爬取失败或返回空数据
   - 解决：重新获取B站Cookie并更新.env文件

2. **依赖安装失败**
   - 现象：pip install报错
   - 解决：尝试使用国内镜像源
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
   ```

3. **词云图片不显示**
   - 现象：词云分析后无图片
   - 解决：检查是否安装了中文字体，确保data目录可写

4. **Streamlit启动失败**
   - 现象：streamlit命令不存在
   - 解决：确认虚拟环境已激活且streamlit已安装

### 调试模式
如果遇到问题，可以设置环境变量启用调试：
```bash
export STREAMLIT_SERVER_HEADLESS=false
export STREAMLIT_LOGGER_LEVEL=debug
```

## 📝 数据格式

爬取的CSV文件包含以下字段：
- 序号、上级评论ID、评论ID
- 用户ID、用户名、用户等级、性别
- 评论内容、评论时间
- 回复数、点赞数、个性签名
- IP属地、是否大会员、头像URL

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本项目
2. 创建功能分支：`git checkout -b feature/新功能`
3. 提交更改：`git commit -am '添加新功能'`
4. 推送分支：`git push origin feature/新功能`
5. 提交Pull Request

## 📄 许可证

本项目仅供学习和研究使用，请遵守相关网站的robots.txt和使用条款。

## ⚠️ 免责声明

- 本工具仅用于学术研究和个人学习
- 请遵守B站相关条款，避免过频繁请求
- 数据仅供分析使用，请勿用于商业用途