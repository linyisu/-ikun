import csv
import hashlib
import json
import urllib
import time
import requests
import re
import pandas as pd
import os
from dotenv import load_dotenv

def getHeaders():
    load_dotenv()
    cookie = os.getenv('BILI_COOKIE')
    if not cookie:
        raise ValueError('BILI_COOKIE not found in .env file')
    return {"cookie": cookie, "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"}

def getInfo(BV, link):
    resp = requests.get(link, headers=getHeaders())
    oid = re.findall(f'"aid":(.*?),"bvid":"{BV}"', resp.text)[0]
    title = re.findall(r'<title data-vue-meta="true">(.*?)</title>', resp.text)[0]
    return oid, title

def getComments(oid):
    params = {
        'oid': oid,
        'type': type,
        'sort': 0, # 0 按时间排序，1 按热度排序， 2 按点赞数排序
    }

    response = requests.get(url=f"https://api.bilibili.com/x/v2/reply", params=params)
    # if response.status_code != 200:
    #     raise Exception(f"Failed to fetch comments: {response.status_code}")
    # data = response.json()
    # print(data)
    # if 'data' not in data or 'replies' not in data['data']:
    #     raise Exception("No comments found or invalid response format")
    # return data['data']['replies']

# def start(bv, oid, pageID, count, csv_writer, cnt, total_count):
#     mode, plat, type = 2, 1, 1
#     wts = time.time()
#     if pageID != '':
#         pagination_str = '{"offset":"{\\\"type\\\":3,\\\"direction\\\":1,\\\"Data\\\":{\\\"cursor\\\":%d}}"}' % pageID
#     else:
#         pagination_str = '{"offset":""}'
#     md5_str = 'ea1db124af3c7062474693fa704f4ff8'
#     code = f"mode={mode}&oid={oid}&pagination_str={urllib.parse.quote(pagination_str)}&plat={plat}&seek_rpid=&type={type}&web_location=1315875&wts={wts}{md5_str}"
#     w_rid = hashlib.md5(code.encode('utf-8')).hexdigest()

#     url = f"https://api.bilibili.com/x/v2/reply/wbi/main?oid={oid}&type={type}&mode={mode}&pagination_str={urllib.parse.quote(pagination_str, safe=':')}&plat=1&seek_rpid=&web_location=1315875&w_rid={w_rid}&wts={wts}"
#     comment = requests.get(url, headers=getHeaders()).json()

#     current_count = 0
#     for reply in comment['data']['replies']:
#         count += 1
#         uid, name, level, sex = reply["mid"], reply["member"]["uname"], reply["member"]["level_info"]["current_level"], \
#         reply["member"]["sex"]
#         context, reply_time = reply["content"]["message"], pd.to_datetime(reply["ctime"], unit='s')

#         try:
#             rereply = int(re.findall(r'\d+', reply["reply_control"]["sub_reply_entry_text"])[0])
#         except KeyError:
#             rereply = 0

#         like, sign = reply['like'], reply.get('member', {}).get('sign', '')
#         csv_writer.writerow([count, uid, name, level, sex, context, reply_time, rereply, like, sign])

#         current_count += 1
#         total_count += 1

#     print(f"累计爬取了 {total_count} 条评论。")

#     if comment['data']['cursor']['next']:
#         if cnt > 0:
#             time.sleep(0.5)
#             start(bv, oid, comment['data']['cursor']['next'], count, csv_writer, cnt - 1, total_count)
#     else:
#         print(f"评论爬取完成！总共爬取{total_count}条。")