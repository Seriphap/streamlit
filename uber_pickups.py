
#1. Convert 2D mao to 3D map usind PyDeck
#2. Use date input
#3. Use Selectbox
#4. Use plotly (any charts)
#5. Click a button to increase the number in the following message, "This page has run 24 times"

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.title('Uber pickups in NYC2')
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')
data

#1. Convert 2D mao to 3D map usind PyDeck
st.title('1. Convert 2D map to 3D map usind PyDeck')
st.subheader('3D Map of all pickups')
# Ensure your data has 'lat' and 'lon' columns (or rename accordingly)
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=data['lat'].mean(),
        longitude=data['lon'].mean(),
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=data,
            get_position='[lon, lat]',
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))

#2. Use date input
st.title('2. Use date input')
# Date input widget for user interaction
selected_date = st.date_input("Select a date", data[DATE_COLUMN].min())
Min_Date = data[DATE_COLUMN].min().date()
Max_Date = data[DATE_COLUMN].max().date()
st.write(f"Record Date from {Min_Date} to {Max_Date} ")

# Convert the 'DATE_COLUMN' to a date format (ignore time part) and create a new column
data['date_only'] = pd.to_datetime(data[DATE_COLUMN]).dt.date
# Filter data based on selected date
filtered_data = data[data['date_only'] == selected_date]
#filtered_data
st.map(filtered_data)

#3. Use Selectbox
st.title('#3. Use Selectbox')
# Add a selectbox for date selection
selected_date = st.selectbox(
    'Select a date',
    options=data[DATE_COLUMN].dt.date.unique(),
    format_func=lambda date: date.strftime('%Y-%m-%d')  # Format the dates for display
)
# Filter the data based on the selected date
filtered_data = data[data[DATE_COLUMN].dt.date == selected_date]
# Display subheader and calculate histogram values
st.subheader(f'Number of pickups by hour on {selected_date}')
hist_values = np.histogram(filtered_data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
# Display the bar chart
st.bar_chart(hist_values)


#4. Use plotly (any charts)
!pip install plotly
import plotly.express as px
st.title('4. Use plotly (any charts)')
# Add a selectbox for date selection
selected_date = st.selectbox(
    'Select a date',
    options=data[DATE_COLUMN].dt.date.unique(),
    format_func=lambda date: date.strftime('%Y-%m-%d')  # Format the dates for display
)

# Filter the data based on the selected date
filtered_data = data[data[DATE_COLUMN].dt.date == selected_date]

# Display subheader
st.subheader(f'Number of pickups by hour on {selected_date}')

# Calculate histogram values for hours (bins = 24, range from 0 to 24 hours)
hist_values = np.histogram(filtered_data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]

# Create a DataFrame for Plotly Express
hourly_data = pd.DataFrame({
    'Hour': np.arange(24),  # Hours 0-23
    'Pickups': hist_values
})

# Create a bar chart using Plotly Express
fig = px.bar(hourly_data, x='Hour', y='Pickups',
             labels={'Hour': 'Hour of Day', 'Pickups': 'Number of Pickups'},
             title=f'Number of Uber Pickups by Hour on {selected_date}')

# Customize layout (optional)
fig.update_layout(
    xaxis_title='Hour of Day',
    yaxis_title='Number of Pickups',
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
)

# Display the plotly chart in Streamlit
st.plotly_chart(fig)


