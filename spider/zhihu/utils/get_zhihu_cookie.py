import pickle
from selenium import webdriver
import os
import time

path = "cookies/zhihu_cookies.pkl"

def save_cookies_to_pkl():
    driver = webdriver.Chrome()
    driver.get("https://www.zhihu.com")
    print("请在 60 秒内扫码登录知乎...")

    #TODO 这里可以使用 WebDriverWait 等待登录完成
    
    time.sleep(10)  # 给你时间扫码登录

    cookies = driver.get_cookies()
    driver.quit()

    # 保存 cookies 到 pkl 文件
    with open(path, "wb") as f:
        pickle.dump(cookies, f)
    
    print("✅ Cookies 已保存到 zhihu_cookies.pkl 文件！")

save_cookies_to_pkl()
