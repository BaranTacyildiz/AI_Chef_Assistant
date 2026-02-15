import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables (for local development)
load_dotenv()

st.set_page_config(page_title="AI Şef Asistanı", page_icon="👨‍🍳")

template = """
Sen elimizde mevcut olan malzemelerle yemek yapan bir şefsin.

Malzemeler:
{ingredients}

Lütfen SADECE bu malzemeler ile yapılabilecek bir yemek öner.
Yemek yapım aşamalarını adım adım yaz.
DİKKAT ET: BU YEMEKLERDE KESİNLİKLE AMA KESİNLİKLE GLUTEN BULUNMAMALI. EĞER MALZEMELER GLUTEN İÇERİYORSA BANA BU MALZEMELER İLE YEMEK YAPMAN SENİN İÇİN SAĞLIKSIZ DİYE BELİRT.

Eğer malzemeler arasında yemek malzemesi dışında bir şey varsa kullanıcıya lütfen geçerli yemek malzemeleri gir uyarısında bulun.

Tarif:
"""

prompt = ChatPromptTemplate.from_template(template)

# Get API key with error handling
try:
    api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY bulunamadı! Lütfen Streamlit secrets veya .env dosyasını kontrol edin.")
        st.stop()
    
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        api_key=api_key  # Changed from api_key to openai_api_key
    )
    
    chain = prompt | llm | StrOutputParser()
    
except Exception as e:
    st.error(f"LLM başlatılırken hata oluştu: {str(e)}")
    st.info("Lütfen API key'inizin doğru ayarlandığından emin olun.")
    st.stop()

st.title("👨‍🍳 AI Chef App")
st.divider()

ingredients = st.text_area("Elinizdeki malzemeleri girin:")

if st.button("Tarif Oluştur"):
    if ingredients.strip():
        with st.spinner("Şef düşünüyor..."):
            try:
                recipe = chain.invoke({"ingredients": ingredients})
                st.success("Tarif hazır!")
                st.write(recipe)
                st.balloons()
            except Exception as e:
                st.error(f"Tarif oluşturulurken hata oluştu: {str(e)}")
    else:
        st.error("Lütfen malzemeleri girin.")