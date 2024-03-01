import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

df_time = pd.read_csv("https://raw.githubusercontent.com/Rakishu02/Bike-Sharing/6dcb5ee8483570e6abdf57f0c88320b24d840770/main_data.csv")
df_time['dteday'] = pd.to_datetime(df_time['dteday'])


###
st.header('🚲Bike Sharing Analysis Dashboard🚲')

# Sidebar untuk rentang tanggal
min_date = df_time["dteday"].min()
max_date = df_time["dteday"].max()
 
with st.sidebar:
    st.title("Sidebar")
    st.image("https://github.com/Rakishu02/Bike-Sharing/blob/631d26a35d1223554e9dcee53e3ed1d51814bbfd/logo%20bangkit.jpg?raw=true")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Konversi start_date dan end_date menjadi np.datetime64
start_date = np.datetime64(start_date)
end_date = np.datetime64(end_date)

# Filter dataframe berdasarkan rentang tanggal yang dipilih
df_selected = df_time[(df_time['dteday'] >= start_date) & (df_time['dteday'] <= end_date)]

# Mengambil nilai casual, registered, dan cnt
casual_values = df_selected['casual'].sum()
registered_values = df_selected['registered'].sum()
total_values = df_selected['cnt'].sum()

# Menampilkan nilai di dashboard dalam format st.metric
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Casual", value=casual_values)

with col2:
    st.metric("Total Registered", value=registered_values)

with col3:
    st.metric("Total Peminjaman", value=total_values)


###
st.subheader("Grafik Perkembangan Jumlah Peminjaman Sepeda 2011 - 2012")

df = df_time.copy()

# Membuat rata-rata untuk setiap minggu dari jumlah peminjaman sepeda tiap harinya
df_weekly = df.resample('W', on='dteday').mean()
df_weekly['moving_avg'] = df_weekly['cnt'].rolling(window=4).mean()
x = np.arange(len(df_weekly)).reshape(-1, 1)
y = df_weekly['cnt'].values.reshape(-1, 1)
slope, intercept = np.polyfit(x.flatten(), y.flatten(), 1)
df_weekly['trend'] = intercept + slope * x

# Pengaturan tema dan palet warna
sns.set_theme(style="whitegrid")  # Ganti tema
custom_palette = sns.color_palette(['salmon', 'skyblue', 'teal'])  # Atur palet warna

# Membuat plot menggunakan Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=df_weekly.index, y='cnt', data=df_weekly, label='Rata-Rata per Minggu', color=custom_palette[0], ax=ax)
sns.lineplot(x=df_weekly.index, y='moving_avg', data=df_weekly, label='Moving Average (4 Minggu)', linestyle='--', color=custom_palette[1], ax=ax)
sns.lineplot(x=df_weekly.index, y='trend', data=df_weekly, label='Tren', linestyle=':', color=custom_palette[2], ax=ax)

plt.xlabel('')
plt.ylabel('Jumlah Peminjaman')
plt.title('')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
st.pyplot(fig)

st.text(" ")
st.text(" ")
st.text(" ")


###
st.subheader("Perbandingan Peminjaman Sepeda Berdasarkan Musim dan Tahun")

df = df_time.copy()

# Mapping untuk variabel kategorik
df['season'] = df['season'].map({1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'})
df['yr'] = df['yr'].map({0: '2011', 1: '2012'})

# Menghitung jumlah total peminjaman (cnt) untuk setiap kombinasi musim dan tahun
pivot_season_year = df.groupby(['season', 'yr'])['cnt'].sum().reset_index()
x = pivot_season_year['season'].unique()
y1 = pivot_season_year[pivot_season_year['yr'] == '2011']['cnt']
y2 = pivot_season_year[pivot_season_year['yr'] == '2012']['cnt']

# Membuat plot stacked barchart
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x, y1, color='skyblue', label='2011', width=0.4, alpha=0.8)
ax.bar(x, y2, bottom=y1, color='salmon', label='2012', width=0.4, alpha=0.8)

ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Peminjaman (Juta)')
ax.legend(title='Tahun')
st.pyplot(fig)

st.text(" ")
st.text(" ")
st.text(" ")


###
st.subheader("Perbandingan Peminjam Kasual dan Terdaftar")

df = df_time.copy()

# Mapping untuk variabel kategorik
df['yr'] = df['yr'].map({0: '2011', 1: '2012'})

# Menghitung rata-rata casual dan registered untuk setiap tahun
avg_data = df.groupby('yr').mean().reset_index()

# Menampilkan pie charts
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

labels_2011 = ['Casual', 'Registered']
sizes_2011 = avg_data.loc[avg_data['yr'] == '2011', ['casual', 'registered']].values.flatten()
axes[0].pie(sizes_2011, labels=labels_2011, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'salmon'],
           wedgeprops={'linewidth': 6, 'edgecolor': 'white'}, textprops={'fontsize': 16})
axes[0].set_title('2011', fontdict={'fontsize': 18, 'fontweight': 'bold'})

labels_2012 = ['Casual', 'Registered']
sizes_2012 = avg_data.loc[avg_data['yr'] == '2012', ['casual', 'registered']].values.flatten()
axes[1].pie(sizes_2012, labels=labels_2012, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'salmon'],
           wedgeprops={'linewidth': 6, 'edgecolor': 'white'}, textprops={'fontsize': 16})
axes[1].set_title('2012', fontdict={'fontsize': 18, 'fontweight': 'bold'})

st.pyplot(fig)

st.text(" ")
st.text(" ")
st.text(" ")


###
st.subheader("Pengelompokan Berdasarkan Jumlah Peminjaman Sepeda per Bulan")

df = df_time.copy()

# Mapping untuk variabel kategorik
month_map = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 6: 'Juni', 
             7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'}
df['mnth'] = pd.Categorical(df['mnth'].map(month_map), categories=month_map.values(), ordered=True)

# Mendapatkan nilai minimum dan maksimum dan membagi data menjadi 3 bagian
min_total = df['cnt'].min()
max_total = df['cnt'].max()
bins = [min_total, min_total + (max_total - min_total) / 3, min_total + 2 * (max_total - min_total) / 3, max_total]

labels = ['Sedikit', 'Sedang', 'Banyak']
df['cluster'] = pd.cut(df['cnt'], bins=bins, labels=labels)

# Menghitung frekuensi masing-masing kombinasi mnth (bulan) dan cluster
result = df.groupby(['mnth', 'cluster']).size().unstack(fill_value=0)

# Data untuk plotting
months = result.index
sedikit = result['Sedikit']
sedang = result['Sedang']
banyak = result['Banyak']

# Plotting garis untuk masing-masing cluster
fig, ax = plt.subplots(figsize=(10, 6))
rng = range(len(months))
ax.plot(rng, sedikit, marker='o', color='skyblue', label='Sedikit', linewidth=2)
ax.plot(rng, sedang, marker='o', color='salmon', label='Sedang', linewidth=2)
ax.plot(rng, banyak, marker='o', color='teal', label='Banyak', linewidth=2)

# Menambahkan judul dan label
ax.set_xlabel('')
ax.set_ylabel('Jumlah Hari')
bar_width = 0.25
ax.set_xticks([r + bar_width for r in range(len(months))])
ax.set_xticklabels(months, rotation=45, ha='right')
ax.legend()

st.pyplot(fig)