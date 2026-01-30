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
            .wheel-mask {
                background: linear-gradient(180deg, white 0%, transparent 40%, transparent 60%, white 100%);
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
                const handleScroll = () => {
                    const idx = Math.round(ref.current.scrollTop / 50);
                    if (items[idx] && items[idx].id !== currentId) onSelect(items[idx].id);
                };
                return (
                    <div className="relative w-32 h-40 bg-white rounded-xl shadow-inner border overflow-hidden">
                        <div className="absolute top-1/2 left-0 w-full h-10 -translate-y-1/2 bg-blue-50 border-y border-blue-200 pointer-events-none"></div>
                        <div ref={ref} onScroll={handleScroll} className="h-full overflow-y-scroll snap-y snap-mandatory no-scrollbar py-16">
                            {items.map(item => (
                                <div key={item.id} className="h-[50px] flex items-center justify-center snap-center font-bold text-lg text-gray-700">
                                    {item.label}
                                </div>
                            ))}
                        </div>
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
                    <div className="p-6 max-w-4xl mx-auto space-y-8">
                        {/* 滾輪區域 */}
                        <div className="flex justify-center items-center gap-8">
                            <Wheel items={DATA.prefixes} onSelect={setP} currentId={p} />
                            <div className="text-4xl text-gray-300 font-light">+</div>
                            <Wheel items={DATA.roots} onSelect={setR} currentId={r} />
                        </div>

                        {/* 動態字卡區域 */}
                        <div className="min-h-[300px]">
                        {match ? (
                            <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100 transition-all duration-500 transform translate-y-0">
                                <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-8 text-white">
                                    <div className="flex justify-between items-center">
                                        <div>
                                            <h1 className="text-5xl font-black tracking-tight">{match.word}</h1>
                                            <p className="text-blue-100 text-xl mt-2 font-mono">/{match.phonetic}/</p>
                                        </div>
                                        <div className="bg-white/20 backdrop-blur-md px-4 py-2 rounded-full font-bold uppercase tracking-widest text-sm">
                                            {match.display}
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="p-8 grid md:grid-cols-2 gap-8 bg-white">
                                    <div className="space-y-4">
                                        <h3 className="text-gray-400 font-bold uppercase tracking-wider text-sm">🗝️ Etymology Breakdown</h3>
                                        <div className="bg-amber-50 p-6 rounded-2xl border-l-4 border-amber-400">
                                            <p className="text-amber-900 text-xl leading-relaxed">
                                                The root <span className="font-black underline">"{r}"</span> means <span className="font-bold text-amber-700">{match.root_mean}</span>.
                                            </p>
                                            <p className="text-amber-700 mt-2">Combined as: <b>{match.definition}</b></p>
                                        </div>
                                    </div>
                                    <div className="space-y-4">
                                        <h3 className="text-gray-400 font-bold uppercase tracking-wider text-sm">🎧 Native Vibe</h3>
                                        <div className="bg-blue-50 p-6 rounded-2xl border-l-4 border-blue-400">
                                            <p className="text-blue-900 text-lg leading-relaxed italic">
                                                "{match.vibe}"
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="h-[300px] border-4 border-dashed border-gray-200 rounded-3xl flex items-center justify-center text-gray-400 text-xl font-medium">
                                🌀 Spin the wheels to decode a word...
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
    
    components.html(html_code, height=650, scrolling=False)

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