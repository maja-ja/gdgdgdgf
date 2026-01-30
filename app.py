import streamlit as st
import json
import streamlit.components.v1 as components

# ==========================================
# 1. 配置與資料準備
# ==========================================
st.set_page_config(page_title="Etymon Decoder Final", layout="wide")

@st.cache_data
def get_data():
    # 這裡定義滾輪選項和字典資料
    # 為了完全符合截圖，我們精確定義每個欄位
    prefixes = [
        {"id": "bureau", "label": "bureau-"},
        {"id": "auto", "label": "auto-"},
        {"id": "de", "label": "de-"},
        {"id": "pre", "label": "pre-"},
        {"id": "re", "label": "re-"},
        {"id": "trans", "label": "trans-"},
        {"id": "dis", "label": "dis-"},
    ]
    roots = [
        {"id": "cratic", "label": "-cratic"},
        {"id": "dictional", "label": "-dictional"},
        {"id": "form", "label": "-form"},
        {"id": "tract", "label": "-tract"},
        {"id": "voke", "label": "-voke"},
    ]
    
    # 字典匹配資料
    dictionary = [
        {
            "p_id": "bureau", "r_id": "cratic",
            "word": "bureaucratic",
            "phonetic": "/ˌbjʊərəˈkrætɪk/",
            "combo_display": "BUREAU + CRATIC",
            # 語源拆解區資料
            "root_highlight": "cratic",
            "root_meaning": "統治/力量",
            "final_meaning": "官僚體制的",
            # 語感區資料
            "vibe": "描述一種依賴複雜程序、層級嚴密但有時顯得僵化的行政系統。"
        },
        {
            "p_id": "dis", "r_id": "tract",
            "word": "distract",
            "phonetic": "/dɪˈstrækt/",
            "combo_display": "DIS + TRACT",
            "root_highlight": "tract",
            "root_meaning": "抽/拉",
            "final_meaning": "使分心",
            "vibe": "像是有東西硬生生把你從軌道上拉走。"
        },
         {
            "p_id": "re", "r_id": "voke",
            "word": "revoke",
            "phonetic": "/rɪˈvoʊk/",
            "combo_display": "RE + VOKE",
            "root_highlight": "voke",
            "root_meaning": "喊叫",
            "final_meaning": "撤銷",
            "vibe": "把說出去的話喊回來，使其無效。"
        },
        {
            "p_id": "trans", "r_id": "form",
            "word": "transform",
            "phonetic": "/trænsˈfɔːrm/",
            "combo_display": "TRANS + FORM",
            "root_highlight": "form",
            "root_meaning": "形狀",
            "final_meaning": "轉化/變形",
            "vibe": "徹底的改變，像毛毛蟲變蝴蝶。"
        }
        # 可以繼續添加更多組合...
    ]
    
    return {"prefixes": prefixes, "roots": roots, "dictionary": dictionary}

