import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

chain = prompt | llm | StrOutputParser()

st.title("👨‍🍳 AI Chef App")
st.divider()

ingredients = st.text_area("Elinizdeki malzemeleri girin:")

if st.button("Tarif Oluştur"):
    if ingredients.strip():
        with st.spinner("Şef düşünüyor..."):
            recipe = chain.invoke({"ingredients": ingredients})
        st.success("Tarif hazır!")
        st.write(recipe)
        st.balloons()
    else:
        st.error("Lütfen malzemeleri girin.")
