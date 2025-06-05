"""
B站评论爬虫模块
"""
import requests
import time
import hashlib
from datetime import datetime
from config.settings import get_request_headers, BILIBILI_API_SETTINGS

def get_avid_from_bv(bv):
    """通过BV号获取视频的AV号"""
    url = f"{BILIBILI_API_SETTINGS['video_info_url']}?bvid={bv}"
    response = requests.get(url, headers=get_request_headers())
    data = response.json()
    if data.get('code', 0) != 0:
        raise Exception(f"获取avid失败: {data.get('message', '未知错误')}")
    return data['data']['aid']

def md5(code):
    """MD5加密"""
    return hashlib.md5(code.encode('utf-8')).hexdigest()

def fetch_comments(bv, max_pages=1000, delay=0.5):
    """爬取B站评论，返回评论列表"""
    aid = get_avid_from_bv(bv)
    pagination_str = ''
    comments = []
    for page in range(max_pages):
        wts = int(time.time())
        offset = f'"offset":"{pagination_str}"' if pagination_str else '"offset":""'
        payload = f"mode=2&oid={aid}&pagination_str=%7B{offset}%7D&plat=1&type=1&web_location=1315875&wts={wts}"
        w_rid = md5(payload + BILIBILI_API_SETTINGS['comment_api_salt'])
        url = f"{BILIBILI_API_SETTINGS['comment_api_url']}?oid={aid}&type=1&mode=2&pagination_str=%7B{offset}%7D&plat=1&web_location=1315875&w_rid={w_rid}&wts={wts}"
        res = requests.get(url, headers=get_request_headers()).json()
        replies = res.get("data", {}).get("replies", [])
        if not replies:
            break
        for r in replies:
            comments.append({
                "用户名": r["member"]["uname"],
                "评论内容": r["content"]["message"],
                "点赞数": r["like"],
                "评论时间": datetime.fromtimestamp(r["ctime"]).strftime('%Y-%m-%d %H:%M:%S'),
            })
        pagination_str = res['data']['cursor']['pagination_reply'].get('next_offset', 0)
        if not pagination_str:
            break
        time.sleep(delay)
    return comments
