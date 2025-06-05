import csv
import re
from spider.get_comments import getInfo, getComments

def safe_filename(name):
    # 替换掉 Windows 文件名不允许的字符
    return re.sub(r'[\\/:*?"<>|]', '_', name)

def main():
    BV = input("请输入BV号：")
    link = f'https://www.bilibili.com/video/{BV}'
    oid, title = getInfo(BV, link)
    print(title[:-14])

    needCnt = 1000
    total_count = 0
    filename = f'{safe_filename(title[:-14])}_评论.csv'
    with open(filename, mode='w+', newline='', encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['序号', '用户ID', '用户名', '用户等级', '性别', '评论内容', '评论时间', '回复数', '点赞数', '个性签名'])
        getComments(oid)

if __name__ == '__main__':
    main()