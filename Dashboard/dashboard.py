import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Memuat dataset default
@st.cache
def load_data():
    try:
        return pd.read_csv("dashboard_data.csv")
    except FileNotFoundError:
        st.error("File 'dashboard_data.csv' tidak ditemukan. Pastikan file tersedia di direktori yang sama dengan aplikasi ini.")
        return None

# Fungsi untuk analisis pertama
def trend_usage_by_season(df, selected_years, selected_seasons, selected_working_days, selected_weather_situations):
    st.subheader("Trend Penggunaan Sepeda Berdasarkan Musim (2011-2012)")

    # Filter berdasarkan tahun
    if selected_years:
        df = df[df["yr"].isin(selected_years)]

    # Filter berdasarkan musim
    if selected_seasons:
        df = df[df["season"].isin(selected_seasons)]

    # Filter berdasarkan working day
    if selected_working_days:
        df = df[df["workingday"].isin(selected_working_days)]

    # Filter berdasarkan weather situation
    if selected_weather_situations:
        df = df[df["weathersit"].isin(selected_weather_situations)]

    # Mengelompokkan data dan menghitung total per tahun dan musim
    total_per_year_season = df.groupby(["yr", "season"])["cnt"].sum().reset_index()

    # Mapping angka musim dan tahun ke deskripsi
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    year_mapping = {0: 2011, 1: 2012}
    total_per_year_season["season"] = total_per_year_season["season"].map(season_mapping)
    total_per_year_season["yr"] = total_per_year_season["yr"].map(year_mapping)

    if total_per_year_season.empty:
        st.warning("Tidak ada data yang cocok dengan filter yang dipilih.")
        return

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
def effect_of_workingday_and_weather(df, selected_years, selected_working_days, selected_weather_situations):
    st.subheader("Pengaruh Hari Kerja dan Situasi Cuaca terhadap Penggunaan Sepeda")

    # Filter berdasarkan tahun
    if selected_years:
        df = df[df["yr"].isin(selected_years)]

    # Filter berdasarkan working day
    if selected_working_days:
        df = df[df["workingday"].isin(selected_working_days)]

    # Filter berdasarkan weather situation
    if selected_weather_situations:
        df = df[df["weathersit"].isin(selected_weather_situations)]

    # Mengelompokkan data dan menghitung rata-rata
    avg_per_workingday_weather = df.groupby(["workingday", "weathersit"])["cnt"].mean().reset_index()

    # Mapping angka workingday dan weathersit ke deskripsi
    workingday_mapping = {0: "Non-Working Day", 1: "Working Day"}
    weathersit_mapping = {1: "Clear", 2: "Cloudy", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"}
    avg_per_workingday_weather["workingday"] = avg_per_workingday_weather["workingday"].map(workingday_mapping)
    avg_per_workingday_weather["weathersit"] = avg_per_workingday_weather["weathersit"].map(weathersit_mapping)

    if avg_per_workingday_weather.empty:
        st.warning("Tidak ada data yang cocok dengan filter yang dipilih.")
        return

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

    # Load dataset
    df = load_data()

    if df is not None:
        # Sidebar - Filter
        st.sidebar.subheader("Filter Data")

        # Filter tahun
        st.sidebar.markdown("**Pilih Tahun**")
        year_mapping = {0: 2011, 1: 2012}
        year_options = {v: k for k, v in year_mapping.items()}
        selected_years_labels = st.sidebar.multiselect(
            "Tahun", list(year_options.keys()), default=list(year_options.keys())
        )
        selected_years = [year_options[label] for label in selected_years_labels]

        # Filter musim (multiple choice)
        st.sidebar.markdown("**Pilih Musim (Season)**")
        season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
        season_options = {v: k for k, v in season_mapping.items()}
        selected_seasons_labels = st.sidebar.multiselect(
            "Musim", list(season_options.keys()), default=list(season_options.keys())
        )
        selected_seasons = [season_options[label] for label in selected_seasons_labels]

        # Filter working day (multiple choice)
        st.sidebar.markdown("**Pilih Hari Kerja (Working Day)**")
        workingday_mapping = {0: "Non-Working Day", 1: "Working Day"}
        workingday_options = {v: k for k, v in workingday_mapping.items()}
        selected_working_days_labels = st.sidebar.multiselect(
            "Hari Kerja", list(workingday_options.keys()), default=list(workingday_options.keys())
        )
        selected_working_days = [workingday_options[label] for label in selected_working_days_labels]

        # Filter weather situation (multiple choice)
        st.sidebar.markdown("**Pilih Situasi Cuaca (Weather Situation)**")
        weathersit_mapping = {1: "Clear", 2: "Cloudy", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"}
        weathersit_options = {v: k for k, v in weathersit_mapping.items()}
        selected_weather_situations_labels = st.sidebar.multiselect(
            "Situasi Cuaca", list(weathersit_options.keys()), default=list(weathersit_options.keys())
        )
        selected_weather_situations = [weathersit_options[label] for label in selected_weather_situations_labels]

        # Analisis pertama
        trend_usage_by_season(df, selected_years, selected_seasons, selected_working_days, selected_weather_situations)

        # Analisis kedua
        effect_of_workingday_and_weather(df, selected_years, selected_working_days, selected_weather_situations)

if __name__ == "__main__":
    main()
