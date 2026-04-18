import common
from datetime import datetime
import pytz
import pandas as pd

def log_result(device, os_ver, ram, ttft, total, char_count):
    try:
        ss = common.connect()
        sheet = ss.worksheet("AIベンチマーク")
        
        # 現在のデータ行数を取得
        values = sheet.get_all_values()
        current_rows = len(values)
        
        # 空行を掃除（1行目だけ残す）
        if current_rows > 0:
            sheet.resize(rows=current_rows)
        
        # 時刻取得
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        now = datetime.now(tokyo_tz).strftime('%Y/%m/%d %H:%M:%S')
        
        # 描画速度（文字/秒）を計算
        speed = round(char_count / (total / 1000), 1)
        
        # A列〜G列までのデータを1行にまとめる
        row_data = [now, device, os_ver, ram, round(ttft, 2), round(total, 2), speed]
        
        # スプレッドシートへ追記
        sheet.append_row(row_data, value_input_option='USER_ENTERED')
        
        return True
    except Exception as e:
        print(f"Logging Error: {e}")
        return False

def get_history():
    try:
        ss = common.connect()
        sheet = ss.worksheet("AIベンチマーク")
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()
