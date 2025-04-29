from selenium import webdriver
import pickle
import time

path = "cookies/zhihu_cookies.pkl"


def load_cookies_and_login():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--lang=en-US")  # 设置浏览器语言为英语
    # 更改时区等信息以减少指纹特征
    options.add_argument("--timezone=America/New_York")  # 示例时区
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.zhihu.com")
    
    # 加载保存的 Cookies
    with open(path, "rb") as f:
        cookies = pickle.load(f)

    # 添加 Cookies 到浏览器
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    # 刷新页面，确保 Cookies 生效
    driver.refresh()
    time.sleep(3)
    
    print("✅ Cookies 已加载并登录成功！")
    time.sleep(60)

load_cookies_and_login()
