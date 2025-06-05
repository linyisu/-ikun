from dotenv import load_dotenv
import requests
import os


def get_avid_from_bv(bv):
    url = f'https://api.bilibili.com/x/web-interface/view?bvid={bv}'
    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'aid' in data['data']:
            return data['data']['aid']
        else:
            raise ValueError("Invalid response structure")
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")


def get_comments(avid):
    params = {
        'type': 1,
        'oid': avid,
        'sort': 1,
        'pn': 2 ,
        'ps': 20,  # 每页20条评论

    }
    url = f'https://api.bilibili.com/x/v2/reply'
    response = session.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'replies' in data['data']:
            return data['data']['replies']
        else:
            raise ValueError("Invalid response structure")
    else:
        raise Exception(f"Failed to fetch comments: {response.status_code}")


if __name__ == "__main__":
    load_dotenv()
    cookies = os.getenv("BILI_COOKIE")
    
    bv = 'BV1qC4y1E7oU'  # 示例 BV 号

    session = requests.Session()
    session.cookies.set('SESSDATA', cookies)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    })

    try:
        avid = get_avid_from_bv(bv)
        print(f"AV号: {avid}")
        comments = get_comments(avid)
        print(f"评论数量: {len(comments)}")
        for comment in comments:
            print(f"评论内容: {comment['content']['message']}")
    except Exception as e:
        print(f"Error: {e}")