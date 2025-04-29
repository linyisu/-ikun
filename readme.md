## 项目结构

```shell
ikun_insight/
├── README.md
├── requirements.txt
├── spider/              # 👀 数据爬虫（bilibili、微博、知乎）
│   ├── bilibili_spider.py
│   ├── weibo_spider.py
│   └── utils.py
├── data/                # 📁 爬下来的原始数据（json/csv）
├── analysis/            # 📊 数据分析（情绪分析、热度趋势）
│   ├── sentiment_analysis.py
│   ├── trend_analysis.py
│   └── wordcloud_generator.py
├── report/              # 🖼 输出结果（图表、词云等）
│   ├── charts/
│   ├── wordclouds/
│   └── summary.md
├── main.py              # 🧩 项目主入口，串联爬虫和分析
└── .gitignore

```