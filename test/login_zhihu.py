from selenium import webdriver
import pickle
import time

def load_cookies_and_login():
    driver = webdriver.Chrome()
    driver.get("https://www.zhihu.com")
    
    # 加载保存的 Cookies
    with open("zhihu_cookies.pkl", "rb") as f:
        cookies = pickle.load(f)

    print(cookies)
    # 添加 Cookies 到浏览器
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    # 刷新页面，确保 Cookies 生效
    driver.refresh()
    time.sleep(3)
    
    print("✅ Cookies 已加载并登录成功！")
    
    # 继续进行后续操作
    driver.get("https://www.zhihu.com/")  # 示例访问某个问题页面
    time.sleep(5)  # 等待页面加载
    driver.quit()

load_cookies_and_login()
