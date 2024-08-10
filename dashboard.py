import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#1 Gathering Data
day_df=pd.read_csv("day_df_final.csv", delimiter=",")
hour_df=pd.read_csv("hour_df_final.csv", delimiter=",")

#2 Cleaning Data
day_df['dteday']=pd.to_datetime(day_df['dteday'])
str_columns = ["season", "yr", "mnth","holiday","weekday","workingday","weathersit"]
for column in str_columns:
  day_df[column] = day_df[column].astype('category')
hour_df['dteday']=pd.to_datetime(hour_df['dteday'])
str_columns_hour = ["season", "yr", "mnth","hr","holiday","weekday","workingday","weathersit"]
for column in str_columns_hour:
  hour_df[column] = hour_df[column].astype('category')

#3 Making Helper Function 1
def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    return daily_rent_df

#4 Making Helper Function 2
def create_seasonal_rent_df(df):
    seasonal_rent_df = df.groupby(by='season').agg({
    "casual": "sum",
    "registered": "sum",
    "cnt":"sum"})
    seasonal_rent_df = seasonal_rent_df.reset_index()
    return seasonal_rent_df

#4 Making Helper Function 3
def create_weathersit_rent_df(df):
   weathersit_rent_df=df.groupby(by='weathersit').agg({
      "casual":"sum",
      "registered":"sum",
      "cnt":"sum",
      "temp":"mean",
      "atemp":"mean",
      "hum":"mean",
      "windspeed":"mean"
      })
   weathersit_rent_df = weathersit_rent_df.reset_index()
   return weathersit_rent_df

#5 Making Helper Function 4
def create_weekday_rent_df(df):
   weekday_rent_df=df.groupby(by='weekday').agg({
    "casual":"sum",
    "registered":"sum",
    "cnt":"sum"
    })
   weekday_rent_df = weekday_rent_df.reset_index()
   return weekday_rent_df

#5 Making Helper Function 5
def create_hourly_rent_df(df):
   hourly_rent_df=df.groupby(by='hr').agg({
    "casual": "sum",
    "registered": "sum",
    "cnt":"sum",
    "temp":"mean",
    "atemp":"mean",
    "hum":"mean",
    "windspeed":"mean"
    })
   hourly_rent_df = hourly_rent_df.reset_index()
   return hourly_rent_df

#5 Making Helper Function 6
def create_dailyhour_rent_df(df):
   daily_hourly_rent_df=df.groupby(by=['weekday','hr']).agg({
    "casual": "sum",
    "registered": "sum",
    "cnt":"sum",
    "temp":"mean",
    "atemp":"mean",
    "hum":"mean",
    "windspeed":"mean"
    })
   daily_hourly_rent_df = daily_hourly_rent_df.reset_index()
   return daily_hourly_rent_df

#Making Filtered Data
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]
hourly_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]


st.title('Hasil Analisis Bike Sharing Dataset')
tab1, tab2, tab3 , tab4, tab5, tab6 = st.tabs(["Conclusion 1", "Conclusion 2", "Conclusion 3","Conclusion 4", "Conclusion 5", "Conclusion 6"])

with tab1:
   st.subheader('Pertanyaan 1: Bagaimana Trend Rental Sepeda Sepanjang Tahun?')
   daily_rented_df = create_daily_rent_df(main_df)
   col1, col2, col3 = st.columns(3)
   with col1:
    total_rented_cas = round(daily_rented_df.casual.mean(),2)
    st.metric("Average Casual User rented per day", value=total_rented_cas)
   with col2:
    total_rented_reg = round(daily_rented_df.registered.mean(),2)
    st.metric("Average Registered User rented per day", value=total_rented_reg)
   with col3:
    total_rented_cnt = round(daily_rented_df.cnt.mean(),2)
    st.metric("Average User rented per day", value=total_rented_cnt)
    
   fig = px.line(daily_rented_df, x="dteday", y=["casual","registered","cnt"])
   st.plotly_chart(fig, use_container_width=True)
   st.write("""Secara umum tren rental sepeda mengalami peningkatan pada periode 20211-2012.Jika kita lihat lebih lanjut, ada pola kenaikan dan penurunan pada periode bulan-bulan tertentu. Jumlah sepeda yang dirental mengalami kenaikan pada periode Semester 1. Namun memasuki bulan september terjadi penurunan drastis hingga akhir tahun. Trend peningkatan jumlah sepeda yang dirental ini lebih dapat ditujunkkan oleh Pengguna yang telah terdaftar (Registered). Pola yang cukup mendatar ditunjukkan oleh pengguna Casual pada periode 2011-2012.""")


