import streamlit as st
import pandas as pd
import io

# Başlık
st.title("Kahve Satış Verisi Görselleştirme Arayüzü")

# Dosya yükleme (sadece CSV formatında)
uploaded_file = st.file_uploader("Veri dosyanızı yükleyin (yalnızca CSV formatında)", type=["csv"])

if uploaded_file:
    # Dosyayı veri çerçevesine yükle
    data = pd.read_csv(uploaded_file)
    
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

    # Kahve türüne göre para miktarı
    if 'coffee_name' in data.columns and 'money' in data.columns:
        st.subheader("Kahve Türüne Göre Toplam Gelir")
        coffee_sales = data.groupby("coffee_name")["money"].sum()
        st.bar_chart(coffee_sales)

    # Nakit/Kart türüne göre toplam gelir
    if 'cash_type' in data.columns and 'money' in data.columns:
        st.subheader("Ödeme Türüne Göre Toplam Gelir")
        payment_type_sales = data.groupby("cash_type")["money"].sum()
        st.bar_chart(payment_type_sales)

    # Tarihe göre gelir trendi
    if 'date' in data.columns and 'money' in data.columns:
        st.subheader("Tarihe Göre Gelir Trendi")
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        date_sales = data.groupby("date")["money"].sum()
        st.line_chart(date_sales)

else:
    st.info("Lütfen bir CSV veri dosyası yükleyin.")
