from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
import json

# 启动 Selenium 浏览器
def start_browser():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 无头模式

    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver

# 自动滚动知乎搜索结果页，收集问题/文章链接
def get_search_links(keyword, scroll_times=10):
    driver = start_browser()
    driver.get(f'https://www.zhihu.com/search?type=content&q={keyword}')
    time.sleep(3)

    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/question/') or href.startswith('/zvideo/'):
            full_url = 'https://www.zhihu.com' + href
            if full_url not in links:
                links.append(full_url)
    return links

# 获取问题页的所有回答（只展示前几条即可）
def get_answers_from_question(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.zhihu.com',
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return []

    soup = BeautifulSoup(res.text, 'html.parser')
    answers = []

    for item in soup.select('.RichContent-inner'):
        text = item.get_text(strip=True)
        if text:
            answers.append(text)
    
    return answers

# 主程序：整合流程
def crawl_zhihu_about(keyword):
    print("开始爬取知乎关于：", keyword)
    links = get_search_links(keyword)
    print(f"共找到 {len(links)} 个相关页面链接")

    all_answers = []

    for i, link in enumerate(links[:20]):  # 只爬前20个链接，可扩展
        print(f"[{i+1}/{len(links)}] 正在抓取：{link}")
        try:
            answers = get_answers_from_question(link)
            for a in answers:
                all_answers.append({"url": link, "text": a})
            time.sleep(1)
        except Exception as e:
            print("抓取失败：", e)
    
    with open(f'zhihu_{keyword}_answers.json', 'w', encoding='utf-8') as f:
        json.dump(all_answers, f, ensure_ascii=False, indent=2)
    print("✅ 完成，共保存回答数：", len(all_answers))

# 运行爬虫
crawl_zhihu_about("蔡徐坤")
