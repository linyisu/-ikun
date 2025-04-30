from DrissionPage import Chromium
import pickle

with open("cookies/zhihu_cookies.pkl", "rb") as f:
    cookies = pickle.load(f)

browser = Chromium()
browser.set.cookies(cookies)

tab = browser.latest_tab

tab.get("https://www.zhihu.com/search?type=content&q=%E8%94%A1%E5%BE%90%E5%9D%A4")

for _ in range(3):
    tab.scroll.to_bottom()
    tab.wait(2)

list_eles = tab.eles('@class=List-item')

for list_ele in list_eles:
    title_ele = list_ele.ele('@class=ContentItem-title')
    if title_ele === 
    print(title_ele)
    # link = list_ele.ele('@class=ContentItem