# ==========================================
# 2. React 前端元件 (包含滾輪與字卡)
# ==========================================
def render_ui(payload):
    json_data = json.dumps(payload)
    
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            /* 隱藏滾動條 */
            .no-scrollbar::-webkit-scrollbar { display: none; }
            .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
            
            /* 滾輪上下遮罩 */
            .wheel-mask {
                background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 30%, rgba(255,255,255,0) 70%, rgba(255,255,255,1) 100%);
            }
            
            /* 字卡進入動畫 */
            .card-enter { animation: slideUpFade 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
            @keyframes slideUpFade {
                from { opacity: 0; transform: translateY(20px) scale(0.98); }
                to { opacity: 1; transform: translateY(0) scale(1); }
            }
        </style>
    </head>
    <body class="bg-transparent">
        <div id="root"></div>
        <script type="text/babel">
            const { useState, useEffect, useRef } = React;
            const DATA = REPLACE_ME;
            const ITEM_HEIGHT = 60; // 滾輪每個選項的高度

            // --- 滾輪元件 ---
            const Wheel = ({ items, onSelect, currentId }) => {
                const ref = useRef(null);
                
                const handleScroll = () => {
                    if (!ref.current) return;
                    const idx = Math.round(ref.current.scrollTop / ITEM_HEIGHT);
                    if (items[idx] && items[idx].id !== currentId) {
                        onSelect(items[idx].id);
                    }
                };

                return (
                    <div className="relative w-40 h-[180px] bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
                        {/* 中央選取框 */}
                        <div className="absolute top-[60px] left-0 w-full h-[60px] bg-blue-50/80 border-y border-blue-100 pointer-events-none"></div>
                        
                        {/* 滾動區域 */}
                        <div 
                            ref={ref} 
                            onScroll={handleScroll} 
                            className="h-full overflow-y-scroll snap-y snap-mandatory no-scrollbar py-[60px]"
                        >
                            {items.map(item => (
                                <div key={item.id} className="h-[60px] flex items-center justify-center snap-center font-bold text-xl text-gray-600">
                                    {item.label}
                                </div>
                            ))}
                        </div>
                        {/* 遮罩 */}
                        <div className="absolute inset-0 wheel-mask pointer-events-none"></div>
                    </div>
                );
            };

            // --- 主應用元件 ---
            const App = () => {
                // 預設選中 bureaucratic 的組合
                const [p, setP] = useState("bureau");
                const [r, setR] = useState("cratic");
                const [match, setMatch] = useState(null);

                // 尋找匹配
                useEffect(() => {
                    const found = DATA.dictionary.find(d => d.p_id === p && d.r_id === r);
                    setMatch(found);
                }, [p, r]);

                return (
                    <div className="py-10 px-4 flex flex-col items-center font-sans">
                        
                        {/* 1. 雙欄滾輪區 */}
                        <div className="flex items-center gap-6 mb-12 relative z-10">
                            <Wheel items={DATA.prefixes} onSelect={setP} currentId={p} />
                            <div className="text-4xl text-gray-300 font-light">+</div>
                            <Wheel items={DATA.roots} onSelect={setR} currentId={r} />
                        </div>

                        {/* 2. 結果字卡區 (完美復刻樣式) */}
                        <div className="w-full max-w-3xl relative z-0 min-h-[400px]">
                        {match ? (
                            <div className="bg-white rounded-[2.5rem] shadow-xl overflow-hidden border border-gray-100 card-enter">
                                {/* 藍色標題頭部 */}
                                <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-8 sm:p-10 text-white relative overflow-hidden">
                                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 relative z-10">
                                        <div>
                                            <h1 className="text-5xl sm:text-6xl font-black tracking-tight drop-shadow-sm mb-2">
                                                {match.word}
                                            </h1>
                                            <p className="text-blue-100 text-xl sm:text-2xl font-mono tracking-wider opacity-90">
                                                {match.phonetic}
                                            </p>
                                        </div>
                                        <div className="bg-white/20 backdrop-blur-md border border-white/20 px-5 py-2 rounded-full font-bold uppercase tracking-widest text-sm shadow-sm whitespace-nowrap">
                                            {match.combo_display}
                                        </div>
                                    </div>
                                </div>
                                
                                {/* 下方雙欄內容 */}
                                <div className="p-8 sm:p-10 grid md:grid-cols-2 gap-8 bg-white">
                                    
                                    {/* 左側：語源拆解 (黃色調) */}
                                    <div className="space-y-3">
                                        <div className="flex items-center gap-2 text-gray-400 mb-2">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                                              <path fillRule="evenodd" d="M15.75 1.5a6.75 6.75 0 0 0-6.651 7.906c.067.39-.032.717-.221.906l-6.5 6.499a3 3 0 0 0-.878 2.121v2.818c0 .414.336.75.75.75H6a.75.75 0 0 0 .75-.75v-1.5h1.5a.75.75 0 0 0 .75-.75v-1.5h1.5a.75.75 0 0 0 .75-.75v-1.5h1.5a.75.75 0 0 0 .75-.75c.311-.31.637-.408 1.028-.34a6.75 6.75 0 1 0 1.002-1.003ZM16.5 5.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" clipRule="evenodd" />
                                            </svg>
                                            <h3 className="font-bold uppercase tracking-widest text-xs">Etymology Breakdown</h3>
                                        </div>
                                        {/* 黃色區塊 */}
                                        <div className="bg-amber-50/80 p-6 rounded-[2rem] border-l-4 border-amber-400 h-full">
                                            <p className="text-amber-900 text-xl leading-snug">
                                                The root <span className="font-black text-amber-600 mx-1 underline decoration-amber-300 underline-offset-4">"{match.root_highlight}"</span> means <span className="font-bold italic">{match.root_meaning}</span>.
                                            </p>
                                            <div className="mt-6 pt-4 border-t border-amber-200/50">
                                                <span className="text-amber-800/70 text-[10px] font-bold uppercase tracking-widest block mb-1">MEANING</span>
                                                <span className="text-amber-900 font-bold text-lg">{match.final_meaning}</span>
                                            </div>
                                        </div>
                                    </div>

                                    {/* 右側：母語語感 (藍色調) */}
                                    <div className="space-y-3">
                                        <div className="flex items-center gap-2 text-gray-400 mb-2">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                                              <path d="M13.5 4.06c0-1.336-1.616-2.005-2.56-1.06l-4.5 4.5H4.508c-1.141 0-2.318.664-2.66 1.905A9.76 9.76 0 0 0 1.5 12c0 .898.121 1.768.35 2.595.341 1.24 1.518 1.905 2.659 1.905h1.93l4.5 4.5c.945.945 2.561.276 2.561-1.06V4.06ZM18.584 5.106a.75.75 0 0 1 1.06 0c3.808 3.807 3.808 9.98 0 13.788a.75.75 0 1 1-1.06-1.06 2.75 2.75 0 0 0 0-11.668.75.75 0 0 1 0-1.06Z" />
                                              <path d="M15.932 7.757a.75.75 0 0 1 1.061 0 6 6 0 0 1 0 8.486.75.75 0 0 1-1.06-1.061 4.5 4.5 0 0 0 0-6.364.75.75 0 0 1 0-1.06Z" />
                                            </svg>
                                            <h3 className="font-bold uppercase tracking-widest text-xs">Native Vibe</h3>
                                        </div>
                                        {/* 藍色區塊 */}
                                        <div className="bg-blue-50/80 p-6 rounded-[2rem] border-l-4 border-blue-400 h-full flex items-center">
                                            <p className="text-blue-900 text-xl leading-relaxed italic font-medium">
                                                “{match.vibe}”
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            // 未匹配時的佔位符
                            <div className="h-[300px] border-4 border-dashed border-gray-200 rounded-[2.5rem] flex flex-col items-center justify-center text-gray-300 space-y-4 bg-white/50">
                                <div className="text-5xl animate-pulse opacity-50">🧬</div>
                                <span className="text-xl font-semibold tracking-wide">Spin to decode...</span>
                            </div>
                        )}
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<App />);
        </script>
    </body>
    </html>
    """.replace("REPLACE_ME", json_data)
    
    # 設定足夠的高度以顯示完整內容
    components.html(html_code, height=850, scrolling=False)

# ==========================================
# 3. 主程式執行
# ==========================================
def main():
    # 隱藏 Streamlit 預設元素，讓畫面更乾淨
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stApp { background-color: #F8F9FA; }
            .block-container { padding-top: 1rem; padding-bottom: 1rem; }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🧬 Etymon Decoder")
    
    data = get_data()
    render_ui(data)

if __name__ == "__main__":
    main()