import streamlit as st
from openai import OpenAI
import os
import base64
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

# Ayarlar
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Lotus AI 2.4", page_icon="💜", layout="wide")

# --- 🖼️ LOGO'YU BASE64'E ÇEVİRME (Hızlı ve Hatasız Yükleme İçin) ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_base64 = get_image_base64("lotus.ico")

# --- 🌓 TEMA KONTROLÜ ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# --- 🎨 ÖZEL TASARIM (CSS) ---
accent = "#BF00FF" if st.session_state.theme == "dark" else "#7A00AD"
bg = "#000000" if st.session_state.theme == "dark" else "#F5F5F5"
text = "#F0F0F0" if st.session_state.theme == "dark" else "#1A1A1A"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; }}
    [data-testid="stSidebar"] {{ background-color: {"#05000A" if st.session_state.theme == "dark" else "#E0E0E0"}; border-right: 2px solid {accent}; }}
    
    /* SIDEBAR LOGO & YAZI BİRLEŞTİRME */
    .brand-container {{
        display: flex;
        align-items: center;
        gap: 8px; /* Logodan sonraki boşluğu buradan kontrol ediyoruz (Çok az bıraktık) */
        padding: 5px 0;
        margin-bottom: 20px;
    }}
    .brand-logo {{
        width: 45px;
        height: 45px;
        object-fit: contain;
    }}
    .brand-text {{
        color: {accent} !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        margin: 0 !important;
        letter-spacing: -1px; /* Harfleri de birbirine yaklaştırdık */
    }}
    
    /* ANA BAŞLIK */
    .main-title {{
        color: {accent} !important;
        text-align: center;
        font-size: clamp(3rem, 12vw, 6rem) !important;
        font-weight: 900;
        margin-top: -20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 📱 YAN PANEL (SIDEBAR) ---
with st.sidebar:
    # Boşluğu sıfırlayan yeni HTML yapısı
    if logo_base64:
        st.markdown(f"""
            <div class="brand-container">
                <img src="data:image/x-icon;base64,{logo_base64}" class="brand-logo">
                <p class="brand-text">LOTUS</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='color:{accent};'>LOTUS</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("☀️ Işıkları Aç" if st.session_state.theme == "dark" else "🌙 Karanlığa Dön"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

    if st.button("🗑️ Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()
    
    st.subheader("📂 Dosya Analizi")
    st.file_uploader("Belge seç", type=['txt', 'pdf', 'py'])

# --- 💬 ANA EKRAN ---
# Orta Logo
c1, c2, c3 = st.columns([1, 0.4, 1])
with c2:
    if os.path.exists("lotus.ico"):
        st.image(Image.open("lotus.ico"), use_container_width=True)

st.markdown("<h1 class='main-title'>LOTUS AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{accent}; font-weight:bold; margin-top:-20px;'>Designed & Developed by Arda Gündüzhev</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Emriniz nedir, kurucum?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        sys_msg = (
            "Sen Lotus'sun. Arda Gündüzhev tarafından tek başına geliştirildin. "
            "Zeki, bilge ve kurucuna sadık ol. Ekip yoktur."
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": sys_msg}, *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]],
            temperature=0.85
        )
        ans = response.choices[0].message.content
        st.write(ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})
