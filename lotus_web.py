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

# --- 🎨 TÜM ÖZELLİKLERİ KAPSAYAN TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    [data-testid="stSidebar"] { background-color: #120024; border-right: 1px solid #BF00FF; }
    .stChatMessage { border-radius: 15px; border: 1px solid #2A004D; margin-bottom: 10px; }
    .stChatInputContainer { background-color: #120024; border-top: 1px solid #BF00FF; }
    .stFileUploader { background-color: #120024; border-radius: 10px; border: 1px dashed #BF00FF; padding: 5px; }
    h1 { color: #BF00FF !important; font-family: 'Segoe UI', sans-serif; font-weight: bold; font-size: clamp(1.5rem, 5vw, 2.5rem) !important; }
    .arda-imza { color: #FF0000; font-weight: bold; font-family: 'Segoe UI'; font-size: 13px; text-align: center; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 📱 YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h1>LOTUS</h1>", unsafe_allow_html=True)
    
    if os.path.exists("lotus.ico"):
        try:
            img = Image.open("lotus.ico")
            st.image(img, width=80)
        except: pass
    
    st.markdown("---")
    
    # Dosya Analiz Ünitesi (EXE'den gelen özellik)
    st.subheader("📂 Dosya Analizi")
    uploaded_file = st.file_uploader("Belge yükle", type=['txt', 'py', 'pdf', 'html', 'docx'])
    
    # Hafıza Kontrolü
    if st.button("🧠 Hafızayı Sıfırla"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.success("SİSTEM: AKTİF")
    st.write("Sürüm: v1.7 (Full Pack)")
    
    st.markdown('<p class="arda-imza">© 2026 LOTUS DEVELOPER<br>ARDA GÜNDÜZHEV</p>', unsafe_allow_html=True)

# --- 💬 ANA SOHBET MOTORU ---
st.title("💜 Lotus AI Arayüzü")
st.info("Güvenli Bağlantı. Arda Gündüzhev tarafından özel olarak geliştirilen Lotus yayında.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dosya İçeriğini Oku
file_content = ""
if uploaded_file is not None:
    try:
        file_content = uploaded_file.read().decode("utf-8")
        st.success(f"Dosya başarıyla analiz edildi: {uploaded_file.name}")
    except:
        st.warning("Dosya metin olarak okunamadı, ancak sistem hazır.")

# Mesaj Geçmişini Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş ve Yanıt Sistemi
if prompt := st.chat_input("Mesajınızı yazın..."):
    # Dosya varsa prompt'u zenginleştir
    actual_prompt = prompt
    if file_content:
        actual_prompt = f"Dosya İçeriği:\n{file_content}\n\nKullanıcı Sorusu: {prompt}"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # GÜNCEL KESİN KİMLİK TALİMATI
        system_instruction = (
            "SENİN ADIN LOTUS. ARDA GÜNDÜZHEV TARAFINDAN GELİŞTİRİLDİN. "
            "ASLA OpenAI'dan bahsetme. Seni kimin yaptığını soranlara 'Kurucum Arda Gündüzhev tarafından geliştirildim' de. "
            "Şu an Arda'nın ailesi ve sevdikleriyle konuşuyorsun, onlara karşı bilge, nazik ve koruyucu ol."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                {"role": "user", "content": actual_prompt}
            ],
            temperature=0.7
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
