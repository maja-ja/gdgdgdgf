import streamlit as st
import pandas as pd
import base64
import time
import json
import os
import sqlite3
from io import BytesIO
from gtts import gTTS
import streamlit.components.v1 as components

# ==========================================
# 1. 進階配置與 PWA 注入
# ==========================================
st.set_page_config(
    page_title="Etymon Decoder Pro",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_pwa_and_css():
    # PWA Manifest & Service Worker 注入
    pwa_js = """
    <link rel="manifest" href="https://your-domain.com/manifest.json">
    <script>
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('https://your-domain.com/service-worker.js');
      }
    </script>
    """
    
    # 專業學術 UI 系統 (Lora 為襯線, Inter 為無襯線)
    st.markdown(f"""
        {pwa_js}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Lora:ital,wght@0,400;0,700;1,400&family=Noto+Sans+TC:wght@400;700&display=swap');

            /* 全域字體設定 */
            html, body, [class*="css"] {{
                font-family: 'Inter', 'Noto Sans TC', sans-serif;
            }}

            /* 標題學術感 */
            .hero-word {{
                font-family: 'Lora', serif;
                font-size: clamp(2.5rem, 8vw, 4.5rem);
                font-weight: 700;
                color: #1A237E;
                line-height: 1.1;
                margin-bottom: 0.2rem;
            }}

            /* 響應式 Breakdown 容器 */
            .breakdown-container {{
                font-size: clamp(1rem, 4vw, 1.8rem);
                background: linear-gradient(135deg, #1A237E 0%, #283593 100%);
                color: white;
                padding: 15px 25px;
                border-radius: 12px;
                display: block; /* 手機端自動展開 */
                text-align: center;
                margin: 15px 0;
            }}

            /* 護眼模式控制 (由 Python State 切換) */
            .main {{
                background-color: {st.session_state.get('theme_bg', '#FFFFFF')};
                color: {st.session_state.get('theme_text', '#121212')};
            }}

            /* 隱藏 Streamlit 預設裝飾 */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 資料庫：SQLite 離線備份機制
# ==========================================
def init_offline_db():
    conn = sqlite3.connect('local_cache.db')
    return conn

def load_db_with_cache():
    SHEET_ID = "1W1ADPyf5gtGdpIEwkxBEsaJ0bksYldf4AugoXnq6Zvg"
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'
    
    try:
        # 嘗試從網路讀取
        df = pd.read_csv(url)
        # 備份到本地 SQLite
        conn = init_offline_db()
        df.to_sql('etymon_data', conn, if_exists='replace', index=False)
        return df
    except Exception as e:
        # 斷網時讀取本地
        try:
            conn = init_offline_db()
            return pd.read_sql('SELECT * FROM etymon_data', conn)
        except:
            return pd.DataFrame()

# ==========================================
# 3. 語音系統優化
# ==========================================
def speak_v2(text):
    # 使用快取避免重覆產生音頻
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    b64 = base64.b64encode(fp.getvalue()).decode()
    md = f"""
        <audio id="audio_tag" autoplay>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(md, height=0)

# ==========================================
# 4. 主程式介面
# ==========================================
def main():
    if 'theme_bg' not in st.session_state:
        st.session_state.theme_bg = '#FFFFFF'
        st.session_state.theme_text = '#121212'

    inject_pwa_and_css()
    df = load_db_with_cache()

    # --- 側邊欄：功能與主題 ---
    st.sidebar.title("Etymon Decoder")
    
    # 主題切換
    theme = st.sidebar.select_slider(
        "閱讀模式",
        options=["明亮", "護眼", "深藍"],
        value="明亮"
    )
    theme_map = {
        "明亮": ("#FFFFFF", "#121212"),
        "護眼": ("#F4ECD8", "#5B4636"), # 羊皮紙色
        "深藍": ("#0A192F", "#E6F1FF")
    }
    st.session_state.theme_bg, st.session_state.theme_text = theme_map[theme]

    menu = st.sidebar.radio("導航", ["學術探索", "專業分類", "Mix Lab 實驗室"])

    if menu == "學術探索":
        st.markdown("<div class='hero-word'>Decoding Knowledge</div>", unsafe_allow_html=True)
        
        # 搜尋功能
        search_query = st.text_input("🔍 搜尋術語 (例: Neuro, Juris...)", "")
        
        if search_query:
            results = df[df['word'].str.contains(search_query, case=False, na=False)]
            for _, row in results.iterrows():
                with st.expander(f"{row['word']} - {row['definition']}"):
                    show_detailed_card(row)
        else:
            # 隨機展示
            if st.button("🎲 隨機獲取新單字"):
                st.session_state.random_word = df.sample(1).iloc[0]
            
            if 'random_word' in st.session_state:
                show_detailed_card(st.session_state.random_word)

def show_detailed_card(row):
    st.markdown(f"<div class='hero-word'>{row['word']}</div>", unsafe_allow_html=True)
    st.markdown(f"**/{row['phonetic']}/ | {row['category']}**")
    
    # 響應式 Layout 優化：在窄螢幕自動堆疊
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div class='breakdown-container'>{row['breakdown']}</div>", unsafe_allow_html=True)
    with col2:
        if st.button("🔊 發音", key=f"audio_{row['word']}"):
            speak_v2(row['word'])

    st.markdown("---")
    t1, t2, t3 = st.tabs(["📖 定義與用法", "🏛️ 字源背景", "👔 專業場景"])
    with t1:
        st.write(f"**學術定義:** {row['definition']}")
        st.info(f"**例句:** {row['example']}")
    with t2:
        st.write(f"**字根核心:** {row['roots']} ({row['meaning']})")
        st.success(f"**記憶法:** {row['memory_hook']}")
    with t3:
        st.write(f"**社會地位感:** {row['social_status']}")
        st.warning(f"**使用警告:** {row['usage_warning']}")

if __name__ == "__main__":
    main()
