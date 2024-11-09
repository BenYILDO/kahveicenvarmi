import streamlit as st
import pandas as pd
import io

# Başlık
st.title("Veri Yükleme ve Görselleştirme Arayüzü")

# Dosya yükleme
uploaded_file = st.file_uploader("Veri dosyanızı yükleyin (CSV veya XLSX formatında)", type=["csv", "xlsx"])

if uploaded_file:
    # Dosya türüne göre veriyi yükle
    if uploaded_file.name.endswith("csv"):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith("xlsx"):
        data = pd.read_excel(uploaded_file)
    
    # Veri önizlemesi
    st.subheader("Yüklenen Veri:")
    st.write(data.head())
    
    # Veriyi indirilebilir CSV olarak dışa aktarma
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    st.download_button(
        label="Veriyi CSV olarak indir",
        data=csv_data,
        file_name="exported_data.csv",
        mime="text/csv",
    )

    # Temel Görselleştirme Seçenekleri
    st.subheader("Görselleştirme Seçenekleri")

    # Ürün kategorisine göre satış miktarı
    if 'product_category' in data.columns and 'transaction_qty' in data.columns:
        st.subheader("Ürün Kategorisine Göre Toplam Satış Miktarı")
        category_sales = data.groupby("product_category")["transaction_qty"].sum()
        st.bar_chart(category_sales)

    # Mağaza lokasyonlarına göre ortalama birim fiyat
    if 'store_location' in data.columns and 'unit_price' in data.columns:
        st.subheader("Mağaza Lokasyonlarına Göre Ortalama Birim Fiyat")
        location_price = data.groupby("store_location")["unit_price"].mean()
        st.bar_chart(location_price)

    # Tarihe göre satış miktarı trendi
    if 'transaction_date' in data.columns and 'transaction_qty' in data.columns:
        st.subheader("Tarihe Göre Satış Miktarı Trendi")
        data['transaction_date'] = pd.to_datetime(data['transaction_date'], errors='coerce')
        date_sales = data.groupby("transaction_date")["transaction_qty"].sum()
        st.line_chart(date_sales)

else:
    st.info("Lütfen bir veri dosyası yükleyin.")
