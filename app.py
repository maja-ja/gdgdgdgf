import streamlit as st

# --- 1. 獨立學科模組 (每個學科一個 def) ---

# 國小模組
def elementary_chinese(): st.title("國小 - 國語宇宙"); st.info("專屬邏輯：生字解碼、注音符號 AI 輔助")
def elementary_english(): st.title("國小 - 英語宇宙"); st.info("專屬邏輯：Phonics 語音模組")
def elementary_math(): st.title("國小 - 數學宇宙"); st.info("專屬邏輯：基礎四則運算視覺化")

# 國中模組
def junior_chinese(): st.title("國中 - 國文宇宙"); st.info("專屬邏輯：文言文解構模組")
def junior_english(): st.title("國中 - 英文宇宙"); st.info("專屬邏輯：基礎文法框架")
def junior_math(): st.title("國中 - 數學宇宙"); st.info("專屬邏輯：幾何與代數運算")
def junior_science(): st.title("國中 - 自然宇宙"); st.info("專屬邏輯：理化實驗模擬")
def junior_social(): st.title("國中 - 社會宇宙"); st.info("專屬邏輯：歷史地理時間線")

# 高中模組 (嚴選 8 個模組)
def senior_chinese(): st.title("高中 - 國文"); st.write("核心：文學評論與古文觀止")
def senior_english(): st.title("高中 - 英文"); st.write("核心：學測/指考單字與作文")
def senior_math(): st.title("高中 - 數學"); st.write("核心：微積分與機率統計")
def senior_physics(): st.title("高中 - 物理"); st.write("核心：力學與電磁學")
def senior_chemistry(): st.title("高中 - 化學"); st.write("核心：有機化學與原子結構")
def senior_biology(): st.title("高中 - 生物"); st.write("核心：遺傳學與細胞生物")
def senior_earth_science(): st.title("高中 - 地科"); st.write("核心：大氣、地質與天文")
def senior_social_science(): st.title("高中 - 社會(歷公地)"); st.write("核心：跨科議題整合")

# --- 2. 映射表 (將主邏輯與 def 關聯) ---

MODULES = {
    "國小宇宙": {
        "國語": elementary_chinese, "英語": elementary_english, "數學": elementary_math
    },
    "國中宇宙": {
        "國文": junior_chinese, "英文": junior_english, "數學": junior_math, 
        "自然": junior_science, "社會": junior_social
    },
    "高中宇宙": {
        "國文": senior_chinese, "英文": senior_english, "數學": senior_math,
        "物理": senior_physics, "化學": senior_chemistry, "生物": senior_biology,
        "地科": senior_earth_science, "社會科學": senior_social_science
    }
}

# --- 3. 主程式 ---

def main():
    # 網址定義
    OLD_ERA_URL = "https://etymon-universe.streamlit.app/"

    # --- 側邊欄：Gateway 樣式 ---
    st.sidebar.title("Era Gateway")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        if st.button("舊世代", use_container_width=True):
            st.components.v1.html(f"<script>window.open('{OLD_ERA_URL}', '_self')</script>", height=0)
    with c2:
        st.button("新世代", disabled=True, use_container_width=True)
    
    st.sidebar.markdown(f'<a href="{OLD_ERA_URL}" target="_self" style="color: #58a6ff; text-decoration: none;">返回舊世代宇宙</a>', unsafe_allow_html=True)
    st.sidebar.markdown("---")

    # --- 主邏輯：學層選擇 ---
    level = st.sidebar.selectbox("切換教育宇宙", ["請選擇學段"] + list(MODULES.keys()) + ["🔄 重新開始"])

    if level == "🔄 重新開始":
        st.rerun()

    if level == "請選擇學段":
        st.title("✨ 新世代學科模組系統")
        st.write("請選擇左側學段開始。")
    else:
        # --- 次級邏輯：科目選擇 ---
        subjects = MODULES[level]
        selected_subject = st.sidebar.radio("選擇學科模組", list(subjects.keys()))
        
        # --- 執行對應的獨立 def ---
        subjects[selected_subject]()

if __name__ == "__main__":
    main()
