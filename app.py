import streamlit as st
import pandas as pd
import json
import base64
from io import BytesIO
from gtts import gTTS
import streamlit.components.v1 as components

# ==========================================
# 1. 核心配置與 CSS (The Foundation)
# ==========================================
st.set_page_config(page_title="Etymon Decoder", page_icon="🧬", layout="wide")

def inject_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Noto+Sans+TC:wght@500;700&display=swap');
            .stApp { font-family: 'Inter', 'Noto Sans TC', sans-serif; background-color: #F8F9FA; }
            .block-container { padding-top: 1.5rem; }
            
            /* 讓 Streamlit 的 Selectbox 看起來更現代 */
            .stSelectbox div[data-baseweb="select"] > div {
                border-radius: 12px;
                background-color: white;
                border: 2px solid #E3F2FD;
            }
            
            /* 裝飾性標題 */
            .section-label {
                color: #546E7A;
                font-size: 0.9rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 資料處理 (Python Brain)
# ==========================================
@st.cache_data
def get_data_payload():
    # 模擬資料庫
    data = [
        {"word": "distract", "breakdown": "dis+tract", "roots": "tract", "meaning": "抽/拉", "definition": "使分心", "category": "心理", "native_vibe": "像是有東西硬生生把你從軌道上拉走，注意力被扯開。", "phonetic": "dɪˈstrækt"},
        {"word": "transform", "breakdown": "trans+form", "roots": "form", "meaning": "形狀", "definition": "轉化/變形", "category": "變化", "native_vibe": "從一種型態徹底變成另一種，像變形金剛或毛毛蟲變蝴蝶。", "phonetic": "trænsˈfɔːrm"},
        {"word": "attract", "breakdown": "at+tract", "roots": "tract", "meaning": "抽/拉", "definition": "吸引", "category": "物理/人際", "native_vibe": "像磁鐵一樣，有一股無形的力量把你拉過去。", "phonetic": "əˈtrækt"},
        {"word": "predict", "breakdown": "pre+dict", "roots": "dict", "meaning": "說", "definition": "預測", "category": "時間", "native_vibe": "在事情發生之前(pre)就先斷言(dict)會發生。", "phonetic": "prɪˈdɪkt"},
        {"word": "revoke", "breakdown": "re+voke", "roots": "voke", "meaning": "喊叫", "definition": "撤銷", "category": "法律", "native_vibe": "把已經發出的命令或執照，大聲喊(voke)回來(re)，使其無效。", "phonetic": "rɪˈvoʊk"}
    ]
    df = pd.DataFrame(data)
    
    # 建立 React 需要的滾輪資料
    prefixes, roots, dictionary_map = set(), set(), []
    
    for _, row in df.iterrows():
        parts = row['breakdown'].split('+')
        if len(parts) >= 2:
            p, r = parts[0], parts[1]
            prefixes.add(p)
            roots.add(r)
            dictionary_map.append({
                "combo": [f"p_{p}", f"r_{r}"], 
                "word": row['word'],
                "meaning": row['definition'],
                "display": f"{p} + {r}"
            })
    
    # 為了讓 React 滾輪好操作，我們將所有選項排序
    react_prefixes = [{"id": f"p_{x}", "label": f"{x}-"} for x in sorted(list(prefixes))]
    react_roots = [{"id": f"r_{x}", "label": f"-{x}"} for x in sorted(list(roots))]
    
    return df, {
        "prefixes": react_prefixes, 
        "roots": react_roots, 
        "dictionary": dictionary_map
    }

def text_to_speech_html(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = BytesIO()
        tts.write_to_fp(fp)
        b64 = base64.b64encode(fp.getvalue()).decode()
        return f"""
            <audio id="audio-{text}" src="data:audio/mp3;base64,{b64}"></audio>
            <button onclick="document.getElementById('audio-{text}').play()" style="border:none; background:none; cursor:pointer; font-size:1.5rem;">🔊</button>
        """
    except:
        return "🔊 (Offline)"

# ==========================================
# 3. React 前端組件 (Frontend Skin)
# ==========================================
def render_react_wheel(payload):
    json_data = json.dumps(payload)
    
    # 優化重點：
    # 1. 增加觸覺回饋視覺效果 (Snap scroll)
    # 2. 當匹配成功時，顯示明顯的成功卡片
    html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            .no-scrollbar::-webkit-scrollbar {{ display: none; }}
            .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
            
            /* 玻璃擬態背景 */
            .glass {{
                background: rgba(255, 255, 255, 0.7);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.5);
            }}
            .wheel-gradient {{
                background: linear-gradient(180deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0) 20%, rgba(255,255,255,0) 80%, rgba(255,255,255,1) 100%);
            }}
        </style>
    </head>
    <body class="bg-transparent overflow-hidden">
        <div id="root"></div>

        <script type="text/babel">
            const {{ useState, useEffect, useRef }} = React;
            const DATA = {json_data};
            const ITEM_HEIGHT = 50; // 每個選項的高度

            const WheelColumn = ({{ items, onSelect, label }}) => {{
                const ref = useRef(null);
                
                const handleScroll = () => {{
                    if (!ref.current) return;
                    const index = Math.round(ref.current.scrollTop / ITEM_HEIGHT);
                    if (items[index]) onSelect(items[index].id);
                }};

                return (
                    <div className="flex flex-col items-center">
                        <span className="text-xs font-bold text-gray-400 mb-2 uppercase tracking-widest">{{label}}</span>
                        <div className="relative w-28 h-[150px] bg-white rounded-xl shadow-inner border border-gray-200 overflow-hidden">
                            {/* 中央選取線 */}
                            <div className="absolute top-[50px] left-0 w-full h-[50px] bg-blue-50 border-y border-blue-200 pointer-events-none z-0"></div>
                            
                            {/* 滾動容器 */}
                            <div 
                                ref={{ref}}
                                onScroll={{handleScroll}}
                                className="absolute inset-0 overflow-y-scroll snap-y snap-mandatory no-scrollbar py-[50px] z-10"
                            >
                                {{items.map((item) => (
                                    <div key={{item.id}} className="h-[50px] flex items-center justify-center snap-center">
                                        <span className="text-lg font-bold text-gray-700 font-mono">{{item.label}}</span>
                                    </div>
                                ))}}
                            </div>
                            
                            {/* 上下遮罩 */}
                            <div className="absolute inset-0 wheel-gradient pointer-events-none z-20"></div>
                        </div>
                    </div>
                );
            }};

            const App = () => {{
                // 預設選中第一組
                const [pId, setP] = useState(DATA.prefixes[0]?.id);
                const [rId, setR] = useState(DATA.roots[0]?.id);
                const [match, setMatch] = useState(null);

                useEffect(() => {{
                    const found = DATA.dictionary.find(d => d.combo[0] === pId && d.combo[1] === rId);
                    setMatch(found || null);
                }}, [pId, rId]);

                return (
                    <div className="flex flex-col items-center justify-center p-4">
                        <div className="flex gap-4 mb-6">
                            <WheelColumn items={{DATA.prefixes}} onSelect={{setP}} label="Prefix" />
                            <div className="h-[150px] flex items-center pt-6 text-gray-300">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={{2}} d="M12 4v16m8-8H4" />
                                </svg>
                            </div>
                            <WheelColumn items={{DATA.roots}} onSelect={{setR}} label="Root" />
                        </div>

                        {{match ? (
                            <div className="animate-bounce-in w-full max-w-sm glass rounded-2xl p-4 shadow-lg border-l-4 border-blue-500 flex justify-between items-center transition-all duration-300">
                                <div>
                                    <div className="text-sm text-blue-500 font-bold mb-1">MATCH FOUND!</div>
                                    <h1 className="text-3xl font-black text-gray-800 tracking-tight">{{match.word}}</h1>
                                    <p className="text-gray-500 text-sm mt-1">{{match.meaning}}</p>
                                </div>
                                <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
                                    ✨
                                </div>
                            </div>
                        ) : (
                            <div className="w-full max-w-sm h-[100px] border-2 border-dashed border-gray-300 rounded-2xl flex flex-col items-center justify-center text-gray-400">
                                <span className="text-sm">Spin the wheels to combine...</span>
                            </div>
                        )}}
                    </div>
                );
            }};

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<App />);
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=400)

