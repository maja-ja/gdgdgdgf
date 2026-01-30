import streamlit as st

# --- 1. 模組化學科函式 (每個學科一個獨立 def) ---

# 國小組 (3個獨立模組)
def elementary_chinese():
    st.title("🍎 國小國語宇宙")
    st.write("目前進入：國小國語模組")

def elementary_english():
    st.title("🔤 國小英語宇宙")
    st.write("目前進入：國小英語模組")

def elementary_math():
    st.title("🔢 國小數學宇宙")
    st.write("目前進入：國小數學模組")

# 國中組 (5個獨立模組)
def junior_chinese():
    st.title("📚 國中國文宇宙")
    st.write("目前進入：國中國文模組")

def junior_english():
    st.title("🌍 國中英文宇宙")
    st.write("目前進入：國中英文模組")

def junior_math():
    st.title("📐 國中數學宇宙")
    st.write("目前進入：國中數學模組")

def junior_science():
    st.title("🧪 國中自然宇宙")
    st.write("目前進入：國中自然模組")

def junior_social():
    st.title("🏛️ 國中社會宇宙")
    st.write("目前進入：國中社會模組")

# 高中組 (精選 8 個獨立模組)
def senior_chinese(): st.title("🎭 高中國文"); st.write("模組內容：深層文本分析")
def senior_english(): st.title("📑 高中英文"); st.write("模組內容：學術寫作與閱讀")
def senior_math(): st.title("📉 高中數學"); st.write("模組內容：微積分與向量")
def senior_physics(): st.title("⚡ 高中物理"); st.write("模組內容：古典力學與量子物理")
def senior_chemistry(): st.title("🧪 高中化學"); st.write("模組內容：有機化學與平衡")
def senior_biology(): st.title("🧬 高中生物"); st.write("模組內容：分子生物與遺傳")
def senior_earth(): st.title("🪐 高中地科"); st.write("模組內容：天文與大氣科學")
def senior_social_integrated(): st.title("🗺️ 高中人文社會"); st.write("模組內容：歷公地跨科整合")

# --- 2. 主程式 ---

def main():
    # --- Era Gateway (側邊欄固定樣式) ---
    OLD_ERA_URL = "https://etymon-universe.streamlit.app/"
    st.sidebar.title("Era Gateway")
    
    col_old, col_new = st.sidebar.columns(2)
    with col_old:
        if st.button("舊世代", use_container_width=True):
            st.components.v1.html(f"<script>window.open('{OLD_ERA_URL}', '_self')</script>", height=0)
    with col_new:
        st.button("新世代", disabled=True, use_container_width=True)
    
    st.sidebar.markdown(f'<a href="{OLD_ERA_URL}" target="_self" style="color: #58a6ff; text-decoration: none;">返回舊世代宇宙</a>', unsafe_allow_html=True)
    st.sidebar.divider()

    # --- App 主選單 (主邏輯：學層) ---
    universe = st.sidebar.selectbox(
        "🚀 選擇教育宇宙",
        ["請選擇學段", "國小宇宙", "國中宇宙", "高中宇宙"]
    )

    # --- 根據選擇分流至各學層模組 ---
    if universe == "請選擇學段":
        st.title("✨ 新世代學科解碼系統")
        st.info("請在左側選單選擇您要進入的教育宇宙。")
        
    elif universe == "國小宇宙":
        # 國小次級導覽
        sub_tab = st.radio("學科模組", ["國語", "英語", "數學"], horizontal=True)
        mapping = {"國語": elementary_chinese, "英語": elementary_english, "數學": elementary_math}
        mapping[sub_tab]()

    elif universe == "國中宇宙":
        # 國中次級導覽
        sub_tab = st.radio("學科模組", ["國文", "英文", "數學", "自然", "社會"], horizontal=True)
        mapping = {
            "國文": junior_chinese, "英文": junior_english, "數學": junior_math, 
            "自然": junior_science, "社會": junior_social
        }
        mapping[sub_tab]()

    elif universe == "高中宇宙":
        # 高中次級導覽 (至多 8 頁)
        sub_tab = st.selectbox("選擇學科頁面", 
                             ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "人文社會"])
        mapping = {
            "國文": senior_chinese, "英文": senior_english, "數學": senior_math, 
            "物理": senior_physics, "化學": senior_chemistry, "生物": senior_biology, 
            "地科": senior_earth, "人文社會": senior_social_integrated
        }
        mapping[sub_tab]()

if __name__ == "__main__":
    main()
