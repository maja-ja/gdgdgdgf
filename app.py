import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

# ==========================================
# 1. 核心配置與資料 (The Brain)
# ==========================================
st.set_page_config(page_title="Etymon Decoder Hybrid", layout="wide")

@st.cache_data
def get_full_data():
    # 這裡包含所有字卡需要的細節資訊
    data = [
        {"word": "distract", "p": "dis", "r": "tract", "meaning": "抽/拉", "definition": "使分心", "vibe": "像是有東西硬生生把你從軌道上拉走。", "phonetic": "dɪˈstrækt"},
        {"word": "transform", "p": "trans", "r": "form", "meaning": "形狀", "definition": "轉化/變形", "vibe": "徹底的改變，像毛毛蟲變蝴蝶。", "phonetic": "trænsˈfɔːrm"},
        {"word": "attract", "p": "at", "r": "tract", "meaning": "抽/拉", "definition": "吸引", "vibe": "像磁鐵般的引力把你拉近。", "phonetic": "əˈtrækt"},
        {"word": "predict", "p": "pre", "r": "dict", "meaning": "說", "definition": "預測", "vibe": "在事情發生前就先說出來。", "phonetic": "prɪˈdɪkt"},
        {"word": "revoke", "p": "re", "r": "voke", "meaning": "喊叫", "definition": "撤銷", "vibe": "把說出去的話喊回來，使其無效。", "phonetic": "rɪˈvoʊk"}
    ]
    df = pd.DataFrame(data)
    
    # 格式化給 React 的資料
    prefixes = [{"id": p, "label": f"{p}-"} for p in sorted(df['p'].unique())]
    roots = [{"id": r, "label": f"-{r}"} for r in sorted(df['r'].unique())]
    
    # 將每一筆資料都變成字典格式
    dictionary = []
    for _, row in df.iterrows():
        dictionary.append({
            "combo": [row['p'], row['r']],
            "word": row['word'],
            "definition": row['definition'],
            "phonetic": row['phonetic'],
            "root_mean": row['meaning'],
            "vibe": row['vibe'],
            "display": f"{row['p']} + {row['r']}"
        })
        
    return {"prefixes": prefixes, "roots": roots, "dictionary": dictionary}

