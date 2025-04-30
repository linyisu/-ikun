import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
import json


class DriverSingleton:
    _driver_instance = None  # 存储单例实例

    def __new__(cls):
        """确保只有一个 WebDriver 实例"""
        if cls._driver_instance is None:
            print("Initializing WebDriver...")
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--start-maximized")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            options.add_argument("--lang=en-US")  # 设置浏览器语言为英语
            # 更改时区等信息以减少指纹特征
            options.add_argument("--timezone=America/New_York")  # 示例时区
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-usb")
            cls._driver_instance = webdriver.Chrome(options=options)  # 创建实例
            cls._driver_instance.get(f'https://www.zhihu.com')
            with open('cookies/zhihu_cookies.pkl', 'rb') as f:
                cookies = pickle.load(f)
            for cookie in cookies:
                cls._driver_instance.add_cookie(cookie)
            cls._driver_instance.refresh()
        return cls._driver_instance


# 自动滚动知乎搜索结果页，收集问题/文章链接
def get_search_links(keyword, scroll_times=10):
    driver = DriverSingleton()
    driver.get(f'https://www.zhihu.com/search?type=content&q={keyword}')
    time.sleep(3)

    for _ in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

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
    driver = DriverSingleton()
    driver.get(url)
    time.sleep(3)

    element = driver.find_element(By.XPATH, "//a[contains(@class, 'ViewAll-QuestionMainAction') and contains(text(), '查看全部')]")
    driver.execute_script("arguments[0].click();", element)
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
    # 滚到底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 等待页面加载（可调整）

        # 获取新高度
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 如果高度没变，就说明到底了
        if new_height == last_height:
            break

        last_height = new_height

    time.sleep(2)  # 等待加载完成

    comments = driver.find_elements(By.XPATH, "//p[@data-pid]")  # 根据data-pid定位评论内容
    # time.sleep(50)
    return comments

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
            if not answers:
                print("没有找到回答，跳过")
                continue
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

# get_answers_from_question("https://www.zhihu.com/question/1894320470754562551/answer/1896939277058824027")