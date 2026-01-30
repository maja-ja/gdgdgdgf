import streamlit as st

# --- 1. 獨立學科模組 (每個學科一個獨立 def) ---

# [國小] (3個)
def elem_chi(): st.title("🍎 國小國語"); st.write("模組內容...")
def elem_eng(): st.title("🔤 國小英語"); st.write("模組內容...")
def elem_mat(): st.title("🔢 國小數學"); st.write("模組內容...")

# [國中] (5個)
def jun_chi(): st.title("📚 國中國文"); st.write("模組內容...")
def jun_eng(): st.title("🌍 國中英文"); st.write("模組內容...")
def jun_mat(): st.title("📐 國中數學"); st.write("模組內容...")
def jun_sci(): st.title("🧪 國中自然"); st.write("模組內容...")
def jun_soc(): st.title("🏛️ 國中社會"); st.write("模組內容...")

# [高中] (完整 10 個獨立模組)
def sen_chi(): st.title("🎭 高中國文"); st.write("專屬解碼內容...")
def sen_eng(): st.title("📑 高中英文"); st.write("專屬解碼內容...")
def sen_mat(): st.title("📉 高中數學"); st.write("專屬解碼內容...")
def sen_bio(): st.title("🧬 高中生物"); st.write("專屬解碼內容...")
def sen_che(): st.title("🧪 高中化學"); st.write("專屬解碼內容...")
def sen_esc(): st.title("🪐 高中地科"); st.write("專屬解碼內容...")
def sen_phy(): st.title("⚡ 高中物理"); st.write("專屬解碼內容...")
def sen_geo(): st.title("🗺️ 高中地理"); st.write("專屬解碼內容...")
def sen_his(): st.title("📜 高中歷史"); st.write("專屬解碼內容...")
def sen_civ(): st.title("⚖️ 高中公民"); st.write("專屬解碼內容...")

# --- 2. 主程式 ---

def main():
    # --- Era Gateway ---
    OLD_ERA_URL = "https://etymon-universe.streamlit.app/"
    st.sidebar.title("Era Gateway")
    
    col_old, col_new = st.sidebar.columns(2)
    with col_old:
        if st.sidebar.button("舊世代", use_container_width=True):
            st.components.v1.html(f"<script>window.open('{OLD_ERA_URL}', '_self')</script>", height=0)
    with col_new:
        st.sidebar.button("新世代", disabled=True, use_container_width=True)
    
    st.sidebar.markdown(f'[手動進入舊宇宙]({OLD_ERA_URL})')
    st.sidebar.divider()

    # --- 第一層：教育宇宙 ---
    universe = st.sidebar.selectbox(
        "🚀 選擇教育宇宙",
        ["請選擇學段", "國小宇宙", "國中宇宙", "高中宇宙"]
    )

    if universe == "請選擇學段":
        st.title("✨ 新世代學科解碼系統")
        st.info("請在左側選單選擇教育階段。")

    else:
        st.write(f"### {universe} | 學科模組導覽")
        
        # --- 第二層：全按鈕式選單 (Mapping 邏輯) ---
        if universe == "國小宇宙":
            sub_tab = st.radio("選擇科目", ["國語", "英語", "數學"], horizontal=True)
            mapping = {"國語": elem_chi, "英語": elem_eng, "數學": elem_mat}
            st.divider()
            mapping[sub_tab]()

        elif universe == "國中宇宙":
            sub_tab = st.radio("選擇科目", ["國文", "英文", "數學", "自然", "社會"], horizontal=True)
            mapping = {"國文": jun_chi, "英文": jun_eng, "數學": jun_mat, "自然": jun_sci, "社會": jun_soc}
            st.divider()
            mapping[sub_tab]()

        elif universe == "高中宇宙":
            # 這裡完整列出你指定的 10 個科目
            sub_tab = st.radio(
                "選擇科目", 
                ["國文", "英文", "數學", "生物", "化學", "地科", "物理", "地理", "歷史", "公民"], 
                horizontal=True
            )
            mapping = {
                "國文": sen_chi, "英文": sen_eng, "數學": sen_mat, "生物": sen_bio,
                "化學": sen_che, "地科": sen_esc, "物理": sen_phy, "地理": sen_geo,
                "歷史": sen_his, "公民": sen_civ
            }
            st.divider()
            mapping[sub_tab]()

if __name__ == "__main__":
    main()
