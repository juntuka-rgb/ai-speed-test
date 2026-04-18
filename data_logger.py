import common
from datetime import datetime
import pytz
import pandas as pd

def log_result(device, os_ver, ttft, total):
    try:
        ss = common.connect()
        sheet = ss.worksheet("AIベンチマーク")
        
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tokyo_tz).strftime('%Y/%m/%d %H:%M:%S')
        
        # 記録内容：日時, デバイス名, OS, TTFT, 合計時間
        sheet.append_row([now, device, os_ver, round(ttft, 2), round(total, 2)])
        return True
    except Exception as e:
        return False

def get_history():
    try:
        ss = common.connect()
        sheet = ss.worksheet("AIベンチマーク")
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()