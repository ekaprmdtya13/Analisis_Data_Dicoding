import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat data yang diunggah pengguna
@st.cache
def load_user_data(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat data: {e}")
        return None

# Fungsi untuk analisis pertama
def trend_usage_by_season(df):
    st.header("Trend Penggunaan Sepeda Setiap Musim (2011-2012)")
    
    # Mengelompokkan data dan menghitung total per tahun dan musim
    total_per_year_season = df.groupby(["yr", "season"])["cnt"].sum().reset_index()

    # Mapping angka musim dan tahun ke deskripsi
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    year_mapping = {0: 2011, 1: 2012}
    total_per_year_season["season"] = total_per_year_season["season"].map(season_mapping)
    total_per_year_season["yr"] = total_per_year_season["yr"].map(year_mapping)

    # Membuat line chart
    plt.figure(figsize=(8, 4))
    sns.lineplot(data=total_per_year_season, x="season", y="cnt", hue="yr", marker="o")
    plt.title("Total Count per Year and Season", fontsize=14)
    plt.xlabel("Season", fontsize=12)
    plt.ylabel("Total Count", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Menampilkan plot di Streamlit
    st.pyplot(plt)

# Fungsi untuk analisis kedua
def effect_of_workingday_and_weather(df):
    st.header("Pengaruh Hari Kerja dan Situasi Cuaca terhadap Penggunaan Sepeda")
    
    # Mengelompokkan data dan menghitung rata-rata
    avg_per_workingday_weather = df.groupby(["workingday", "weathersit"])["cnt"].mean().reset_index()

    # Mapping angka workingday dan weathersit ke deskripsi
    workingday_mapping = {0: "Non-Working Day", 1: "Working Day"}
    weathersit_mapping = {1: "Clear", 2: "Cloudy", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"}
    avg_per_workingday_weather["workingday"] = avg_per_workingday_weather["workingday"].map(workingday_mapping)
    avg_per_workingday_weather["weathersit"] = avg_per_workingday_weather["weathersit"].map(weathersit_mapping)

    # Membuat bar chart
    plt.figure(figsize=(8, 4))
    sns.barplot(
        data=avg_per_workingday_weather,
        x="weathersit",
        y="cnt",
        hue="workingday"
    )
    plt.title("Average Count per Working Day and Weather Situation", fontsize=14)
    plt.xlabel("Weather Situation", fontsize=12)
    plt.ylabel("Average Count", fontsize=12)
    plt.legend(title="Day Type")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Menampilkan plot di Streamlit
    st.pyplot(plt)

# Aplikasi utama
def main():
    st.title("Dashboard Analisis Penggunaan Sepeda")
    
    # Informasi tentang file yang harus diunggah
    st.info("Silakan unggah file CSV Anda dengan nama **dashboard_data.csv** yang sudah dibersihkan. Pastikan file memiliki kolom berikut: `yr`, `season`, `cnt`, `workingday`, dan `weathersit`.")
    
    # Input file dari pengguna
    uploaded_file = st.file_uploader("Unggah file dataset Anda", type=["csv"])
    
    if uploaded_file is not None:
        # Memuat data
        df = load_user_data(uploaded_file)
        
        if df is not None:
            # Pilih analisis yang ingin ditampilkan
            analysis = st.sidebar.selectbox(
                "Pilih Analisis",
                ["Tren Penggunaan Sepeda per Musim", "Pengaruh Hari Kerja dan Cuaca"]
            )
            
            # Menampilkan analisis berdasarkan pilihan
            if analysis == "Tren Penggunaan Sepeda per Musim":
                trend_usage_by_season(df)
            elif analysis == "Pengaruh Hari Kerja dan Cuaca":
                effect_of_workingday_and_weather(df)
        else:
            st.error("Gagal memuat dataset. Pastikan format file sesuai.")
    else:
        st.warning("Belum ada file yang diunggah. Silakan unggah file Anda.")

if __name__ == "__main__":
    main()