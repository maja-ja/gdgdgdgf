import streamlit as st

# --- 1. 獨立學科模組 (Def) ---
def elem_chi(): st.title("🍎 國小國語"); st.write("模組內容...")
def elem_eng(): st.title("🔤 國小英語"); st.write("模組內容...")
def elem_mat(): st.title("🔢 國小數學"); st.write("模組內容...")

def jun_chi(): st.title("📚 國中國文"); st.write("模組內容...")
def jun_eng(): st.title("🌍 國中英文"); st.write("模組內容...")
def jun_mat(): st.title("📐 國中數學"); st.write("模組內容...")
def jun_sci(): st.title("🧪 國中自然"); st.write("模組內容...")
def jun_soc(): st.title("🏛️ 國中社會"); st.write("模組內容...")

def sen_chi(): st.title("🎭 高中國文"); st.write("解碼內容...")
def sen_eng(): st.title("📑 高中英文"); st.write("解碼內容...")
def sen_mat(): st.title("📉 高中數學"); st.write("解碼內容...")
def sen_bio(): st.title("🧬 高中生物"); st.write("解碼內容...")
def sen_che(): st.title("🧪 高中化學"); st.write("解碼內容...")
def sen_esc(): st.title("🪐 高中地科"); st.write("解碼內容...")
def sen_phy(): st.title("⚡ 高中物理"); st.write("解碼內容...")
def sen_geo(): st.title("🗺️ 高中地理"); st.write("解碼內容...")
def sen_his(): st.title("📜 高中歷史"); st.write("解碼內容...")
def sen_civ(): st.title("⚖️ 高中公民"); st.write("解碼內容...")

# --- 2. 主程式 ---
def main():
    # 初始化宇宙選擇狀態
    if 'universe_choice' not in st.session_state:
        st.session_state.universe_choice = "請選擇學段"

    OLD_ERA_URL = "https://etymon-universe.streamlit.app/"

    # --- Era Gateway (側邊欄) ---
    st.sidebar.title("Era Gateway")
    
    col_a, col_b = st.sidebar.columns(2)
    with col_a:
        # 使用 HTML 連結代替 JS 按鈕，完全避免「重定向次數過多」的問題
        st.markdown(f'''
            <a href="{OLD_ERA_URL}" target="_self" style="text-decoration: none;">
                <button style="width: 100%; cursor: pointer; background-color: transparent; border: 1px solid #4B4B4B; color: white; padding: 5px; border-radius: 5px;">
                    舊世代
                </button>
            </a>
        ''', unsafe_allow_html=True)
    with col_b:
        # 「新世代」按鈕改為：強制重置目前的 App 狀態到首頁
        if st.button("新世代", use_container_width=True):
            st.session_state.universe_choice = "請選擇學段"
            st.rerun()

    st.sidebar.divider()

    # --- 主導覽 (使用 Session State 綁定) ---
    universe = st.sidebar.selectbox(
        "🚀 選擇教育宇宙",
        ["請選擇學段", "國小宇宙", "國中宇宙", "高中宇宙"],
        key="universe_selector",
        index=["請選擇學段", "國小宇宙", "國中宇宙", "高中宇宙"].index(st.session_state.universe_choice)
    )
    # 同步狀態
    st.session_state.universe_choice = universe

    if universe == "請選擇學段":
        st.title("✨ 新世代學科解碼系統")
        st.info("請在左側選單選擇教育階段。")
    else:
        st.write(f"### {universe} | 學科模組導覽")
        
        if universe == "國小宇宙":
            sub = st.radio("選擇科目", ["國語", "英語", "數學"], horizontal=True)
            st.divider()
            maps = {"國語": elem_chi, "英語": elem_eng, "數學": elem_mat}
            maps[sub]()

        elif universe == "國中宇宙":
            sub = st.radio("選擇科目", ["國文", "英文", "數學", "自然", "社會"], horizontal=True)
            st.divider()
            maps = {"國文": jun_chi, "英文": jun_eng, "數學": jun_mat, "自然": jun_sci, "社會": jun_soc}
            maps[sub]()

        elif universe == "高中宇宙":
            sub = st.radio("選擇科目", ["國文", "英文", "數學", "生物", "化學", "地科", "物理", "地理", "歷史", "公民"], horizontal=True)
            st.divider()
            maps = {
                "國文": sen_chi, "英文": sen_eng, "數學": sen_mat, "生物": sen_bio,
                "化學": sen_che, "地科": sen_esc, "物理": sen_phy, "地理": sen_geo,
                "歷史": sen_his, "公民": sen_civ
            }
            maps[sub]()

if __name__ == "__main__":
    main()
