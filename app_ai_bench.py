import streamlit as st
import google.generativeai as genai
import time

# --- APIキーの自動セットアップ ---
# じゅんさんのSecretsに合わせて「MY_GEMINI_API_KEY」を探すように修正しました
api_key = None

if "MY_GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["MY_GEMINI_API_KEY"]
elif "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

# サイドバーの入力欄（Secretsにない場合の予備）
input_key = st.sidebar.text_input("Gemini API Key (予備)", value=api_key if api_key else "", type="password")
final_key = input_key if input_key else api_key

# APIキーが取得できている場合のみ設定
if final_key:
    try:
        genai.configure(api_key=final_key)
    except Exception as e:
        st.error(f"API設定エラー: {e}")
else:
    st.warning("⚠️ APIキーがSecretsから読み込めません。サイドバーに入力するか、Secretsの変数名を確認してください。")

# --- アプリ本体の構成 ---
st.title("⚡ AI Speed Test: 実戦ベンチマーク")

with st.sidebar:
    st.header("📊 マシンスペック設定")
    machine_score = st.number_input("Speedometer 3.0 Score", value=53.1)
    st.caption("M4 Safari: 53.1 / MBA: 4.49 / 2011 Sequoia: 1.25")

tab1, tab2 = st.tabs(["📡 脳：APIレスポンス", "🎨 筋肉：描画負荷テスト"])

with tab1:
    st.header("1. API Response Time (脳)")
    st.info("AIが考え始めてから、最初の1文字が届くまでの時間を測ります。")
    if st.button("脳の反応を測る", key="brain_test"):
        if not final_key:
            st.error("APIキーが必要です")
        else:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                start_time = time.perf_counter()
                response = model.generate_content("こんにちは。テストです。", stream=True)
                for chunk in response:
                    ttft = (time.perf_counter() - start_time) * 1000
                    st.metric("初速 (TTFT)", f"{ttft:.0f} ms")
                    break
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

with tab2:
    st.header("2. AI Rendering Load (筋肉)")
    st.success("AIの回答を『どれだけ滑らかに表示できるか』。マシンの地力を試します。")
    
    def heavy_render(text):
        container = st.empty()
        start = time.perf_counter()
        chars = 0
        display_text = ""
        for i, char in enumerate(text):
            chars += 1
            display_text += char
            # 3文字に1回更新に制限してブラウザのフリーズを防ぐ
            if i % 3 == 0 or i == len(text) - 1:
                container.markdown(f"""
                    <div style="border: 2px solid #00ff00; padding: 10px; background: #000; color: #0f0; font-family: monospace;">
                    {display_text}█
                    </div>
                """, unsafe_allow_html=True)
            time.sleep(0.01) 
        end = time.perf_counter()
        return end - start, chars

    if st.button("筋肉のキレを測る", key="muscle_test"):
        if not final_key:
            st.error("APIキーが必要です")
        else:
            try:
                with st.spinner("AIが思考中..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt = "3月のブログまとめを、QOL、ドリーム、ファイナンスの3軸で、それぞれ100文字程度で構造化して解説して。"
                    response = model.generate_content(prompt)
                    full_text = response.text
                
                st.write("🏃‍♂️ レンダリング負荷計測開始...")
                duration, char_count = heavy_render(full_text)
                cps = char_count / duration
                
                st.divider()
                col1, col2 = st.columns(2)
                col1.metric("完走タイム", f"{duration:.2f} 秒")
                col2.metric("実戦描画速度", f"{cps:.1f} 文字/秒")
                
                if machine_score > 30:
                    st.balloons()
                    st.write("🚀 **王者クラス**: AI体験は完璧にスムーズです。")
                elif machine_score > 5:
                    st.write("✅ **実用クラス**: ストレスなく対話が可能です。")
                else:
                    st.write("🐢 **要転生クラス**: ChromeOS Flex等での軽量化が推奨されます。")
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
