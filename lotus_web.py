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

# --- 🎨 PREMİUM MOR & SİYAH TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #000000; color: white; }
    
    /* Yan Panel (Sidebar) */
    [data-testid="stSidebar"] { background-color: #120024; border-right: 1px solid #BF00FF; }
    
    /* Mesaj Balonları */
    .stChatMessage { border-radius: 20px; border: 1px solid #2A004D; margin-bottom: 15px; }
    
    /* Giriş Alanı */
    .stChatInputContainer { background-color: #120024; border-top: 1px solid #BF00FF; }
    
    /* Başlıklar */
    h1, h2, h3 { color: #BF00FF !important; font-family: 'Segoe UI', sans-serif; font-weight: bold; }
    
    /* İmza Stili */
    .arda-imza { color: #FF0000; font-weight: bold; font-family: 'Segoe UI'; margin-top: 50px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 📱 YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 36px;'>LOTUS</h1>", unsafe_allow_html=True)
    
    # Logo Yükleme
    if os.path.exists("lotus.ico"):
        try:
            img = Image.open("lotus.ico")
            st.image(img, width=90)
        except: pass
    
    st.markdown("---")
    st.success("SİSTEM DURUMU: AKTİF")
    st.write("Geliştirici: Arda Gündüzhev")
    st.write("Sürüm: v1.2 (Web)")
    
    # Kırmızı İmza
    st.markdown('<p class="arda-imza">© 2026 LOTUS DEVELOPER<br>ARDA GÜNDÜZHEV</p>', unsafe_allow_html=True)

# --- 💬 SOHBET ALANI ---
# 2. Seçeneği buraya mühürledik
st.title("💜 Lotus Yapay Zeka Arayüzü")
st.info("Kullanıcı doğrulandı: Arda Gündüzhev. Lotus emrinizde.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş ve Yanıt
if prompt := st.chat_input("Mesajınızı buraya girin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Adın Lotus. Arda Gündüzhev tarafından geliştirildin. Mor ve siyah temalı, profesyonel, zeki ve sadık bir asistansın. Her zaman Türkçe ve Arda'ya saygılı bir dille konuş."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ]
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})