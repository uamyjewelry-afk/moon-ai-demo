import streamlit as st
import google.generativeai as genai
import json

# -----------------------------------------------------------------------------
# 1. 디자인 및 설정
# -----------------------------------------------------------------------------
st.set_page_config(layout="wide", page_title="Teacher Moon AI Studio", page_icon="🎬")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e5e7eb; }
    .stSidebar { background-color: #0d0d0d; border-right: 1px solid #1e1e1e; }
    .stButton>button { 
        background-color: #fbbf24; color: black; font-weight: 900; 
        border-radius: 12px; text-transform: uppercase; letter-spacing: 1px;
    }
    .stButton>button:hover { background-color: #f59e0b; color: black; }
    h1, h2, h3 { color: white !important; font-family: sans-serif; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 사이드바
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🚪 Teacher Moon")
    st.caption("All-In-One AI Production Studio")
    
    # API Key 처리 (비밀번호 설정되어 있으면 자동 입력, 아니면 입력창 뜸)
    if 'GOOGLE_API_KEY' in st.secrets:
        api_key = st.secrets['GOOGLE_API_KEY']
        st.success("✅ API Key Connected")
    else:
        api_key = st.text_input("Google API Key", type="password")
    
    st.divider()
    topic = st.text_area("주제 입력", height=100, placeholder="Example: A futuristic city in 2050...")
    st.markdown("#### Settings")
    num_cuts = st.slider("Scenes", 1, 10, 5)
    ratio = st.selectbox("Ratio", ["16:9", "1:1", "9:16"])
    generate_btn = st.button("🚀 LAUNCH PRODUCTION")

# -----------------------------------------------------------------------------
# 3. 로직
# -----------------------------------------------------------------------------
def generate_story(key, topic, cuts):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Create a {cuts}-scene storyboard for: "{topic}".
    Return ONLY a JSON array: [{{"id":1, "story":"...", "prompt":"..."}}, ...]
    """
    try:
        res = model.generate_content(prompt)
        return json.loads(res.text.replace("```json","").replace("```",""))
    except:
        return []

# -----------------------------------------------------------------------------
# 4. 결과 화면
# -----------------------------------------------------------------------------
if generate_btn:
    if not api_key:
        st.error("API Key가 없습니다.")
    elif not topic:
        st.warning("주제를 입력하세요.")
    else:
        with st.status("Running AI...", expanded=True):
            scenes = generate_story(api_key, topic, num_cuts)
            st.session_state['scenes'] = scenes

if 'scenes' in st.session_state:
    st.markdown("## Storyboard Gallery")
    for s in st.session_state['scenes']:
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"<div style='background:#222;height:150px;display:flex;align-items:center;justify-content:center;border-radius:10px;'>Cut {s['id']} Image</div>", unsafe_allow_html=True)
            with col2:
                st.info(s['story'])
                st.code(s.get('prompt', 'Prompt generation failed'), language='text')