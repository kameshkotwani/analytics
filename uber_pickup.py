import streamlit as st
import numpy as np
import pandas as pd

st.title('Uber Pickups in New York City!')

# creating consts for data fetching
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


# function to load the data
@st.cache  # we use st.chache to avoid data loading everytime we run the app
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    # change data to lowercase
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# create a state for a user to show that data is loading
data_load_state = st.text('Loading data...')

# load the data
df = load_data(10000)

# notify that data load is done
data_load_state.text('Loading data is done!')
see_data = st.checkbox('See Raw Data')
if see_data:
    st.subheader('Raw Data')
    st.dataframe(df.head())

st.header('Busiest Hours of New York City')
hist_values = np.histogram(df[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

st.header('Map of all Pickups!')
st.map(df)

hour_filter = st.slider('hour',0,23,17)
st.subheader(f'Map of all pickups at {hour_filter}:00')
filtered_df = df[df[DATE_COLUMN].dt.hour == hour_filter]
st.map(filtered_df)
