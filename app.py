import streamlit as st
import pandas as pd
import base64
import time
import json
from io import BytesIO
from gtts import gTTS

# ==========================================
# 1. 核心配置與 CSS
# ==========================================
st.set_page_config(page_title="Etymon Universe: New Era", page_icon="🧩", layout="wide")

def inject_custom_css():
    st.markdown("""
        <style>
            /* 保持你原本的 v2.5 視覺樣式 */
            .breakdown-container {
                font-family: 'Inter', 'Noto Sans TC', sans-serif; 
                font-size: 1.5rem !important; 
                background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
                color: #FFFFFF; padding: 12px 25px; border-radius: 12px;
                display: inline-block; margin: 10px 0;
            }
            .hero-word { font-size: 3.5rem; font-weight: 900; color: #1E88E5; }
            /* 自定義按鈕樣式 */
            div.stButton > button:first-child { border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 獨立學科模組 (每個學科一個 def)
# ==========================================

# --- 國小模組 ---
def elem_chi(): st.title("🍎 國小國語"); st.info("新世代國語解碼邏輯載入中...")
def elem_eng(): st.title("🔤 國小英語"); st.info("新世代英語聽力模組載入中...")
def elem_mat(): st.title("🔢 國小數學"); st.info("新世代數學圖形模組載入中...")

# --- 國中模組 ---
def jun_chi(): st.title("📚 國中國文"); st.write("模組：文言文解構器")
def jun_eng(): st.title("🌍 國中英文"); st.write("模組：核心文法框架")
def jun_mat(): st.title("📐 國中數學"); st.write("模組：代數與幾何")
def jun_sci(): st.title("🧪 國中自然"); st.write("模組：理化生實驗室")
def jun_soc(): st.title("🏛️ 國中社會"); st.write("模組：史地整合系統")

# --- 高中模組 (完整 10 科) ---
def sen_chi(): st.title("🎭 高中國文"); st.success("高階文本思辨模組")
def sen_eng(): st.title("📑 高中英文"); st.success("學術寫作與閱讀解碼")
def sen_mat(): st.title("📉 高中數學"); st.success("微積分與統計分析")
def sen_bio(): st.title("🧬 高中生物"); st.success("分子生物與遺傳解碼")
def sen_che(): st.title("🧪 高中化學"); st.success("物質變化與有機化學")
def sen_esc(): st.title("🪐 高中地科"); st.success("天文與大氣科學")
def sen_phy(): st.title("⚡ 高中物理"); st.success("力學與電磁學實驗室")
def sen_geo(): st.title("🗺️ 高中地理"); st.success("空間資訊與地理系統")
def sen_his(): st.title("📜 高中歷史"); st.success("歷史脈絡與斷代分析")
def sen_civ(): st.title("⚖️ 高中公民"); st.success("法律、經濟與社會研究")

# ==========================================
# 3. 主導航與 Gateway
# ==========================================
def main():
    # 這是你剛才提供的「舊世代」網址
    st.sidebar.title("Era Gateway")
    
    # 準備網址
    OLD_ERA_URL = "https://etymon-universe.streamlit.app/"
    
    col_a, col_b = st.sidebar.columns(2)
    
    with col_a:
        # 這是最穩定的方式：看起來像按鈕的 Markdown 連結
        # target="_self" 確保在同一個標籤頁開啟，不會被瀏覽器攔截
        st.markdown(
            f"""
            <a href="{OLD_ERA_URL}" target="_self" style="text-decoration: none;">
                <div style="
                    text-align: center;
                    background-color: transparent;
                    border: 1px solid #4B4B4B;
                    padding: 6px;
                    border-radius: 10px;
                    color: white;
                    font-size: 14px;
                    cursor: pointer;">
                    🔙 舊世代
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )
    
    with col_b:
        # 新世代按鈕只做「App 內部的重置」，不涉及網址跳轉，所以不會有 Redirect 錯誤
        if st.sidebar.button("✨ 新世代", use_container_width=True, type="primary"):
            # 清除 Session 狀態，強迫回到首頁
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    st.sidebar.divider()

    # --- 高中 10 科按鈕邏輯 ---
    st.write("### 🚀 高中宇宙全學科解碼")
    sub = st.radio(
        "選擇科目", 
        ["國文", "英文", "數學", "生物", "化學", "地科", "物理", "地理", "歷史", "公民"], 
        horizontal=True
    )
    
    st.divider()
    # 執行對應 def
    if sub == "物理": sen_phy()
    elif sub == "化學": sen_che()
    else: st.write(f"目前進入：高中{sub}")

if __name__ == "__main__":
    main()
