import streamlit as st
import google.generativeai as genai
import time

# --- じゅんさん専用：ブラウザ負荷を最大化する描画関数 ---
def heavy_ai_render(full_text):
    container = st.empty()
    start_time = time.perf_counter()
    chars_count = 0
    
    # 1文字ずつ追加し、その度に「影付き・枠付き・フォント計算」をブラウザに強いる
    display_html = ""
    for char in full_text:
        chars_count += 1
        display_html += char
        # あえて複雑なCSSを毎文字適用してブラウザをいじめる
        container.markdown(f"""
            <div style="border: 2px solid #00ff00; padding: 15px; 
                        background: #000; color: #0f0; 
                        box-shadow: 0 0 10px #0f0; font-family: monospace;">
                {display_html}█
            </div>
        """, unsafe_allow_html=True)
        # 描画の「粘り」を見るための極小ウェイト
        time.sleep(0.002)
        
    end_time = time.perf_counter()
    duration = end_time - start_time
    cps = chars_count / duration  # Characters Per Second (実戦速度)
    return duration, cps

# --- メインポータル ---
st.title("⚡ AI Speed Test: 実戦編")

# 以前のグラフ結果をユーザーが入力できるようにする
with st.sidebar:
    st.header("📊 Base Muscle (Speedometer)")
    base_score = st.number_input("Speedometer Score", value=53.1)
    api_key = st.text_input("Gemini API Key", type="password")

tab1, tab2 = st.tabs(["API応答（脳）", "描画負荷（筋肉）"])

with tab1:
    st.subheader("📡 1. API Response Test")
    st.caption("AIが『考え始める』までの時間を測定。マシンスペックに依存しないはずの領域。")
    if st.button("脳の速さを測る"):
        # (既存のTTFT計測ロジック)
        pass

with tab2:
    st.subheader("🎨 2. NotebookLM Rendering Test")
    st.caption("AIの回答を『どれだけ滑らかに表示できるか』を測定。マシンの筋肉がモロに出る領域。")
    
    prompt = "3月のブログ記事をQOL・Dream・Financeで詳しく構造化して解説して。"
    
    if st.button("筋肉のキレを測る"):
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 1. まずAIからテキストを取得（ストリーミングなしで一度受ける）
            with st.spinner("AI生成中..."):
                response = model.generate_content(prompt)
                full_text = response.text
            
            # 2. 実戦描画スタート
            st.write("🏃‍♂️ レンダリング・スタート！")
            duration, cps = heavy_ai_render(full_text)
            
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("描画完走タイム", f"{duration:.2f} 秒")
            c2.metric("実戦速度 (CPS)", f"{cps:.1f} 文字/秒")
            
            # 3. 診断（Speedometerとの相関）
            efficiency = (cps / base_score) * 10
            st.info(f"💡 スコア診断: このマシンのAI描画効率は **{efficiency:.1f}** です。")