with tab2:
   st.subheader('Pertanyaan 2: Bagaimana Trend Rental Sepeda Menurut Musim?')
   season_rented_df=create_seasonal_rent_df(main_df)
   fig = px.bar(season_rented_df, x="season", y=["casual","registered"], barmode='group')
   st.plotly_chart(fig, use_container_width=True)
   st.write("""Pola rental sepeda mengalami kenaikan setiap musimnya hingga puncaknya pada musim gugur. Pada musim dingin, terjadi sedikit penurunan dibanding musim gugur dalam penggunaan sepeda rental""")

with tab3:
   st.subheader('Pertanyaan 3: Bagaimana Trend Rental Sepeda Menurut Kondisi Cuaca?')
   weathersit_rented_df=create_weathersit_rent_df(main_df)
   fig = px.bar(weathersit_rented_df, x="weathersit", y=["casual","registered"], barmode='group')
   st.plotly_chart(fig, use_container_width=True)
   st.write("""Rental sepeda paling banyak dilakukan saat kondisi cuaca yang cerah/sedikit berawan. Pada saat cuaca hujan deras/bersalju tidak ada penggunaan rental sepeda""")

with tab4:
   st.subheader('Pertanyaan 4: Bagaimana Trend Rental Sepeda Menurut hari dalam seminggu?')
   weekday_rented_df=create_weekday_rent_df(main_df)
   fig = px.bar(weekday_rented_df, x="weekday", y=["casual","registered"], barmode='group')
   st.plotly_chart(fig, use_container_width=True)
   st.write("""Rata-rata penggunaan sepeda rental menurut hari ditemukan berbeda untuk Registered user dan Casual User. Rata-rata sepeda yang dipinjam oleh Registered user ditemukan lebih rendah pada hari minggu dan sabtu. Sedangkan pada weekday, penggunaan sepeda rental oleh Registered user cenderung lebih tinggi dan mempunyai pola yang relatif sama. Sedangkan casual user lebih banyak meminjam sepeda pada hari minggu dan sabtu dibandingkan dengan weekday""")

with tab5:
   st.subheader('Pertanyaan 5: Bagaimana Trend Rental Sepeda Menurut Jam dalam 1 hari?')
   hourly_rented_df=create_hourly_rent_df(hourly_df)
   fig = px.line(hourly_rented_df, x="hr", y=["casual","registered","cnt"])
   st.plotly_chart(fig, use_container_width=True)
   st.write("""Rata-rata penggunaan sepeda rental menurut jam ditemukan berbeda untuk Registered user dan Casual User. Peminjaman sepeda oleh registered user mempunyai 2 waktu puncak yakni jam 8 dan jam 17. Sedangkan Rata-rata Casual user menggunakan sepeda mulai dari pukul 8 hingga 17 dan relatif sama pada periode waktu tersebut""")

with tab6:
   st.subheader('Pertanyaan 6: Bagaimana Trend Rental Sepeda Menurut Jam dan hari dalam seminggu?')
   dailyhourly_rented_df=create_dailyhour_rent_df(hourly_df)
   fig=px.line(dailyhourly_rented_df, x="hr", y=["casual","registered"],
              facet_col="weekday",facet_col_wrap=2)
   st.plotly_chart(fig, use_container_width=True)
   st.write("""Rata-rata penggunaan sepeda rental menurut jam dan hari ditemukan berbeda untuk Registered user dan Casual User pada weekdays namun pola yang relatif sama terjadi pada weekend. Pada weekday registered user mempunyai puncak peminjaman sepede pada pukul 08.00 dan 17.00. Namun pada weekend, registered user tidak ditemukan 2 puncak seperti yang terjadi pada weekday. Registered user mulai meminjam sepeda sekitar pukul 08.00 dan secara perlahan meningkat hingga mulai mengalami penurunan pada pukul 15.00 atau 16.00""")
