import streamlit as st
import pandas as pd
import base64
import time
import json
from io import BytesIO
from gtts import gTTS
import streamlit.components.v1 as components

# ==========================================
# 1. 核心視覺配置 (繼承 v2.5 靈魂)
# ==========================================
st.set_page_config(page_title="Etymon Universe 3.0", page_icon="🚀", layout="wide")

def inject_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Noto+Sans+TC:wght@500;700&display=swap');
            .subject-card {
                font-family: 'Inter', 'Noto Sans TC', sans-serif; 
                background: linear-gradient(135deg, #1E88E5 0%, #1565C0 100%);
                color: white; padding: 20px; border-radius: 15px;
                margin-bottom: 15px; box-shadow: 0 4px 15px rgba(30, 136, 229, 0.3);
            }
            .hero-title { font-size: 3.5rem; font-weight: 900; color: #1E88E5; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 學科模組定義 (在這裡擴充內容)
# ==========================================
def render_subject_content(title, desc, modules):
    st.markdown(f"<div class='subject-card'><h1>{title}</h1><p>{desc}</p></div>", unsafe_allow_html=True)
    cols = st.columns(len(modules))
    for i, mod in enumerate(modules):
        with cols[i]:
            if st.button(f"🔓 開啟 {mod}", key=f"{title}_{mod}", use_container_width=True):
                st.balloons()
                st.info(f"{mod} 模組解碼中...")

# ==========================================
# 3. 穩定導航系統 (防止 Redirect Loop)
# ==========================================
def main():
    inject_custom_css()
    OLD_ERA_URL = "https://etymon-universe.streamlit.app/"

    # --- 側邊欄 Era Gateway ---
    st.sidebar.title("🌌 世代門戶")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        st.markdown(f'<a href="{OLD_ERA_URL}" target="_self" style="text-decoration:none;"><div style="text-align:center; padding:8px; border:1px solid #4B4B4B; border-radius:10px; color:white;">🔙 舊世代</div></a>', unsafe_allow_html=True)
    with c2:
        if st.sidebar.button("✨ 重置首頁", use_container_width=True, type="primary"):
            st.session_state.clear()
            st.rerun()

    st.sidebar.divider()

    # --- 學段切換 ---
    universe = st.sidebar.radio(
        "選擇教育宇宙",
        ["🏠 宇宙中心", "🌱 國小宇宙", "🧬 國中宇宙", "🛰️ 高中宇宙"]
    )

    if universe == "🏠 宇宙中心":
        st.markdown("<div class='hero-title'>Etymon Universe 3.0</div>", unsafe_allow_html=True)
        st.write("---")
        st.subheader("歡迎來到新世代解碼核心")
        st.write("我們已將原本的單字解碼技術，擴散到全台灣學子的所有學科。請由左側選擇您的學段。")
        
        # 視覺數據卡片
        col1, col2, col3 = st.columns(3)
        col1.metric("解碼學段", "3 大宇宙")
        col2.metric("涵蓋學科", "18 門科目")
        col3.metric("系統狀態", "穩定執行中")

    elif universe == "🌱 國小宇宙":
        sub = st.selectbox("選擇科目", ["國語", "英語", "數學"])
        if sub == "國語": render_subject_content("🍎 國小國語", "字感與修辭解碼", ["識字規律", "成語宇宙", "作文邏輯"])
        elif sub == "英語": render_subject_content("🔤 國小英語", "基礎音韻與語感", ["自然發音", "核心單字", "情境對話"])
        elif sub == "數學": render_subject_content("🔢 國小數學", "圖像化邏輯運算", ["幾何拼圖", "數感訓練", "應用問題"])

    elif universe == "🧬 國中宇宙":
        sub = st.radio("選擇科目", ["國文", "英文", "數學", "自然", "社會"], horizontal=True)
        st.divider()
        render_subject_content(f"📚 國中{sub}", f"國中{sub}核心框架載入中", ["重點筆記", "考古題解", "考點預測"])

    elif universe == "🛰️ 高中宇宙":
        sub = st.selectbox("選擇科目", ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "歷史", "地理", "公民"])
        st.divider()
        # 這裡就是你的高中 10 科！
        render_subject_content(f"🚀 高中{sub}", f"高階{sub}深度思辨與學術模型", ["學測攻堅", "分科測驗", "學習歷程"])

if __name__ == "__main__":
    main()
