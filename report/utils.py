import os
import traceback

def file_exists(path):
    return os.path.exists(path)

def print_traceback():
    return traceback.format_exc()
