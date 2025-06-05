"""
报告模块业务逻辑
"""
import requests
import time
import hashlib
from datetime import datetime
import os
from config.settings import get_headers, BILIBILI_API

def get_avid_from_bv(bv):
    """通过BV号获取视频的AV号"""
    url = f"{BILIBILI_API['video_info']}?bvid={bv}"
    response = requests.get(url, headers=get_headers())
    data = response.json()
    if data.get('code', 0) != 0:
        raise Exception(f"获取avid失败: {data.get('message', '未知错误')}")
    return data['data']['aid']

def md5(code):
    """MD5加密"""
    return hashlib.md5(code.encode('utf-8')).hexdigest()

def fetch_comments(bv, max_pages=1000):
    """获取评论数据"""
    aid = get_avid_from_bv(bv)
    comments = []
    pagination_str = ''
    
    for page in range(max_pages):
        # 构造请求参数
        mode = 2  # 最新评论
        plat = 1
        type = 1
        web_location = 1315875
        
        params = f"mode={mode}&oid={aid}&plat={plat}&type={type}&web_location={web_location}"
        if pagination_str:
            params += f"&pagination_str={pagination_str}"
        
        # 生成签名
        wts = str(int(time.time()))
        w_rid = md5(params + wts + "ea1db124af3c7062474693fa704f4ff8")
        
        url = f"{BILIBILI_API['comment_api']}?{params}&wts={wts}&w_rid={w_rid}"
        
        try:
            response = requests.get(url, headers=get_headers())
            data = response.json()
            
            if data.get('code') != 0:
                print(f"API错误: {data.get('message', '未知错误')}")
                break
            
            replies = data.get('data', {}).get('replies', [])
            if not replies:
                break
            
            # 解析评论数据
            for reply in replies:
                comment = {
                    'rpid': reply.get('rpid', ''),
                    'content': reply.get('content', {}).get('message', ''),
                    'ctime': reply.get('ctime', 0),
                    'like': reply.get('like', 0),
                    'member_uname': reply.get('member', {}).get('uname', ''),
                    'member_mid': reply.get('member', {}).get('mid', ''),
                    'member_level': reply.get('member', {}).get('level_info', {}).get('current_level', 0),
                    'reply_count': reply.get('rcount', 0)
                }
                
                # 格式化时间
                if comment['ctime']:
                    comment['formatted_time'] = datetime.fromtimestamp(comment['ctime']).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    comment['formatted_time'] = ''
                
                comments.append(comment)
            
            # 检查是否有下一页
            cursor = data.get('data', {}).get('cursor', {})
            if cursor.get('is_end', True):
                break
            
            pagination_str = cursor.get('pagination_reply', {}).get('next_offset', '')
            if not pagination_str:
                break
            
            time.sleep(1)  # 延时避免被封
            
        except Exception as e:
            print(f"请求失败: {e}")
            break
    
    return comments
