import streamlit as st
import google.generativeai as genai
import time

# --- APIキーの自動セットアップ ---
# Secretsに設定があればそれを使用し、なければサイドバーから入力できるようにします
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Gemini API Key", type="password")

# APIキーが取得できている場合のみ設定を有効化
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("⚠️ APIキーが設定されていません。サイドバーから入力するか、Secretsにセットしてください。")

# --- アプリ本体の構成 ---
st.title("⚡ AI Speed Test: 実戦ベンチマーク")

# 手持ちのマシンのSpeedometerスコアを比較の基準として入力
with st.sidebar:
    st.header("📊 マシンスペック設定")
    # グラフで判明した各マシンの数値を初期値として選べるようにしておくと便利です
    machine_score = st.number_input("Speedometer 3.0 Score", value=53.1)
    st.caption("M4 Safari: 53.1 / MBA: 4.49 / 2011 Sequoia: 1.25")

tab1, tab2 = st.tabs(["📡 脳：APIレスポンス", "🎨 筋肉：描画負荷テスト"])

with tab1:
    st.header("1. API Response Time (脳)")
    st.info("AIが考え始めてから、最初の1文字が届くまでの時間を測ります。")
    if st.button("脳の反応を測る", key="brain_test"):
        if not api_key:
            st.error("APIキーが必要です")
        else:
            model = genai.GenerativeModel('gemini-1.5-flash')
            start_time = time.perf_counter()
            # 軽い挨拶で通信速度をチェック
            response = model.generate_content("こんにちは。テストです。", stream=True)
            for chunk in response:
                ttft = (time.perf_counter() - start_time) * 1000
                st.metric("初速 (TTFT)", f"{ttft:.0f} ms")
                break

with tab2:
    st.header("2. AI Rendering Load (筋肉)")
    st.success("AIの回答を『どれだけ滑らかに表示できるか』。マシンの地力を試します。")
    
    # 描画負荷をかけるための重いレンダリング関数
   def heavy_render(text):
        container = st.empty()
        start = time.perf_counter()
        chars = 0
        display_text = ""
        # 1文字ずつではなく、描画を少し間引く
        for i, char in enumerate(text):
            chars += 1
            display_text += char
            # 3文字に1回だけ描画を更新するようにして負荷を調整
            if i % 3 == 0 or i == len(text) - 1:
                container.markdown(f"""
                    <div style="border: 2px solid #00ff00; padding: 10px; background: #000; color: #0f0; font-family: monospace;">
                    {display_text}█
                    </div>
                """, unsafe_allow_html=True)
            # 息継ぎの時間を少し増やす (0.001 -> 0.01)
            time.sleep(0.01) 
        end = time.perf_counter()
        return end - start, chars

    if st.button("筋肉のキレを測る", key="muscle_test"):
        if not api_key:
            st.error("APIキーが必要です")
        else:
            with st.spinner("AIが思考中..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                # NotebookLM的な構造化を模した少し長めのプロンプト
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
            
            # 王者M4(53.1)との比較診断
            if machine_score > 30:
                st.balloons()
                st.write("🚀 **王者クラス**: AI体験は完璧にスムーズです。")
            elif machine_score > 5:
                st.write("✅ **実用クラス**: ストレスなく対話が可能です。")
            else:
                st.write("🐢 **要転生クラス**: ChromeOS Flex等での軽量化が推奨されます。")
