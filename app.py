import streamlit as st

# --- 1. 獨立學科模組 (每個學科一個獨立 def) ---

# [國小] ---------------------------------------
def elem_chi(): st.title("🍎 國小國語"); st.write("模組：生字與閱讀解碼")
def elem_eng(): st.title("🔤 國小英語"); st.write("模組：聽力與口說解碼")
def elem_mat(): st.title("🔢 國小數學"); st.write("模組：基礎邏輯解碼")

# [國中] ---------------------------------------
def jun_chi(): st.title("📚 國中國文"); st.write("模組：古文與修辭分析")
def jun_eng(): st.title("🌍 國中英文"); st.write("模組：核心語法架構")
def jun_mat(): st.title("📐 國中數學"); st.write("模組：代數與幾何")
def jun_sci(): st.title("🧪 國中自然"); st.write("模組：理化生實驗室")
def jun_soc(): st.title("🏛️ 國中社會"); st.write("模組：地理歷史公民")

# [高中] (至多 8 個獨立 def) --------------------
def sen_chi(): st.title("🎭 高中國文"); st.write("解碼：高階文本思辨")
def sen_eng(): st.title("📑 高中英文"); st.write("解碼：學術寫作與翻譯")
def sen_mat(): st.title("📉 高中數學"); st.write("解碼：向量、微積分與統計")
def sen_phy(): st.title("⚡ 高中物理"); st.write("解碼：物理量與宇宙法則")
def sen_che(): st.title("🧪 高中化學"); st.write("解碼：物質變化的微觀宇宙")
def sen_bio(): st.title("🧬 高中生物"); st.write("解碼：生命系統的奧秘")
def sen_esc(): st.title("🪐 高中地科"); st.write("解碼：天文地質氣象")
def sen_hum(): st.title("🗺️ 高中人文"); st.write("解碼：歷公地跨科整合")

# --- 2. 主程式 ---

def main():
    # --- Era Gateway (側邊欄固定樣式) ---
    OLD_ERA_URL = "https://etymon-universe.streamlit.app/"
    st.sidebar.title("Era Gateway")
    
    col_old, col_new = st.sidebar.columns(2)
    with col_old:
        if st.sidebar.button("舊世代", use_container_width=True):
            st.components.v1.html(f"<script>window.open('{OLD_ERA_URL}', '_self')</script>", height=0)
    with col_new:
        st.sidebar.button("新世代", disabled=True, use_container_width=True)
    
    st.sidebar.markdown(f'<a href="{OLD_ERA_URL}" target="_self" style="color: #58a6ff; text-decoration: none;">返回舊世代宇宙</a>', unsafe_allow_html=True)
    st.sidebar.divider()

    # --- 第一層主邏輯 (學層選擇) ---
    universe = st.sidebar.selectbox(
        "🚀 選擇教育宇宙",
        ["請選擇學段", "國小宇宙", "國中宇宙", "高中宇宙"]
    )

    if universe == "請選擇學段":
        st.title("✨ 新世代學科解碼系統")
        st.info("請在左側選單選擇您要進入的教育階段。")

    # --- 第二層主邏輯 (全按鈕式選單) ---
    else:
        st.write(f"### {universe} | 學科模組導覽")
        
        if universe == "國小宇宙":
            # 國小 3 科按鈕
            sub_tab = st.radio("選擇科目", ["國語", "英語", "數學"], horizontal=True, label_visibility="collapsed")
            mapping = {"國語": elem_chi, "英語": elem_eng, "數學": elem_mat}
            st.divider()
            mapping[sub_tab]()

        elif universe == "國中宇宙":
            # 國中 5 科按鈕
            sub_tab = st.radio("選擇科目", ["國文", "英文", "數學", "自然", "社會"], horizontal=True, label_visibility="collapsed")
            mapping = {"國文": jun_chi, "英文": jun_eng, "數學": jun_mat, "自然": jun_sci, "社會": jun_soc}
            st.divider()
            mapping[sub_tab]()

        elif universe == "高中宇宙":
            # 高中 8 科按鈕 (使用 radio 橫向排列營造按鈕感)
            sub_tab = st.radio(
                "選擇科目", 
                ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "人文"], 
                horizontal=True, 
                label_visibility="collapsed"
            )
            mapping = {
                "國文": sen_chi, "英文": sen_eng, "數學": sen_mat, 
                "物理": sen_phy, "化學": sen_che, "生物": sen_bio, 
                "地科": sen_esc, "人文": sen_hum
            }
            st.divider()
            mapping[sub_tab]()

if __name__ == "__main__":
    main()