# ==========================================
# 2. React 滾輪 + 字卡整合 (The Frontend)
# ==========================================
def render_unified_interface(payload):
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
            .no-scrollbar::-webkit-scrollbar { display: none; }
            .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
            
            /* 滾輪遮罩優化：讓邊緣更透明，減少視覺壓迫 */
            .wheel-mask {
                background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 25%, rgba(255,255,255,0) 75%, rgba(255,255,255,1) 100%);
            }
            
            /* 字卡滑入動畫 */
            .card-enter {
                animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
            }
            @keyframes slideUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body class="bg-gray-50">
        <div id="root"></div>
        <script type="text/babel">
            const { useState, useEffect, useRef } = React;
            const DATA = REPLACE_ME;

            const Wheel = ({ items, onSelect, currentId }) => {
                const ref = useRef(null);
                
                // 處理滾動邏輯
                const handleScroll = () => {
                    if (!ref.current) return;
                    const idx = Math.round(ref.current.scrollTop / 50);
                    if (items[idx] && items[idx].id !== currentId) {
                        onSelect(items[idx].id);
                    }
                };

                return (
                    <div className="relative w-32 h-36 bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                        {/* 選中高亮條 */}
                        <div className="absolute top-[50px] left-0 w-full h-[50px] bg-blue-50/50 border-y border-blue-100 pointer-events-none"></div>
                        
                        {/* 滾動內容 */}
                        <div 
                            ref={ref} 
                            onScroll={handleScroll} 
                            className="h-full overflow-y-scroll snap-y snap-mandatory no-scrollbar py-[50px]"
                        >
                            {items.map(item => (
                                <div key={item.id} className="h-[50px] flex items-center justify-center snap-center font-bold text-xl text-gray-600">
                                    {item.label}
                                </div>
                            ))}
                        </div>
                        
                        {/* 漸變遮罩 */}
                        <div className="absolute inset-0 wheel-mask pointer-events-none"></div>
                    </div>
                );
            };

            const App = () => {
                const [p, setP] = useState(DATA.prefixes[0].id);
                const [r, setR] = useState(DATA.roots[0].id);
                const [match, setMatch] = useState(null);

                useEffect(() => {
                    const found = DATA.dictionary.find(d => d.combo[0] === p && d.combo[1] === r);
                    setMatch(found);
                }, [p, r]);

                return (
                    <div className="pt-6 pb-20 px-6 max-w-4xl mx-auto flex flex-col items-center">
                        
                        {/* 滾輪控制區：使用 flex-col 確保與下方字卡徹底切開 */}
                        <div className="flex items-center gap-6 mb-16 relative z-10">
                            <Wheel items={DATA.prefixes} onSelect={setP} currentId={p} />
                            <div className="text-3xl text-gray-300 font-light">+</div>
                            <Wheel items={DATA.roots} onSelect={setR} currentId={r} />
                        </div>

                        {/* 字卡顯示區：設定為 w-full 並增加 padding 防止重疊 */}
                        <div className="w-full min-h-[400px] relative z-0">
                        {match ? (
                            <div className="bg-white rounded-[2.5rem] shadow-2xl overflow-hidden border border-gray-100 card-enter">
                                {/* 字卡頭部 */}
                                <div className="bg-gradient-to-br from-blue-600 to-indigo-700 p-10 text-white">
                                    <div className="flex justify-between items-start">
                                        <div className="space-y-2">
                                            <h1 className="text-6xl font-black tracking-tight drop-shadow-sm">
                                                {match.word}
                                            </h1>
                                            <p className="text-blue-100 text-2xl font-mono tracking-wider opacity-90">
                                                /{match.phonetic}/
                                            </p>
                                        </div>
                                        <div className="bg-white/15 backdrop-blur-xl border border-white/20 px-6 py-2 rounded-2xl font-bold uppercase tracking-[0.2em] text-xs shadow-sm">
                                            {match.display}
                                        </div>
                                    </div>
                                </div>
                                
                                {/* 字卡內容 */}
                                <div className="p-10 grid md:grid-cols-2 gap-10 bg-white">
                                    <div className="space-y-4">
                                        <div className="flex items-center gap-2 text-gray-400">
                                            <span className="text-lg">🗝️</span>
                                            <h3 className="font-bold uppercase tracking-widest text-xs">Etymology Breakdown</h3>
                                        </div>
                                        <div className="bg-amber-50/50 p-7 rounded-[2rem] border-l-4 border-amber-400">
                                            <p className="text-amber-900 text-2xl leading-snug">
                                                The root <span className="font-black text-amber-600 underline decoration-amber-200 underline-offset-4">"{r}"</span> means <span className="font-bold italic">{match.root_mean}</span>.
                                            </p>
                                            <div className="mt-4 pt-4 border-t border-amber-200/50 text-amber-800 text-lg">
                                                <span className="opacity-60 text-sm block mb-1">MEANING</span>
                                                <span className="font-bold">{match.definition}</span>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="space-y-4">
                                        <div className="flex items-center gap-2 text-gray-400">
                                            <span className="text-lg">🎧</span>
                                            <h3 className="font-bold uppercase tracking-widest text-xs">Native Vibe</h3>
                                        </div>
                                        <div className="bg-blue-50/50 p-7 rounded-[2rem] border-l-4 border-blue-400 h-full">
                                            <p className="text-blue-900 text-xl leading-relaxed italic font-medium">
                                                "{match.vibe}"
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="h-[350px] border-4 border-dashed border-gray-200 rounded-[3rem] flex flex-col items-center justify-center text-gray-300 space-y-4 bg-white/50">
                                <div className="text-5xl animate-pulse">🧬</div>
                                <span className="text-xl font-semibold tracking-wide">Spin the wheels to decode...</span>
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
    
    # 高度調整
    components.html(html_code, height=850, scrolling=False)
# ==========================================
# 3. 啟動 (The Launch)
# ==========================================
def main():
    st.title("🧬 Etymon Decoder 2.0")
    st.markdown("轉動滾輪即時解碼單字語源與語感。")
    
    data_payload = get_full_data()
    render_unified_interface(data_payload)

if __name__ == "__main__":
    main()