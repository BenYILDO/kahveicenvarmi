import streamlit as st
import pandas as pd

# Veri setini yükle
df = pd.read_csv("coffee-quality-data-cqi.csv")  # CSV dosyasının yolu

# Uygulama başlığı
st.title("Kahve Kalitesi Analizi - CQI")

# Veri seti hakkında genel bilgi
st.subheader("Veri Seti Genel Bilgileri")
st.write(df.describe())

# Kahve türü seçme aracı
coffee_types = df['Species'].unique()  # Kahve türleri (örneğin Arabica, Robusta vb.)
selected_type = st.selectbox("Kahve Türünü Seç:", coffee_types)

# Seçilen kahve türüne göre
