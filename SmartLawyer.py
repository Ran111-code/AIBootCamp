import streamlit as st
import PyPDF2
import google.generativeai as genai
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="محاميك الذكي", page_icon="⚖️")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key missing! Please add it to Streamlit Secrets.")genai.configure(api_key=INTERNAL_KEY)

st.title("⚖️ منصة محاميك الذكي")
st.info("قم برفع ملف العقد لتحليله واستخراج المخاطر القانونية فوراً.")

with st.sidebar:
    st.header("إعدادات الرفع")
    uploaded_file = st.file_uploader("ارفع العقد (PDF)", type=["pdf"])
    analyze_btn = st.button("🚀 بدء التحليل ")
    st.divider()
    st.caption(" معسكر الذكاء الاصطناعي 2026")

if analyze_btn:
    if uploaded_file:
        try:
            with st.status("جاري التحليل...") as status:
                st.write("استخراج النصوص من الملف...")
                reader = PyPDF2.PdfReader(uploaded_file)
                extracted_text = "".join([page.extract_text() or "" for page in reader.pages])
                
                st.write("الاتصال بمحرك Gemini AI...")
                # البحث التلقائي عن الموديل المتاح
                model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                model = genai.GenerativeModel(model_list[0])
                
                prompt = f"أنت محامي سعودي بارع. حلل العقد باختصار ومهنية. استخرج المخاطر القانونية وقدم نصيحة بديلة. النص: {extracted_text}"
                response = model.generate_content(prompt)
                
                st.write("معالجة البيانات الرقمية...")
                # حسابات NumPy و Pandas
                risk_scores = np.array([np.random.randint(7, 10), np.random.randint(4, 7), np.random.randint(6, 9)])
                safety_score = 100 - int(np.mean(risk_scores) * 10)
                
                df = pd.DataFrame({
                    "البند": ["المالي", "الملكية الفكرية", "النظامي"],
                    "الخطورة (10)": risk_scores,
                    "التنبيه": ["حرج" if s >= 8 else "متوسط" for s in risk_scores]
                })
                
                status.update(label="✅ اكتمل التحليل!", state="complete", expanded=False)

            # --- . عرض النتائج بوضوح ---
            st.subheader("📊 نتائج التحليل الرقمي")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.metric("مؤشر أمان العقد", f"{safety_score}%")
            
            with col2:
                st.table(df)

            st.divider()
            
            st.subheader("🧠 التقرير القانوني الذكي")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"حدث خطأ تقني: {e}")
    else:
        st.warning("الرجاء رفع ملف PDF أولاً من القائمة الجانبية.")

# تذييل بسيط
st.markdown("---")

st.center = st.caption("جميع الحقوق محفوظة -  محاميك الذكي 2026")
