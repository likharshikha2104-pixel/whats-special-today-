import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("places.csv")

# Page configuration
st.set_page_config(
    page_title="What's Special Today?",
    page_icon="✨",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #0f1117;
}

h1 {
    color: white;
    text-align: center;
    font-size: 50px;
}

.stSidebar {
    background-color: #161a23;
}

.card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 20px;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    transition: 0.3s;
          
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
}

.card:hover {
    transform: scale(1.02);
}

.badge {
    background-color: #ff4b4b;
    padding: 6px 12px;
    border-radius: 12px;
    color: white;
    font-size: 14px;
    display: inline-block;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# Title
st.title("✨ What's Special Today?")

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Find the best nearby places within your budget!</h4>",
    unsafe_allow_html=True
)

# Sidebar
search = st.sidebar.text_input(
    "🔎 Search Place"
)

# Filters
location = st.sidebar.selectbox(
    "📍 Select Location",
    df["location"].unique()
)

category = st.sidebar.selectbox(
    "🎯 Select Category",
    df["category"].unique()
)

budget = st.sidebar.slider(
    "💰 Select Budget",
    100,
    2000,
    500
)

distance = st.sidebar.slider(
    "📍 Select Distance (KM)",
    1,
    10,
    5
)
# Filter data
filtered_df = df[
    (df["location"] == location) &
    (df["category"] == category) &
    (df["budget"] <= budget)&
    (df["distance"] <= distance)
]

# Search filter
if search:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(search, case=False)
    ]

# Results section
st.subheader("🔥 Today's Recommendations")

# Display cards
if not filtered_df.empty:

    for index, row in filtered_df.iterrows():

        card = f"""
        <div class="card">

           <img src="{row['image']}"
           style="
               width:100%;
               height:250px;
               object-fit:cover;
               border-radius:15px;
               margin-bottom:15px;
           ">
            <h2>{row['name']}</h2>

            <p>📍 <b>Location:</b> {row['location']}</p>

            <p>🎯 <b>Category:</b> {row['category']}</p>

            <p>💰 <b>Budget:</b> ₹{row['budget']}</p>

            <p>⭐ <b>Rating:</b> {row['rating']}</p>

            <p>📍 <b>Distance:</b> {row['distance']} KM away</p>

            <div class="badge">
                🔥 {row['special']}
            </div>

            <br><br>
 
            <span style="
            background-color:#22c55e;
            padding:6px 12px;
            border-radius:12px;
            font-size:14px;
            ">
            Trending Today
            </span>
        </div>
        """

        st.markdown(card, unsafe_allow_html=True)
else:
    st.warning(" No places found for selected filters.")

# Top Rated Places Section

st.markdown("---")

st.subheader("⭐ Top Rated Places")

# Get top rated places
top_rated = filtered_df.sort_values(
    by="rating",
    ascending=False
).head(5)

for index, row in top_rated.iterrows():

    top_card = f"""
    <div class="card">

        <img src="{row['image']}"
        style="
            width:100%;
            height:220px;
            object-fit:cover;
            border-radius:15px;
            margin-bottom:15px;
        ">

        <h2>{row['name']}</h2>

        <p>⭐ Rating: {row['rating']}</p>

        <p>📍 {row['location']}</p>

    </div>
    """

    st.markdown(top_card, unsafe_allow_html=True)

# Trending Today Section

st.markdown("---")

st.subheader("🔥 Trending Today")

# Trending places
trending_places = filtered_df.sort_values(
    by="rating",
    ascending=False
).head(3)

for index, row in trending_places.iterrows():

    trending_card = f"""
    <div class="card">

        <img src="{row['image']}"
        style="
            width:100%;
            height:220px;
            object-fit:cover;
            border-radius:15px;
            margin-bottom:15px;
        ">

        <h2>{row['name']}</h2>

        <p>⭐ Rating: {row['rating']}</p>

        <p>📍 {row['distance']} KM away</p>

        <div class="badge">
            🔥 Trending Now
        </div>

    </div>
    """

    st.markdown(trending_card, unsafe_allow_html=True)

st.markdown("---")
st.subheader("🗺 Map View")

import folium
from streamlit_folium import st_folium
import geocoder

# Get user location (SAFE)
g = geocoder.ip("me")

if g.latlng is not None:
    user_lat, user_lon = g.latlng
else:
    user_lat, user_lon = 21.1458, 79.0882

# Create map centered on user
m = folium.Map(location=[user_lat, user_lon], zoom_start=12)

# 👤 User marker (blue)
folium.Marker(
    [user_lat, user_lon],
    popup="📍 You are here",
    icon=folium.Icon(color="blue")
).add_to(m)

# 📍 Place markers (red)
for _, row in filtered_df.iterrows():
    if "lat" in row and "lon" in row:
        folium.Marker(
            [row["lat"], row["lon"]],
            popup=f"{row['name']} ({row['category']})",
            tooltip=row["name"],
            icon=folium.Icon(color="red")
        ).add_to(m)

st_folium(m, width=900, height=500)