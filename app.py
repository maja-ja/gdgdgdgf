import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

# ==========================================
# 1. 更精細的三段式資料庫
# ==========================================
@st.cache_data
def get_pro_data():
    data = [
        # AI 科技
        {"word": "neuromorphic", "p": "neuro", "r": "morph", "s": "ic", "p_m": "神經", "r_m": "形狀", "s_m": "形容詞尾", "def": "類神經型態的", "vibe": "硬體層級模擬大腦，不只是演算法，是『數位大腦』的實體化。"},
        {"word": "hyperdimensional", "p": "hyper", "r": "dimens", "s": "ional", "p_m": "超越", "r_m": "測量", "s_m": "相關的", "def": "高維向量空間的", "vibe": "在萬千維度中尋找語義的座標，這是大型語言模型理解世界的本質。"},
        {"word": "autopoietic", "p": "auto", "r": "poie", "s": "tic", "p_m": "自我", "r_m": "創造", "s_m": "屬性", "def": "自我生成的", "vibe": "系統不假外求，像生命體一樣自我修復與演化，這是強人工智慧的終極聖盃。"},
        
        # 高階寫作
        {"word": "intertextuality", "p": "inter", "r": "text", "s": "uality", "p_m": "之間", "r_m": "編織", "s_m": "性質", "def": "文本互涉性", "vibe": "世上沒有原創，只有無窮無盡的引用與拼貼，所有文章都在彼此對話。"},
        {"word": "epistemological", "p": "epistemo", "r": "log", "s": "ical", "p_m": "知識", "r_m": "研究", "s_m": "形容詞", "def": "認識論的", "vibe": "這是在質疑現實的根基：我們憑什麼相信我們所觀察到的真相？"},
        {"word": "defamiliarization", "p": "de", "r": "familiar", "s": "ization", "p_m": "除去", "r_m": "熟悉", "s_m": "過程", "def": "陌生化手法", "vibe": "把日常變成奇觀，強迫讀者跳脫自動導航模式，重新凝視世界。"},

        # 醫學/法研/公務
        {"word": "idiopathic", "p": "idio", "r": "path", "s": "ic", "p_m": "個體", "r_m": "疾病", "s_m": "特徵", "def": "特發性的 (病因不明)", "vibe": "醫學上的優雅投降：知道生病了，但宇宙仍保守著發病的祕密。"},
        {"word": "jurisdictional", "p": "juris", "r": "dict", "s": "ional", "p_m": "法律", "r_m": "宣告", "s_m": "範圍", "def": "管轄權的", "vibe": "權力的疆界，定義了誰能在這片土地上落槌定罪。"},
        {"word": "bureaucratic", "p": "bureau", "r": "cratic", "s": "tic", "p_m": "辦事處", "r_m": "統治", "s_m": "特質", "def": "官僚體制的", "vibe": "層級森嚴的精密機器，既能維持秩序，也可能在程序中迷失。"}
    ]
    df = pd.DataFrame(data)
    
    # 分類整理
    prefixes = [{"id": p, "label": p, "m": m} for p, m in df[['p', 'p_m']].drop_duplicates().values]
    roots = [{"id": r, "label": r, "m": m} for r, m in df[['r', 'r_m']].drop_duplicates().values]
    suffixes = [{"id": s, "label": s, "m": m} for s, m in df[['s', 's_m']].drop_duplicates().values]
    
    dictionary = []
    for _, row in df.iterrows():
        dictionary.append({
            "combo": [row['p'], row['r'], row['s']],
            "word": row['word'],
            "p_m": row['p_m'], "r_m": row['r_m'], "s_m": row['s_m'],
            "definition": row['def'], "vibe": row['vibe']
        })
    return {"prefixes": prefixes, "roots": roots, "suffixes": suffixes, "dictionary": dictionary}

