import streamlit as st

# --- 1. 定義模組化學科函式 (獨立 def) ---

# 國小組
def primary_chi(): st.title("國小國語"); st.write("模組內容：識字與閱讀")
def primary_eng(): st.title("國小英語"); st.write("模組內容：聽力與口說")
def primary_math(): st.title("國小數學"); st.write("模組內容：數與量")

# 國中組
def junior_chi(): st.title("國中國文"); st.write("模組內容：古文與修辭")
def junior_eng(): st.title("國中英文"); st.write("模組內容：文法與克漏字")
def junior_math(): st.title("國中數學"); st.write("模組內容：幾何與函數")
def junior_sci(): st.title("國中自然"); st.write("模組內容：理化與生物")
def junior_soc(): st.title("國中社會"); st.write("模組內容：史地與公民")

# 高中組 (至多 8 頁)
def senior_chi(): st.title("高中國文"); st.write("高階思辨模組")
def senior_eng(): st.title("高中英文"); st.write("核心單字與寫作")
def senior_math(): st.title("高中數學"); st.write("微積分與機率")
def senior_phy(): st.title("高中物理"); st.write("力學實驗模擬")
def senior_che(): st.title("高中化學"); st.write("元素週期表應用")
def senior_bio(): st.title("高中生物"); st.write("遺傳與生命科學")
def senior_earth(): st.title("高中地科"); st.write("天文與大氣")
def senior_integrated(): st.title("高中社會跨科"); st.write("歷公地整合議題")

# --- 2. 主程式 ---

def main():
    # --- Gateway 設定 (依您截圖的需求) ---
    OLD_ERA_URL = "https://etymon-universe.streamlit.app/"
    
    st.sidebar.title("Era Gateway")
    c1, c2 = st.sidebar.columns(2)
    with c1:
        if st.sidebar.button("舊世代", use_container_width=True):
            st.components.v1.html(f"<script>window.open('{OLD_ERA_URL}', '_self')</script>", height=0)
    with c2:
        st.sidebar.button("新世代", disabled=True, use_container_width=True)
    
    st.sidebar.markdown(f'[手動進入舊宇宙]({OLD_ERA_URL})')
    st.sidebar.divider()

    # --- App 主選單邏輯 ---
    
    # 步驟 A: 選擇學層 (主選單)
    universe = st.selectbox(
        "🚀 請選擇教育宇宙 (主邏輯)",
        ["請選擇", "國小宇宙", "國中宇宙", "高中宇宙", "重新開始"],
        index=0
    )

    if universe == "重新開始":
        st.rerun()

    if universe == "請選擇":
        st.title("✨ 新世代學科解碼系統")
        st.info("請使用上方選單進入對應學層。")
    
    else:
        # 步驟 B: 根據學層顯示對應的 App 選單 (次級邏輯)
        st.divider()
        
        if universe == "國小宇宙":
            tab_choice = st.radio("學科模組", ["國語", "英語", "數學"], horizontal=True)
            mapping = {"國語": primary_chi, "英語": primary_eng, "數學": primary_math}
            mapping[tab_choice]() # 執行對應的 def

        elif universe == "國中宇宙":
            tab_choice = st.radio("學科模組", ["國文", "英文", "數學", "自然", "社會"], horizontal=True)
            mapping = {"國文": junior_chi, "英文": junior_eng, "數學": junior_math, "自然": junior_sci, "社會": junior_soc}
            mapping[tab_choice]()

        elif universe == "高中宇宙":
            # 高中 8 頁限制，使用 Selectbox 或 Radio 均可
            tab_choice = st.selectbox("選擇學科頁面 (至多8頁)", 
                                    ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "社會跨科"])
            mapping = {
                "國文": senior_chi, "英文": senior_eng, "數學": senior_math, 
                "物理": senior_phy, "化學": senior_che, "生物": senior_bio, 
                "地科": senior_earth, "社會跨科": senior_integrated
            }
            mapping[tab_choice]()

if __name__ == "__main__":
    main()
