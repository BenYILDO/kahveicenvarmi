import streamlit as st
import pandas as pd
import io

# Başlık
st.title("Dinamik Veri Görselleştirme Arayüzü")

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

    # Dinamik Görselleştirme Seçenekleri
    st.subheader("Görselleştirme Seçenekleri")

    # Sütunları inceleyip görselleştirme yapalım
    numeric_columns = data.select_dtypes(include='number').columns.tolist()
    date_columns = data.select_dtypes(include='datetime').columns.tolist()
    categorical_columns = data.select_dtypes(include='object').columns.tolist()

    # Sayısal bir sütunu kategorik bir sütuna göre gruplandırarak toplam almak
    if len(numeric_columns) > 0 and len(categorical_columns) > 0:
        st.subheader("Kategorik ve Sayısal Sütunlara Göre Toplam Görselleştirme")
        
        selected_category = st.selectbox("Kategorik sütun seçin", categorical_columns)
        selected_numeric = st.selectbox("Sayısal sütun seçin", numeric_columns)
        
        category_sales = data.groupby(selected_category)[selected_numeric].sum()
        st.bar_chart(category_sales)
    
    # Tarihsel bir trende göre çizgi grafiği (eğer tarih verisi varsa)
    if len(date_columns) > 0 and len(numeric_columns) > 0:
        st.subheader("Tarihsel Trende Göre Sayısal Verilerin Görselleştirilmesi")
        
        selected_date = st.selectbox("Tarih sütununu seçin", date_columns)
        selected_numeric_for_trend = st.selectbox("Sayısal sütun seçin", numeric_columns, key="trend")
        
        # Tarih sütununu datetime formatına çevirme
        data[selected_date] = pd.to_datetime(data[selected_date], errors='coerce')
        date_sales = data.groupby(selected_date)[selected_numeric_for_trend].sum()
        st.line_chart(date_sales)

else:
    st.info("Lütfen bir CSV veri dosyası yükleyin.")