# ==========================================
# 2. React 鍵盤操控與三滾輪介面
# ==========================================
def render_keyboard_reactor(payload):
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
            .active-wheel { ring: 3px solid #3B82F6; ring-offset: 4px; border-color: #3B82F6 !important; }
            .wheel-mask { background: linear-gradient(180deg, white 0%, transparent 30%, transparent 70%, white 100%); }
        </style>
    </head>
    <body class="bg-gray-50 flex justify-center">
        <div id="root" class="w-full"></div>
        <script type="text/babel">
            const { useState, useEffect, useRef } = React;
            const DATA = REPLACE_ME;

            const Wheel = ({ items, onSelect, currentId, isActive }) => {
                const ref = useRef(null);
                
                useEffect(() => {
                    const idx = items.findIndex(i => i.id === currentId);
                    if (ref.current) ref.current.scrollTo({ top: idx * 50, behavior: 'smooth' });
                }, [currentId]);

                return (
                    <div className={`relative w-28 h-36 bg-white rounded-2xl border transition-all duration-200 overflow-hidden ${isActive ? 'active-wheel shadow-lg scale-105' : 'border-gray-200 opacity-60'}`}>
                        <div className="absolute top-[43px] left-0 w-full h-[50px] bg-blue-50/50 pointer-events-none"></div>
                        <div ref={ref} className="h-full overflow-y-scroll no-scrollbar py-[43px]">
                            {items.map(item => (
                                <div key={item.id} className="h-[50px] flex flex-col items-center justify-center font-bold text-sm text-gray-700">
                                    <span>{item.label}</span>
                                    <span className="text-[10px] text-gray-400 font-normal">{item.m}</span>
                                </div>
                            ))}
                        </div>
                        <div className="absolute inset-0 wheel-mask pointer-events-none"></div>
                    </div>
                );
            };

            const App = () => {
                const [focusIdx, setFocusIdx] = useState(0); // 0: Prefix, 1: Root, 2: Suffix
                const [sel, setSel] = useState([DATA.prefixes[0].id, DATA.roots[0].id, DATA.suffixes[0].id]);
                const [match, setMatch] = useState(null);

                const move = (dir) => {
                    const cols = [DATA.prefixes, DATA.roots, DATA.suffixes];
                    const currentList = cols[focusIdx];
                    const currentItemId = sel[focusIdx];
                    const currentIdx = currentList.findIndex(i => i.id === currentItemId);
                    
                    let nextIdx = currentIdx + dir;
                    if (nextIdx < 0) nextIdx = 0;
                    if (nextIdx >= currentList.length) nextIdx = currentList.length - 1;
                    
                    const newSel = [...sel];
                    newSel[focusIdx] = currentList[nextIdx].id;
                    setSel(newSel);
                };

                useEffect(() => {
                    const handleKeyDown = (e) => {
                        if (e.key === 'ArrowLeft') setFocusIdx(prev => Math.max(0, prev - 1));
                        if (e.key === 'ArrowRight') setFocusIdx(prev => Math.min(2, prev + 1));
                        if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
                        if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
                    };
                    window.addEventListener('keydown', handleKeyDown);
                    return () => window.removeEventListener('keydown', handleKeyDown);
                }, [focusIdx, sel]);

                useEffect(() => {
                    const found = DATA.dictionary.find(d => d.combo.every((val, i) => val === sel[i]));
                    setMatch(found);
                }, [sel]);

                return (
                    <div className="p-10 flex flex-col items-center space-y-12 outline-none" tabIndex="0">
                        <div className="text-center">
                            <h2 className="text-xs font-black text-blue-400 uppercase tracking-[0.3em] mb-2">Navigator</h2>
                            <p className="text-gray-400 text-sm">Use ← → to select column, ↑ ↓ to spin</p>
                        </div>

                        <div className="flex items-center gap-4">
                            <Wheel items={DATA.prefixes} onSelect={(id) => {}} currentId={sel[0]} isActive={focusIdx === 0} />
                            <div className="text-gray-200">+</div>
                            <Wheel items={DATA.roots} onSelect={(id) => {}} currentId={sel[1]} isActive={focusIdx === 1} />
                            <div className="text-gray-200">+</div>
                            <Wheel items={DATA.suffixes} onSelect={(id) => {}} currentId={sel[2]} isActive={focusIdx === 2} />
                        </div>

                        <div className="w-full max-w-2xl min-h-[300px]">
                            {match ? (
                                <div className="bg-white rounded-[2rem] shadow-2xl border border-gray-100 overflow-hidden">
                                    <div className="bg-slate-900 p-8 text-white">
                                        <h1 className="text-5xl font-black mb-2 tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
                                            {match.word}
                                        </h1>
                                        <div className="flex gap-2">
                                            <span className="px-3 py-1 bg-white/10 rounded text-xs font-mono">{match.p_m}</span>
                                            <span className="px-3 py-1 bg-white/10 rounded text-xs font-mono">{match.r_m}</span>
                                            <span className="px-3 py-1 bg-white/10 rounded text-xs font-mono">{match.s_m}</span>
                                        </div>
                                    </div>
                                    <div className="p-8 space-y-6">
                                        <div>
                                            <h4 className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-2">Core Definition</h4>
                                            <p className="text-2xl font-bold text-slate-800">{match.definition}</p>
                                        </div>
                                        <div className="bg-blue-50 p-6 rounded-2xl border-l-4 border-blue-500">
                                            <h4 className="text-[10px] font-bold text-blue-400 uppercase tracking-widest mb-1">Deep Logic</h4>
                                            <p className="text-slate-600 leading-relaxed italic">"{match.vibe}"</p>
                                        </div>
                                    </div>
                                </div>
                            ) : (
                                <div className="h-64 border-2 border-dashed border-gray-200 rounded-[2rem] flex items-center justify-center text-gray-300 font-medium">
                                    Waiting for valid synthesis...
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
    
    components.html(html_code, height=850)

# ==========================================
# 3. Streamlit 運行
# ==========================================
st.set_page_config(page_title="Etymon Reactor", layout="wide")
st.title("🔬 語義解碼反應爐 v3.0")
payload = get_pro_data()
render_keyboard_reactor(payload)