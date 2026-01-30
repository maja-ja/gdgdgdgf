import streamlit as st
import pandas as pd
import base64
import time
import json
from io import BytesIO
from gtts import gTTS

# ==========================================
# 1. 核心配置與 CSS (繼承 v2.5 視覺)
# ==========================================
st.set_page_config(page_title="Etymon Universe: New Era", page_icon="🧩", layout="wide")

def inject_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Noto+Sans+TC:wght@500;700&display=swap');
            .breakdown-container {
                font-family: 'Inter', 'Noto Sans TC', sans-serif; 
                font-size: 1.6rem !important; 
                background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
                color: #FFFFFF; padding: 10px 25px; border-radius: 12px;
                display: inline-block; margin: 10px 0;
            }
            .hero-word { font-size: 3.5rem; font-weight: 900; color: #1E88E5; }
            div.stButton > button:first-child { border-radius: 10px; height: 3em; }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 獨立模組定義 (每個學科一個獨立 def)
# ==========================================

# --- 國小模組 ---
def elem_chi(): st.title("🍎 國小國語"); st.write("模組：生字與閱讀")
def elem_eng(): st.title("🔤 國小英語"); st.write("模組：Phonics 語音")
def elem_mat(): st.title("🔢 國小數學"); st.write("模組：基礎邏輯")

# --- 國中模組 ---
def jun_chi(): st.title("📚 國中國文"); st.write("模組：文言文解構")
def jun_eng(): st.title("🌍 國中英文"); st.write("模組：核心語法")
def jun_mat(): st.title("📐 國中數學"); st.write("模組：代數與幾何")
def jun_sci(): st.title("🧪 國中自然"); st.write("模組：理化生基礎")
def jun_soc(): st.title("🏛️ 國中社會"); st.write("模組：史地整合")

# --- 高中模組 (完整 10 科) ---
def sen_chi(): st.title("🎭 高中國文"); st.success("高階文本思辨載入中...")
def sen_eng(): st.title("📑 高中英文"); st.success("學術寫作解碼載入中...")
def sen_mat(): st.title("📉 高中數學"); st.success("高等數學邏輯載入中...")
def sen_bio(): st.title("🧬 高中生物"); st.success("生命科學解碼載入中...")
def sen_che(): st.title("🧪 高中化學"); st.success("微觀化學反應載入中...")
def sen_esc(): st.title("🪐 高中地科"); st.success("天文與地質解碼載入中...")
def sen_phy(): st.title("⚡ 高中物理"); st.success("古典與當代物理載入中...")
def sen_geo(): st.title("🗺️ 高中地理"); st.success("全球與區域地理載入中...")
def sen_his(): st.title("📜 高中歷史"); st.success("時間線與歷史解構載入中...")
def sen_civ(): st.title("⚖️ 高中公民"); st.success("法律與社會制度載入中...")

# ==========================================
# 3. 主導航與 Gateway (解決跳轉問題)
# ==========================================
def main():
    inject_custom_css()
    
    # 網址定義
    OLD_ERA_URL = "https://etymon-universe.streamlit.app/"
    
    # 側邊欄 Era Gateway
    st.sidebar.title("Era Gateway")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        # 使用 HTML 標籤直接跳轉，避免 Redirect 迴圈
        st.markdown(f'''<a href="{OLD_ERA_URL}" target="_self">
            <button style="width:100%; cursor:pointer; background-color:transparent; border:1px solid #4B4B4B; color:white; padding:8px; border-radius:5px;">舊世代</button>
            </a>''', unsafe_allow_html=True)
    with c2:
        if st.sidebar.button("新世代", use_container_width=True, type="primary"):
            # 點擊「新世代」即重設為首頁
            st.session_state.level = "🏠 首頁"
            st.rerun()

    st.sidebar.divider()

    # --- 主選擇邏輯 ---
    level = st.sidebar.selectbox(
        "選擇教育宇宙",
        ["🏠 首頁", "國小宇宙", "國中宇宙", "高中宇宙"],
        key="main_level_selector"
    )

    # --- 分流渲染 ---
    if level == "🏠 首頁":
        st.title("✨ 新世代全學段解碼宇宙")
        st.info("系統偵測您已成功進入新世代環境。")
        st.write("請從左側選擇您的教育階段。所有的學科已經各自模組化。")

    elif level == "國小宇宙":
        sub = st.radio("學科按鈕", ["國語", "英語", "數學"], horizontal=True)
        st.divider()
        maps = {"國語": elem_chi, "英語": elem_eng, "數學": elem_mat}
        maps[sub]()

    elif level == "國中宇宙":
        sub = st.radio("學科按鈕", ["國文", "英文", "數學", "自然", "社會"], horizontal=True)
        st.divider()
        maps = {"國文": jun_chi, "英文": jun_eng, "數學": jun_mat, "自然": jun_sci, "社會": jun_soc}
        maps[sub]()

    elif level == "高中宇宙":
        # 完整顯示 10 個科目的按鈕
        sub = st.radio(
            "學科按鈕", 
            ["國文", "英文", "數學", "生物", "化學", "地科", "物理", "地理", "歷史", "公民"], 
            horizontal=True
        )
        st.divider()
        maps = {
            "國文": sen_chi, "英文": sen_eng, "數學": sen_mat, "生物": sen_bio,
            "化學": sen_che, "地科": sen_esc, "物理": sen_phy, "地理": sen_geo,
            "歷史": sen_his, "公民": sen_civ
        }
        maps[sub]()

if __name__ == "__main__":
    main()
