"""
通用工具函数模块
"""
import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from config.settings import DATA_DIR

def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(exist_ok=True)

def save_comments_to_csv(comments, filename=None, bv=None):
    """保存评论数据到CSV文件"""
    if not comments:
        return None
    
    ensure_data_dir()
    
    if filename is None:
        if bv:
            filename = f"{bv}_comments.csv"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comments_{timestamp}.csv"
    
    filepath = DATA_DIR / filename
    df = pd.DataFrame(comments)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    return filepath

def load_csv_file(filepath):
    """加载CSV文件"""
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        print(f"加载CSV文件失败: {e}")
        return None

def get_csv_files():
    """获取数据目录下的所有CSV文件"""
    ensure_data_dir()
    return list(DATA_DIR.glob("*.csv"))

def format_timestamp(timestamp):
    """格式化时间戳"""
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return ""

def clean_text(text):
    """清理文本内容"""
    if not text:
        return ""
    
    # 移除换行符和多余空格
    text = str(text).replace('\n', ' ').replace('\r', '').strip()
    
    # 移除多余空格
    import re
    text = re.sub(r'\s+', ' ', text)
    
    return text

def validate_bv_number(bv):
    """验证BV号格式"""
    import re
    pattern = r'^BV[1-9A-Za-z]{10}$'
    return bool(re.match(pattern, bv))

def get_file_size(filepath):
    """获取文件大小（人类可读格式）"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    except:
        return "未知"

def create_backup(filepath, backup_dir=None):
    """创建文件备份"""
    if backup_dir is None:
        backup_dir = DATA_DIR / "backup"
    
    backup_dir = Path(backup_dir)
    backup_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_file = Path(filepath)
    backup_name = f"{original_file.stem}_{timestamp}{original_file.suffix}"
    backup_path = backup_dir / backup_name
    
    try:
        import shutil
        shutil.copy2(filepath, backup_path)
        return backup_path
    except Exception as e:
        print(f"创建备份失败: {e}")
        return None
