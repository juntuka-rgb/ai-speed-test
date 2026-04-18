import streamlit as st
import google.generativeai as genai
import time
import pandas as pd
import io

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
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1c1f24; border: 1px solid #00ff00; padding: 15px; border-radius: 10px; }
    div[data-testid="stExpander"] { border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AI Speed Test (Alpha)")
st.caption("最新AI(Gemini)を、オールドMacで快適に動かせるか？の異種格闘技戦")

# ========== サイドバー設定 ==========
with st.sidebar:
    st.header("💻 Test Environment")
    device_name = st.text_input("Device Name", "M4 Mac mini")
    os_version = st.text_input("OS Version", "macOS 15.1")
    st.divider()
    api_key = st.text_input("Gemini API Key", type="password")
    
    if HAS_LOGGER:
        st.success("✅ Personal Logging: ON")
    else:
        st.info("💡 Logging Mode: OFF (配布用)")

# ========== メインベンチマーク ==========
if not api_key:
    st.warning("サイドバーに Gemini API Key を入力してください。")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = st.text_area("Benchmark Prompt", 
        "以下のテーマで、300文字程度の短いブログ記事を生成し、最後に『QOL・Dream・Finance』の3軸で要約してください：\n「オールドMacにChromeOS Flexを入れて最新AI端末として蘇らせる楽しみについて」")

    if st.button("🚀 RUN BENCHMARK", use_container_width=True):
        start_time = time.perf_counter()
        ttft_time = None
        
        status_area = st.empty()
        response_area = st.empty()
        
        status_area.info("📡 Requesting to Gemini API...")
        
        full_text = ""
        # ストリーミング実行
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if ttft_time is None:
                ttft_time = (time.perf_counter() - start_time) * 1000
                status_area.success(f"✔️ Response Received! (TTFT: {ttft_time:.0f}ms)")
            
            full_text += chunk.text
            response_area.markdown(full_text + "▌")
        
        total_time = (time.perf_counter() - start_time) * 1000
        response_area.markdown(full_text)
        
        # ========== 結果パネル ==========
        st.divider()
        st.subheader("📊 Performance Score")
        col1, col2, col3 = st.columns(3)
        col1.metric("初速 (TTFT)", f"{ttft_time:.0f} ms")
        col2.metric("完走 (Total)", f"{total_time:.0f} ms")
        col3.metric("描画速度", f"{len(full_text)/(total_time/1000):.1f} 文字/秒")

        # SNSシェア用
        share_text = f"【AIスピードテスト結果】\n💻 {device_name} ({os_version})\n⚡ 初速: {ttft_time:.0f}ms\n🏁 完走: {total_time:.0f}ms\n#AISpeedTest #GeminiAI"
        st.text_area("📢 SNSシェア用テキスト (Facebookコメント欄にどうぞ！)", share_text, height=120)

        # じゅんさん専用保存ボタン
        if HAS_LOGGER:
            if st.button("💾 じゅんさんのスプレッドシートに記録"):
                if data_logger.log_result(device_name, os_version, ttft_time, total_time):
                    st.balloons()
                    st.success("スプレッドシートに記録完了！")
                    st.rerun()

# ========== ランキング表示（じゅんさん専用機能） ==========
if HAS_LOGGER:
    st.divider()
    st.subheader("🏆 Official Leaderboard (じゅんさんの記録)")
    df = data_logger.get_history()
    if not df.empty:
        # 最新10件を表示
        st.table(df.tail(10))
    else:
        st.info("まだ記録がありません。最初のテストを実行しましょう！")