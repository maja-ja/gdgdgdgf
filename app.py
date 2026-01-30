import streamlit as st

# --- 1. 獨立學科模組 (各學科一個獨立 def) ---
# [國小]
def elem_chi(): st.title("🍎 國小國語"); st.write("模組內容...")
def elem_eng(): st.title("🔤 國小英語"); st.write("模組內容...")
def elem_mat(): st.title("🔢 國小數學"); st.write("模組內容...")

# [國中]
def jun_chi(): st.title("📚 國中國文"); st.write("模組內容...")
def jun_eng(): st.title("🌍 國中英文"); st.write("模組內容...")
def jun_mat(): st.title("📐 國中數學"); st.write("模組內容...")
def jun_sci(): st.title("🧪 國中自然"); st.write("模組內容...")
def jun_soc(): st.title("🏛️ 國中社會"); st.write("模組內容...")

# [高中] (10個)
def sen_chi(): st.title("🎭 高中國文"); st.write("專屬內容...")
def sen_eng(): st.title("📑 高中英文"); st.write("專屬內容...")
def sen_mat(): st.title("📉 高中數學"); st.write("專屬內容...")
def sen_bio(): st.title("🧬 高中生物"); st.write("專屬內容...")
def sen_che(): st.title("🧪 高中化學"); st.write("專屬內容...")
def sen_esc(): st.title("🪐 高中地科"); st.write("專屬內容...")
def sen_phy(): st.title("⚡ 高中物理"); st.write("專屬內容...")
def sen_geo(): st.title("🗺️ 高中地理"); st.write("專屬內容...")
def sen_his(): st.title("📜 高中歷史"); st.write("專屬內容...")
def sen_civ(): st.title("⚖️ 高中公民"); st.write("專屬內容...")

# --- 2. 主程式 ---

def main():
    # 定義跳轉網址
    OLD_ERA_URL = "https://etymon-universe.streamlit.app"

    # --- Era Gateway (側邊欄) ---
    st.sidebar.title("Era Gateway")
    
    c1, c2 = st.sidebar.columns(2)
    with c1:
        # 修正：增加跳轉邏輯
        if st.button("舊世代", use_container_width=True):
            js = f"window.open('{OLD_ERA_URL}', '_self')"
            st.components.v1.html(f"<script>{js}</script>", height=0)
            st.stop() # 停止後續渲染
    with c2:
        # 新世代按鈕：點擊可強制回首頁 (重置)
        if st.button("新世代", use_container_width=True):
            st.rerun()

    st.sidebar.markdown(f'<a href="{OLD_ERA_URL}" target="_self" style="color: #58a6ff; text-decoration: none;">手動返回舊宇宙</a>', unsafe_allow_html=True)
    st.sidebar.divider()

    # --- 主導覽邏輯 ---
    universe = st.sidebar.selectbox(
        "🚀 選擇教育宇宙",
        ["請選擇學段", "國小宇宙", "國中宇宙", "高中宇宙"],
        key="main_nav" # 固定 key 確保狀態一致
    )

    if universe == "請選擇學段":
        st.title("✨ 新世代學科解碼系統")
        st.info("請在左側選單選擇教育階段。")
    else:
        st.write(f"### {universe} | 學科模組導覽")
        
        # 根據 universe 顯示按鈕
        if universe == "國小宇宙":
            sub = st.radio("選擇科目", ["國語", "英語", "數學"], horizontal=True)
            st.divider()
            maps = {"國語": elem_chi, "英語": elem_eng, "數學": elem_mat}
            maps[sub]()

        elif universe == "國中宇宙":
            sub = st.radio("選擇科目", ["國文", "英文", "數學", "自然", "社會"], horizontal=True)
            st.divider()
            maps = {"國文": junior_chinese, "英文": junior_english, "數學": junior_math, "自然": junior_science, "社會": junior_social}
            # 注意：這裡需對應你上面定義的 def 名稱
            if sub == "國文": jun_chi()
            elif sub == "英文": jun_eng()
            elif sub == "數學": jun_mat()
            elif sub == "自然": jun_sci()
            elif sub == "社會": jun_soc()

        elif universe == "高中宇宙":
            sub = st.radio(
                "選擇科目", 
                ["國文", "英文", "數學", "生物", "化學", "地科", "物理", "地理", "歷史", "公民"], 
                horizontal=True
            )
            st.divider()
            # 建立映射表
            maps = {
                "國文": sen_chi, "英文": sen_eng, "數學": sen_mat, "生物": sen_bio,
                "化學": sen_che, "地科": sen_esc, "物理": sen_phy, "地理": sen_geo,
                "歷史": sen_his, "公民": sen_civ
            }
            maps[sub]()

if __name__ == "__main__":
    main()
