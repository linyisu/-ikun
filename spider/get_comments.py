
import csv
import hashlib
import json
import urllib
import time
import requests
import re
import pandas as pd

def getHeaders():
    with open('bili_cookie.txt', 'r') as f:
        return {"cookie": f.read(), "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"}

def getInfo(BV, link):
    resp = requests.get(link, headers=getHeaders())
    oid = re.findall(f'"aid":(.*?),"bvid":"{BV}"', resp.text)[0]
    title = re.findall(r'<title data-vue-meta="true">(.*?)</title>', resp.text)[0]
    return oid, title

def clean_title(title):
    # 替换 Windows 文件名不允许的字符
    return re.sub(r'[\\/:*?"<>|]', '_', title)

def start(bv, oid, pageID, count, csv_writer, cnt, total_count):
    mode, plat, type = 2, 1, 1
    wts = time.time()
    if pageID != '':
        pagination_str = '{"offset":"{\\\"type\\\":3,\\\"direction\\\":1,\\\"Data\\\":{\\\"cursor\\\":%d}}"}' % pageID
    else:
        pagination_str = '{"offset":""}'
    md5_str = 'ea1db124af3c7062474693fa704f4ff8'
    code = f"mode={mode}&oid={oid}&pagination_str={urllib.parse.quote(pagination_str)}&plat={plat}&seek_rpid=&type={type}&web_location=1315875&wts={wts}{md5_str}"
    w_rid = hashlib.md5(code.encode('utf-8')).hexdigest()

    url = f"https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type={type}&mode={mode}&pagination_str={urllib.parse.quote(pagination_str, safe=':')}&plat=1&seek_rpid=&web_location=1315875&w_rid={w_rid}&wts={wts}"
    comment = requests.get(url, headers=getHeaders()).json()

    current_count = 0
    for reply in comment['data']['replies']:
        count += 1
        uid, name, level, sex = reply["mid"], reply["member"]["uname"], reply["member"]["level_info"]["current_level"], \
        reply["member"]["sex"]
        context, reply_time = reply["content"]["message"], pd.to_datetime(reply["ctime"], unit='s')

        try:
            rereply = int(re.findall(r'\d+', reply["reply_control"]["sub_reply_entry_text"])[0])
        except KeyError:
            rereply = 0

        like, sign = reply['like'], reply.get('member', {}).get('sign', '')
        csv_writer.writerow([count, uid, name, level, sex, context, reply_time, rereply, like, sign])

        current_count += 1
        total_count += 1

    print(f"累计爬取了 {total_count} 条评论。")

    if comment['data']['cursor']['next']:
        if cnt > 0:
            time.sleep(0.5)
            start(bv, oid, comment['data']['cursor']['next'], count, csv_writer, cnt - 1, total_count)
    else:
        print(f"评论爬取完成！总共爬取{total_count}条。")

if __name__ == '__main__':
    BV = input()
    link = f'https://www.bilibili.com/video/{BV}'
    oid, title = getInfo(BV, link)
    safe_title = clean_title(title[:-14])
    print(safe_title)

    needCnt = 1000
    total_count = 0

    with open(f'{safe_title}_评论.csv', mode='w', newline='', encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['序号', '用户ID', '用户名', '用户等级', '性别', '评论内容', '评论时间', '回复数', '点赞数', '个性签名'])
        start(BV, oid, '', 0, csv_writer, needCnt, total_count)