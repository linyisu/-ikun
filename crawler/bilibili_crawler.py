"""
B站评论爬虫模块
"""
import re
import requests
import json
from urllib.parse import quote
import pandas as pd
import hashlib
import urllib
import time
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from config.settings import get_headers, BILIBILI_API, DATA_DIR

load_dotenv()

class BilibiliCommentCrawler:
    """B站评论爬虫类"""
    
    def __init__(self):
        self.headers = get_headers()
        self.comments_data = []
    
    def get_avid_from_bv(self, bv):
        """通过BV号获取视频的AV号"""
        url = f"{BILIBILI_API['video_info']}?bvid={bv}"
        response = requests.get(url, headers=self.headers)
        try:
            data = response.json()
        except Exception as e:
            print('接口返回内容不是合法JSON，可能是Cookie失效或被风控。返回内容如下：')
            print(response.text)
            raise e
        
        if data.get('code', 0) != 0:
            print(f"接口返回错误: {data.get('message', '未知错误')}")
            raise Exception('获取avid失败')
        return data['data']['aid']
    
    def md5(self, code):
        """MD5加密"""
        MD5 = hashlib.md5()
        MD5.update(code.encode('utf-8'))
        return MD5.hexdigest()
    
    def fetch_page_comments(self, bv, oid, page_id, is_second=False):
        """获取单页评论"""
        mode = 2  # 2为最新评论，3为热门评论
        plat = 1
        type = 1  
        web_location = 1315875
        
        pagination_str = f"&pagination_str={page_id}" if page_id else ""
        
        # 构造参数
        params = f"mode={mode}&oid={oid}&plat={plat}&type={type}&web_location={web_location}{pagination_str}"
        
        # 获取wts和w_rid
        wts = str(int(time.time()))
        w_rid = self.md5(params + wts + "ea1db124af3c7062474693fa704f4ff8")
        
        # 完整URL
        url = f"{BILIBILI_API['comment_api']}?{params}&wts={wts}&w_rid={w_rid}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            if data.get('code') == 0:
                return data.get('data', {})
            else:
                print(f"API返回错误: {data.get('message', '未知错误')}")
                return None
                
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def parse_comments(self, data):
        """解析评论数据"""
        comments = []
        replies = data.get('replies', [])
        
        for reply in replies:
            comment_info = {
                'rpid': reply.get('rpid', ''),
                'content': reply.get('content', {}).get('message', ''),
                'ctime': reply.get('ctime', 0),
                'like': reply.get('like', 0),
                'member_uname': reply.get('member', {}).get('uname', ''),
                'member_mid': reply.get('member', {}).get('mid', ''),
                'member_level': reply.get('member', {}).get('level_info', {}).get('current_level', 0),
                'member_avatar': reply.get('member', {}).get('avatar', ''),
                'reply_count': reply.get('rcount', 0)
            }
            
            # 时间格式化
            if comment_info['ctime']:
                comment_info['formatted_time'] = datetime.fromtimestamp(comment_info['ctime']).strftime('%Y-%m-%d %H:%M:%S')
            else:
                comment_info['formatted_time'] = ''
            
            comments.append(comment_info)
        
        return comments
    
    def crawl_comments(self, bv, max_pages=1000):
        """爬取评论主函数"""
        print(f"开始爬取BV号: {bv}")
        
        try:
            # 获取视频AV号
            oid = self.get_avid_from_bv(bv)
            print(f"获取到AV号: {oid}")
            
            all_comments = []
            page_id = ""
            
            for page_num in range(1, max_pages + 1):
                print(f"正在爬取第 {page_num} 页...")
                
                # 获取当前页数据
                data = self.fetch_page_comments(bv, oid, page_id, page_num > 1)
                
                if not data:
                    print("获取数据失败，停止爬取")
                    break
                
                # 解析评论
                comments = self.parse_comments(data)
                if not comments:
                    print("没有更多评论了")
                    break
                
                all_comments.extend(comments)
                print(f"第 {page_num} 页获取到 {len(comments)} 条评论")
                
                # 获取下一页标识
                cursor = data.get('cursor')
                if not cursor or not cursor.get('is_end', True):
                    print("已到最后一页")
                    break
                
                page_id = cursor.get('pagination_reply', {}).get('next_offset', '')
                if not page_id:
                    print("没有下一页信息")
                    break
                
                # 添加延时避免被封
                time.sleep(1)
            
            print(f"爬取完成，共获取 {len(all_comments)} 条评论")
            return all_comments
            
        except Exception as e:
            print(f"爬取过程中出现错误: {e}")
            return []
    
    def save_to_csv(self, comments, filename=None):
        """保存评论到CSV文件"""
        if not comments:
            print("没有评论数据要保存")
            return None
        
        if filename is None:
            filename = DATA_DIR / "comments.csv"
        
        # 确保数据目录存在
        DATA_DIR.mkdir(exist_ok=True)
        
        df = pd.DataFrame(comments)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"评论数据已保存到: {filename}")
        return filename

def main():
    """主函数"""
    print("B站评论爬虫")
    print("-" * 40)
    
    bv = input("请输入BV号 (例: BV1234567890): ").strip()
    if not bv:
        print("BV号不能为空")
        return
    
    # 创建爬虫实例
    crawler = BilibiliCommentCrawler()
    
    # 爬取评论
    comments = crawler.crawl_comments(bv)
    
    # 保存到CSV
    if comments:
        crawler.save_to_csv(comments)
        print("爬取任务完成！")
    else:
        print("未获取到评论数据")

if __name__ == "__main__":
    main()
