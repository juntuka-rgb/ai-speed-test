import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

def connect():
    # 🚩 StreamlitのSecretsから認証情報を取得（クラウド公開時）
    # ローカル実行時は st.secrets 経由、または direct に jsonファイルを指定します
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # じゅんさんの既存の仕組みに合わせて、Secretsから読み込む形式にします
    conf = st.secrets["gcp_service_account"]
    
    creds = Credentials.from_service_account_info(conf, scopes=scope)
    client = gspread.authorize(creds)
    
    # スプレッドシート名（ファイル名）を指定して開く
    # ※今回は「AIスピードテスト」という名前のスプレッドシートを想定
    # （存在しない場合はじゅんさんの既存のスプレッドシート名を指定してください）
    ss = client.open("AIスピードテスト") 
    return ss