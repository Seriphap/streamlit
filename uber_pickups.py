
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
print(selected_date)
# Filter data based on selected date
filtered_data = data[data[DATE_COLUMN] == selected_date]
print(filtered_data)
st.subheader(f"3D Map of pickups on {selected_date}")
# Ensure filtered data has latitude and longitude
if not filtered_data.empty:
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=filtered_data['lat'].mean(),
            longitude=filtered_data['lon'].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=filtered_data,
                get_position='[lon, lat]',
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                     
            ),
        ],
    ))
else:
    st.warning("No data available for the selected date.")

import streamlit as st
import pandas as pd
import pydeck as pdk

# Display title in Streamlit
st.title('2. Use Date Input')

# Load the data (ensure the CSV file exists and has the required columns)
DATA_FILE = "data.csv"  # Adjust the filename as needed
DATE_COLUMN = "date"  # Replace with your actual date column name

try:
    data = pd.read_csv(DATA_FILE)  # Load your data
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])  # Convert to datetime if necessary
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Date input widget for user interaction
selected_date = st.date_input("Select a date", data[DATE_COLUMN].min())  # Default to the earliest date
st.write(f"Selected date: {selected_date}")

# Filter data based on selected date
filtered_data = data[data[DATE_COLUMN] == pd.Timestamp(selected_date)]
st.write(f"Filtered data: {filtered_data.shape[0]} rows")

# Ensure filtered data has latitude and longitude columns
LAT_COLUMN = "lat"  # Replace with your latitude column name
LON_COLUMN = "lon"  # Replace with your longitude column name

if filtered_data.empty:
    st.warning("No data available for the selected date.")
else:
    st.subheader(f"3D Map of pickups on {selected_date}")
    
    # Pydeck chart for visualization
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=filtered_data[LAT_COLUMN].mean(),
            longitude=filtered_data[LON_COLUMN].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=filtered_data,
                get_position=f"[{LON_COLUMN}, {LAT_COLUMN}]",  # Use column names
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ],
    ))


#3. Use Selectbox
st.title('#3. Use Selectbox')
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

