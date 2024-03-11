import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


# Helper Function
def create_season_df(df):
    season_df = df.groupby(by='season').agg({
        "cnt" : "sum"
    })
        
    return season_df

def create_month_df(df):
    month_df = df.groupby(by='mnth').agg({
        "cnt" : "sum"
    })
    
    return month_df

def create_hour_df(df):
    hour_df = df.groupby(by='hr').agg({
        "cnt" : "sum"
    }).sort_values(by='hr', ascending=False)
    
    return hour_df

def create_workingday_df(df):
    workingday_df = df.groupby(by='workingday').agg({
        "cnt" : "sum"
    })
    
    return workingday_df

def create_weather_df(df):
    weathersit_df = df.groupby(by='weathersit').agg({
        "cnt" : "sum"
    })
    
    return weathersit_df



all_df = pd.read_csv("dashboard\data.csv")
all_df["dteday"] = pd.to_datetime(all_df['dteday'])
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQVmG4CoRPFsQf_hQkA6B-tlkfdJsaSTpjBzg&usqp=CAU")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

season_df = create_season_df(main_df)
month_df = create_month_df(main_df)
hour_df = create_hour_df(main_df)
workingday_df = create_workingday_df(main_df)
weather_df = create_weather_df(main_df)


st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Daily Bike Sharing')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_cas_rent = main_df.casual.sum()
    st.metric("Total Casul Bike Rent", value=total_cas_rent)

with col2:
    total_reg_rent = main_df.registered.sum()
    st.metric("Total Registered Bike Rent", value=total_reg_rent)

with col3:
    total_all_rent = main_df.cnt.sum()
    st.metric("Total All Bike Rent", value=total_all_rent)
  
st.subheader("Best Season For Rent Bike")
 
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(35, 15))
 
colors = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"]
season_names = ['Spring', 'Summer', 'Fall', 'Winter']

sns.barplot(x=season_names, y="cnt", data=season_df, palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel("Season", fontsize=30)
ax.invert_xaxis()
ax.set_title("Best Season", loc="center", fontsize=50)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

st.subheader("Best Time Rent")
 
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(x="mnth", y="cnt", data=month_df, errorbar=None)
plt.title("User Rent by Hour")
plt.xlabel("Month")
plt.ylabel(None)
plt.show()
st.pyplot(plt)

sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(x="hr", y="cnt", data=hour_df, errorbar=None)
plt.title("User Rent by Hour")
plt.xlabel("Hour")
plt.ylabel(None)
plt.show()
st.pyplot(plt)

# customer demographic
st.subheader("User Rent Bike by Working Day & Weather")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 20))

    colors = ["#D3D3D3", "#90CAF9"]

    sns.barplot(
        y="cnt", 
        x=["Holiday", "Workingday"],
        data=workingday_df,
        palette=colors,
        ax=ax
        )
    ax.set_title("Number of Rent Bike by Working Day", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=50)
    ax.tick_params(axis='y', labelsize=50)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 20))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="cnt", 
        x=["Clear", "Mist", "Light Snow", "Heavy Rain"],
        data=weather_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rent Bike by Weather", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=50)
    ax.tick_params(axis='y', labelsize=50)
    st.pyplot(fig)

st.caption('Copyright (c) Muh Royan Fauzi M 2024')