# update
import streamlit as st
import google.generativeai as genai
import time
import pandas as pd

# 🚩 記録用モジュールがあるかチェック
try:
    import data_logger
    HAS_LOGGER = True
except ImportError:
    HAS_LOGGER = False

# ========== ページ設定・デザイン ==========
st.set_page_config(page_title="AI Speed Test", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #e0e0e0; }
    .stMetric { background-color: #1c1f24; border: 1px solid #00ff00; padding: 15px; border-radius: 10px; }
    /* 入力欄などの色調整 */
    .stTextInput>div>div>input { color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AI Speed Test (Private Alpha)")
st.caption("最新AIを、オールドMacで快適に動かせるか？の異種格闘技戦")

# ========== APIキーの取得（金庫から参照） ==========
# Secretsに保存したキーをデフォルト値にする
default_key = st.secrets.get("MY_GEMINI_API_KEY", "")

# ========== サイドバー設定 ==========
with st.sidebar:
    st.header("💻 Test Environment")
    device_name = st.text_input("Device Name", "M4 Mac mini")
    os_version = st.text_input("OS Version", "macOS 15.1")
    st.divider()
    # 最初から金庫のキーをセットしておく（type="password"で中身は隠れる）
    api_key = st.text_input("Gemini API Key", value=default_key, type="password")
    
    if api_key == default_key and default_key != "":
        st.success("🔑 じゅんさんのキーをロードしました")
    
    if HAS_LOGGER:
        st.success("✅ Personal Logging: ON")

# ========== メインベンチマーク ==========
if not api_key:
    st.warning("サイドバーに Gemini API Key を入力してください。")
else:
    # 接続設定
    genai.configure(api_key=api_key)
    # じゅんさんのメモにあった最新の 2.0-flash を指定します
    model = genai.GenerativeModel('gemini-2.0-flash')

    prompt = st.text_area("Benchmark Prompt", 
        "以下のテーマで、300文字程度の短いブログ記事を生成し、最後に『QOL・Dream・Finance』の3軸で要約してください：\n「オールドMacにChromeOS Flexを入れて最新AI端末として蘇らせる楽しみについて」")

    if st.button("🚀 RUN BENCHMARK", use_container_width=True):
        start_time = time.perf_counter()
        ttft_time = None
        
        status_area = st.empty()
        response_area = st.empty()
        
        status_area.info("📡 Requesting to Gemini 2.0 Flash...")
        
        full_text = ""
        try:
            response = model.generate_content(prompt, stream=True)
            for chunk in response:
                if ttft_time is None:
                    ttft_time = (time.perf_counter() - start_time) * 1000
                    status_area.success(f"✔️ Response Received! (TTFT: {ttft_time:.0f}ms)")
                
                full_text += chunk.text
                response_area.markdown(full_text + "▌")
            
            total_time = (time.perf_counter() - start_time) * 1000
            response_area.markdown(full_text)
            
            # 結果表示
            st.divider()
            st.subheader("📊 Performance Score")
            col1, col2, col3 = st.columns(3)
            col1.metric("初速 (TTFT)", f"{ttft_time:.0f} ms")
            col2.metric("完走 (Total)", f"{total_time:.0f} ms")
            col3.metric("描画速度", f"{len(full_text)/(total_time/1000):.1f} 文字/秒")

            if HAS_LOGGER:
                if st.button("💾 じゅんさんのスプレッドシートに記録"):
                    if data_logger.log_result(device_name, os_version, ttft_time, total_time):
                        st.balloons()
                        st.success("スプレッドシートに記録しました！")
                        time.sleep(1)
                        st.rerun()
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# ========== ランキング表示 ==========
if HAS_LOGGER:
    st.divider()
    st.subheader("🏆 Leaderboard (Latest 10)")
    df = data_logger.get_history()
    if not df.empty:
        st.table(df.tail(10))
