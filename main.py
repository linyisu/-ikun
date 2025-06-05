from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    cookie = os.getenv("BILI_COOKIE")
    if not cookie:
        raise ValueError("未找到 .env 文件中的 BILI_COOKIE 变量，请检查配置。")
    
    bv = 'BV1qC4y1E7oU'  # 示例 BV 号

    

if __name__ == "__main__":
    main()