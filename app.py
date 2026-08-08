import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="Emir Hoca'nın Özel Asistanı",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. TEMA VE SPORCU KLASÖRÜ SEÇİMİ (SIDEBAR)
st.sidebar.title("🎨 Tema & Ayarlar")
selected_theme = st.sidebar.selectbox(
    "Renk Modu",
    ["Altın & Bordo", "GS Özel", "Gece Mavisi (FB)", "Karanlık Mod"]
)

themes = {
    "Altın & Bordo": {"bg": "#0A192F", "card": "#172A45", "text": "#FFFFFF", "primary": "#FFD700", "btn": "#8B0000"},
    "GS Özel": {"bg": "#121212", "card": "#1E1E1E", "text": "#FFFFFF", "primary": "#FFCC00", "btn": "#D32F2F"},
    "Gece Mavisi (FB)": {"bg": "#001F3F", "card": "#002B5B", "text": "#FFFFFF", "primary": "#FFD700", "btn": "#003366"},
    "Karanlık Mod": {"bg": "#0E1117", "card": "#262730", "text": "#FFFFFF", "primary": "#00FFC6", "btn": "#FF4B4B"}
}

t = themes[selected_theme]

st.sidebar.divider()
st.sidebar.title("🎯 Sporcu Klasörleri")
active_athlete = st.sidebar.selectbox(
    "Aktif Sporcu Seçin:",
    ["Genel / Tüm Okçular", "Emir", "Sporcu 1", "Sporcu 2", "+ Yeni Sporcu Ekle"]
)

if active_athlete == "+ Yeni Sporcu Ekle":
    new_name = st.sidebar.text_input("Yeni Sporcu Adı:")
    if st.sidebar.button("Klasör Oluştur"):
        st.sidebar.success(f"{new_name} klasörü eklendi!")

# 3. CSS TASARIM
st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; color: {t['text']}; }}
    h1, h2, h3 {{ color: {t['primary']} !important; }}
    .stButton > button {{
        background-color: {t['btn']} !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {t['card']};
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. BAŞLIK
st.title("🏹 Emir Hoca'nın Özel Asistanı V1.0")
st.caption(f"📁 **Aktif Klasör:** {active_athlete}")
st.divider()

# 5. İÇERİK MODÜLLERİ
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("📷 Skorkart Yükle / Çek")
        photo_option = st.radio("Fotoğraf Kaynağı:", ["Kamera", "Dosya Yükle"], key="photo_source")
        
        if photo_option == "Kamera":
            img = st.camera_input("Skorkart Görseli Çekin")
        else:
            img = st.file_uploader("Görsel Seçin", type=["jpg", "jpeg", "png"])
            
        st.markdown("---")
        st.subheader("📝 Bu Skorkarta Özel Antrenör Notu")
        card_note = st.text_area(
            "Atış notları (Rüzgar, nişangah, clicker, teknik uyarılar):",
            placeholder="Örn: Rüzgar sağdan esti, nişangah 2 tık sola çekildi...",
            height=100
        )

        if img is not None:
            st.image(img, caption="Yüklenen Skorkart", use_container_width=True)
            if st.button("🧠 Puanları Oku & Analiz Et (Gemini Vision)"):
                with st.spinner("İşleniyor..."):
                    try:
                        api_key = st.secrets.get("GEMINI_API_KEY", "")
                        if not api_key:
                            st.error("Gemini API Key bulunamadı! Secrets alanına ekleyin.")
                        else:
                            genai.configure(api_key=api_key)
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            image_data = Image.open(img)
                            prompt = "Bu okçuluk skorkartındaki puanları oku ve toplam puanı ver."
                            response = model.generate_content([prompt, image_data])
                            st.success("Analiz Tamamlandı!")
                            st.write(response.text)
                    except Exception as e:
                        st.error(f"Hata: {e}")

with col2:
    with st.container(border=True):
        st.subheader("🎙️ Sesli Not & Komut")
        st.info("Atış hakkındaki genel değerlendirmelerinizi ses kaydı olarak ekleyin.")
        if hasattr(st, "audio_input"):
            audio_data = st.audio_input("Mikrofona Dokunun")
            if audio_data:
                st.audio(audio_data)
                st.success("Ses kaydı alındı.")
        else:
            st.warning("Ses kaydı için Streamlit sürümünü güncelleyin.")

    with st.container(border=True):
        st.subheader("📊 Performans Grafiği")
        st.line_chart([52, 54, 53, 57, 56, 58])