# ==========================================
# 4. Streamlit 主邏輯 (The Deep Dive)
# ==========================================
def main():
    inject_custom_css()
    df, react_payload = get_data_payload()

    # --- Header ---
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Etymon Decoder")
        st.caption("Visualizing English Etymology through Interactive Wheels")
    
    st.divider()

    # --- Section A: React Wheel ---
    # 這是 Hybrid 的核心：用 Web 技術做互動，但顯示在 Streamlit 裡
    render_react_wheel(react_payload)

    # --- Section B: Python Analysis ---
    st.markdown("<div class='section-label'>🔬 Deep Analysis Lab</div>", unsafe_allow_html=True)
    
    # 用戶操作指引 (因為 React 無法直接寫入 st.session_state，我們需要這個橋樑)
    st.info("👆 在上方找到單字後，請在下方選單選取以查看深度解析：")

    # 搜尋/選擇區
    target_word = st.selectbox(
        "選擇單字：", 
        df['word'].tolist(),
        index=0,
        help="選擇你剛剛在滾輪上組成的單字"
    )

    if target_word:
        # 抓取資料
        row = df[df['word'] == target_word].iloc[0]
        
        # 顯示卡片
        st.markdown("---")
        
        # 佈局：左邊是核心資訊，右邊是語感與發音
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.markdown(f"""
            <div style="background-color:white; padding:30px; border-radius:20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
                <h1 style="margin:0; font-size: 3rem; color: #1565C0;">{row['word']}</h1>
                <div style="color:#78909C; font-size: 1.2rem; font-family: monospace; margin-bottom: 20px;">/{row['phonetic']}/</div>
                
                <div style="display:flex; gap:10px; align-items:center; margin-bottom:15px;">
                    <span style="background:#E3F2FD; color:#1565C0; padding:5px 12px; border-radius:8px; font-weight:bold;">{row['breakdown']}</span>
                    <span style="color:#90A4AE;">➞</span>
                    <span style="font-size:1.2rem; font-weight:bold;">{row['definition']}</span>
                </div>
                
                <div style="background:#FFF3E0; padding:15px; border-radius:10px; border-left: 5px solid #FF9800;">
                    <strong>🗝️ Root Strategy:</strong> <br>
                    root "<b>{row['roots']}</b>" means <em>{row['meaning']}</em>.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown("### 🎧 Native Vibe")
            st.write(row['native_vibe'])
            
            st.markdown("### 🔊 Pronunciation")
            # 嵌入音檔
            st.markdown(text_to_speech_html(row['word']), unsafe_allow_html=True)

if __name__ == "__main__":
    main()