import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image

# Ayarlar ve API
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Sayfa Yapılandırması
st.set_page_config(page_title="Lotus AI 2026", page_icon="💜", layout="wide")

# --- 📱 GELİŞMİŞ MOBİL & OKUNABİLİRLİK TASARIMI (CSS) ---
st.markdown("""
    <style>
    /* Ana Arka Plan ve Yazı Rengi */
    .stApp { 
        background-color: #000000; 
        color: #E0E0E0; 
    }
    
    /* Başlık Fontu - Mobilde Dinamik Boyut */
    h1 { 
        color: #BF00FF !important; 
        font-family: 'Segoe UI', sans-serif; 
        font-weight: 800;
        font-size: clamp(1.2rem, 6vw, 2.5rem) !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Mesaj Balonları ve Okunabilirlik */
    .stChatMessage { 
        border-radius: 15px; 
        border: 1px solid #3D007A; 
        background-color: #0A001A;
        margin-bottom: 8px;
        padding: 10px;
        font-size: 15px !important;
        line-height: 1.4;
    }

    /* Yan Panel Mobilde Daha Temiz */
    [data-testid="stSidebar"] { 
        background-color: #05000A; 
        border-right: 2px solid #BF00FF;
    }

    /* Giriş Kutusu - Mobilde Sabit ve Belirgin */
    .stChatInputContainer { 
        background-color: #000000; 
        border-top: 1px solid #BF00FF;
        padding-bottom: 20px;
    }

    /* Bilgi Kutusu (Info) */
    .stAlert {
        background-color: #120024;
        color: #BF00FF;
        border: 1px solid #BF00FF;
        font-size: 13px;
    }

    /* Görünmeyen Yazılar İçin Fix */
    p, span, label {
        color: #F0F0F0 !important;
    }
    
    .arda-imza { 
        color: #FF3131; 
        font-weight: bold; 
        font-size: 11px; 
        text-align: center;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 📱 YAN PANEL ---
with st.sidebar:
    st.markdown("<h1>LOTUS</h1>", unsafe_allow_html=True)
    if os.path.exists("lotus.ico"):
        try:
            st.image(Image.open("lotus.ico"), width=70)
        except: pass
    
    st.markdown("---")
    st.subheader("⚙️ Araçlar")
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

    uploaded_file = st.file_uploader("Dosya Analizi", type=['txt', 'pdf', 'py'])
    
    st.markdown("---")
    st.markdown('<p class="arda-imza">© 2026 LOTUS DEVELOPER<br>ARDA GÜNDÜZHEV</p>', unsafe_allow_html=True)

# --- 💬 SOHBET ALANI ---
st.title("💜 Lotus AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dosya İşleme
file_text = ""
if uploaded_file:
    try:
        file_text = uploaded_file.read().decode("utf-8")
        st.info("📂 Dosya içeriği sisteme yüklendi.")
    except:
        st.error("Dosya okunurken hata oluştu.")

# Sohbeti Yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Giriş
if prompt := st.chat_input("Lotus'a yazın..."):
    final_prompt = prompt
    if file_text:
        final_prompt = f"Dosya verisi: {file_text}\n\nSoru: {prompt}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        sys_msg = "Adın Lotus. Arda Gündüzhev tarafından yapıldın. Çok kibar ve bilge bir asistansın. OpenAI'dan asla bahsetme."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": sys_msg},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                {"role": "user", "content": final_prompt}
            ]
        )
        ans = response.choices[0].message.content
        st.write(ans)
    st.session_state.messages.append({"role": "assistant", "content": ans})
