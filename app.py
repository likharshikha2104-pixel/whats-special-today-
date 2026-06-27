import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# --- PAGE SETUP ---
st.set_page_config(
    page_title="What's Special Today?",
    page_icon="✨",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
/* HIDE WHITE HEADER BAR AT THE VERY TOP */
header, [data-testid="stHeader"], .stAppHeader, #MainMenu {
    background-color: transparent !important;
    display: none !important;
    visibility: hidden !important;
}

.stApp {
    background-color: #0f1117;
    color: white;
    padding-top: 0px !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

/* SLEEK BLACK SIDEBAR OVERRIDE */
section[data-testid="stSidebar"], [data-testid="stSidebar"], .stSidebar {
    background-color: #111827 !important;
    border-right: 1px solid #1f2937 !important;
}

[data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h4 {
    color: #ffffff !important;
}

/* MAKE TYPED INPUT TEXT BLACK INSIDE WHITE BOXES */
[data-testid="stSidebar"] input, 
[data-testid="stSidebar"] div[role="combobox"] *, 
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* FIX FAINT FORM LABELS */
label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span, 
.stTextInput label, .stSelectbox label, .stMultiSelect label, .stNumberInput label, .stSlider label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 15px !important;
}

/* BUTTON STYLING OVERRIDES */
.stButton > button {
    background: linear-gradient(135deg, #dc2626, #991b1b) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: 1px solid #ef4444 !important;
    padding: 6px 16px !important;
    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #ef4444, #dc2626) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 16px rgba(239, 68, 68, 0.5) !important;
}

/* FORM SUBMIT & PRIMARY BUTTONS */
div[data-testid="stFormSubmitButton"] > button, .stButton > button[data-testid="baseButton-primary"] {
    background: linear-gradient(90deg, #ec4899, #8b5cf6) !important;
    border: 1px solid #a855f7 !important;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3) !important;
}

.landing-card {
    background: linear-gradient(135deg, #1e1b4b, #312e81);
    border: 2px solid #6366f1;
    border-radius: 24px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    margin-bottom: 25px;
    transition: all 0.3s ease;
}

.landing-card:hover {
    transform: translateY(-5px);
    border-color: #a855f7;
    box-shadow: 0 15px 35px rgba(168, 85, 247, 0.4);
}

/* COMPACT PLACE CARDS FOR 2-COLUMN DISPLAY */
.compact-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 16px;
    border-radius: 16px;
    margin-bottom: 20px;
    color: white;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    border: 1px solid #374151;
    height: 100%;
}

.compact-card:hover {
    border-color: #ec4899;
}

.compact-card img {
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 12px;
    margin-bottom: 10px;
}

.badge {
    background-color: #ff4b4b;
    padding: 4px 10px;
    border-radius: 10px;
    color: white;
    font-size: 12px;
    display: inline-block;
    margin-top: 6px;
    font-weight: bold;
}

.event-card {
    background: linear-gradient(135deg, #2d1b4e, #1e1b4b);
    border: 1px solid #8b5cf6;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 15px;
}

.hero-box {
    background: linear-gradient(90deg, #ec4899, #8b5cf6);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 25px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- SAFE DATA LOADERS ---
@st.cache_data(ttl=1)
def load_places():
    if os.path.exists("places.csv") and os.path.getsize("places.csv") > 0:
        df = pd.read_csv("places.csv").fillna("")
        for col in ["name", "location", "category", "budget", "rating", "special", "image", "distance", "lat", "lon"]:
            if col not in df.columns:
                df[col] = ""
        if "moods" not in df.columns:
            df["moods"] = "Unexpected Friend Meetup, Chill with Coffee"
        return df
    return pd.DataFrame(columns=["name", "location", "category", "budget", "rating", "special", "image", "distance", "lat", "lon", "moods"])

def load_events():
    if os.path.exists("events.csv") and os.path.getsize("events.csv") > 0:
        df = pd.read_csv("events.csv").fillna("")
        for col in ["id", "place_name", "title", "event_type", "price_or_discount", "date", "time", "description", "tickets_left"]:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=["id", "place_name", "title", "event_type", "price_or_discount", "date", "time", "description", "tickets_left"])

def load_users():
    if os.path.exists("users.csv") and os.path.getsize("users.csv") > 0:
        df = pd.read_csv("users.csv").fillna("")
        for col in ["username", "password", "role", "place_name"]:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=["username", "password", "role", "place_name"])

def load_bookings():
    if os.path.exists("bookings.csv") and os.path.getsize("bookings.csv") > 0:
        df = pd.read_csv("bookings.csv").fillna("")
        for col in ["booking_id", "username", "place_name", "event_title", "tickets_count", "total_price", "status"]:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=["booking_id", "username", "place_name", "event_title", "tickets_count", "total_price", "status"])

# Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = "Customer"
if "owner_place" not in st.session_state:
    st.session_state.owner_place = ""

# --- HERO HEADER ---
st.markdown("""
<div class="hero-box">
    <h1 style="margin:0; font-size: 36px; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">✨ What's Special Today?</h1>
    <p style="margin-top:6px; font-size: 17px; color: #f3e8ff;">Met your friends unexpectedly? Don't know where to chill? Discover live events, student deals & local gems in Nagpur!</p>
</div>
""", unsafe_allow_html=True)

# Navigation Bar / Logout with Cool Glowing Badge
if st.session_state.authenticated:
    col_nav1, col_nav2 = st.columns([3.5, 1.5])
    with col_nav1:
        st.markdown(f"""
        <div style="font-size: 20px; font-weight: 700; color: white; padding-top: 4px;">
            Logged in as <span style="color:#f472b6;">{st.session_state.username}</span> 
            <span style="background: linear-gradient(90deg, #a855f7, #ec4899); color: white; padding: 4px 14px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-left: 8px; box-shadow: 0 2px 8px rgba(168,85,247,0.4);">{st.session_state.role}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_nav2:
        if st.button("🚪 Logout / Switch Portal", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.role = "Customer"
            st.session_state.page = "landing"
            st.rerun()

# ==============================================================================
# SCREEN 1: FIRST LANDING PAGE (ROLE CHOICE GATEWAY)
# ==============================================================================
if st.session_state.page == "landing" and not st.session_state.authenticated:
    st.markdown("<h2 style='text-align:center;'>Welcome! Choose how you would like to continue:</h2><br>", unsafe_allow_html=True)
    
    col_cust, col_owner = st.columns(2)
    
    with col_cust:
        st.markdown("""
        <div class="landing-card">
            <h2 style="font-size:28px; margin-bottom:10px;">👤 I am a Customer / Explorer</h2>
            <p style="color:#cbd5e1; font-size:16px;">Looking for places to hangout with friends based on your current mood, budget, and live events in Nagpur!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Enter Customer Portal", key="goto_cust", use_container_width=True, type="primary"):
            st.session_state.page = "customer_auth"
            st.rerun()
            
    with col_owner:
        st.markdown("""
        <div class="landing-card">
            <h2 style="font-size:28px; margin-bottom:10px;">🏪 I am a Shop / Place Owner</h2>
            <p style="color:#cbd5e1; font-size:16px;">Register your cafe, pub, or store. Promote underrated spots, post flash sales, live acoustic shows & sell tickets!</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏬 Enter Shop Owner Portal", key="goto_owner", use_container_width=True, type="primary"):
            st.session_state.page = "owner_auth"
            st.rerun()

# ==============================================================================
# SCREEN 2A: CUSTOMER AUTHENTICATION PAGE
# ==============================================================================
elif st.session_state.page == "customer_auth" and not st.session_state.authenticated:
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.update({"page": "landing"}))
    st.subheader("👤 Customer Access Portal")
    
    auth_tab1, auth_tab2 = st.tabs(["🔓 Customer Login", "📝 New Customer Registration"])
    
    with auth_tab1:
        u_in = st.text_input("Username", key="c_log_u")
        p_in = st.text_input("Password", type="password", key="c_log_p")
        if st.button("Log In as Customer", type="primary"):
            users_df = load_users()
            match = users_df[(users_df["username"] == u_in) & (users_df["password"] == p_in) & (users_df["role"] == "Customer")]
            if not match.empty:
                st.session_state.authenticated = True
                st.session_state.username = u_in
                st.session_state.role = "Customer"
                st.session_state.page = "customer_app"
                st.success("Welcome!")
                st.rerun()
            else:
                st.error("Invalid Customer credentials. Or try registering first!")
                
    with auth_tab2:
        reg_u = st.text_input("Choose Username", key="c_reg_u")
        reg_p = st.text_input("Choose Password", type="password", key="c_reg_p")
        if st.button("Create Customer Account"):
            if reg_u and reg_p:
                users_df = load_users()
                if reg_u in users_df["username"].values:
                    st.error("Username already exists!")
                else:
                    new_u = pd.DataFrame([{"username": reg_u, "password": reg_p, "role": "Customer", "place_name": "None"}])
                    pd.concat([users_df, new_u], ignore_index=True).to_csv("users.csv", index=False)
                    st.success("Account created! Please switch to Login tab.")
            else:
                st.error("Please fill all fields.")

# ==============================================================================
# SCREEN 2B: SHOP OWNER AUTHENTICATION & ENHANCED REGISTRATION
# ==============================================================================
elif st.session_state.page == "owner_auth" and not st.session_state.authenticated:
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.update({"page": "landing"}))
    st.subheader("🏪 Shop / Place Owner Access & Business Setup")
    
    o_tab1, o_tab2 = st.tabs(["🔓 Owner Login", "🏬 Register Business & Create Owner Account"])
    
    with o_tab1:
        ou_in = st.text_input("Owner Username", key="o_log_u")
        op_in = st.text_input("Owner Password", type="password", key="o_log_p")
        if st.button("Log In as Shop Owner", type="primary"):
            users_df = load_users()
            match = users_df[(users_df["username"] == ou_in) & (users_df["password"] == op_in) & (users_df["role"] == "Shop Owner")]
            if not match.empty:
                st.session_state.authenticated = True
                st.session_state.username = ou_in
                st.session_state.role = "Shop Owner"
                st.session_state.owner_place = match.iloc[0]["place_name"]
                st.session_state.page = "owner_app"
                st.success("Welcome, Business Owner!")
                st.rerun()
            else:
                st.error("Invalid Owner credentials!")
                
    with o_tab2:
        st.markdown("### Register Your Business (Underrated Gems Welcome!)")
        st.caption("Provide your place details so customers searching by mood and budget can find you instantly!")
        
        with st.form("owner_full_reg_form"):
            col_reg1, col_reg2 = st.columns(2)
            with col_reg1:
                new_ou = st.text_input("Owner Username *")
                new_op = st.text_input("Owner Password *", type="password")
                biz_name = st.text_input("Business / Place Name * (e.g. Chillout Cafe)")
                biz_loc = st.text_input("Region / Location * (e.g. Dharampeth, Sadar)")
                biz_cat = st.selectbox("Category", ["Cafe", "Restaurant", "Mall", "Tourist Attraction", "Park", "Hotel"])
            with col_reg2:
                biz_budget = st.number_input("Average Budget per Person (₹)", min_value=50, value=400)
                biz_special = st.text_input("Special Highlight / Offer (e.g. Live Comedy, Best Cold Brew)")
                biz_moods = st.multiselect("Select Target Hangout Moods Supported *", [
                    "Unexpected Friend Meetup",
                    "Chill with Coffee & Conversations",
                    "Delicious Budget Eats",
                    "Shopping & Bargains",
                    "Peaceful Nature & Lake View",
                    "Nightlife & Live Shows"
                ], default=["Unexpected Friend Meetup", "Chill with Coffee & Conversations"])
                biz_img = st.text_input("Image URL", value="https://images.unsplash.com/photo-1554118811-1e0d58224f24")
                biz_dist = st.number_input("Distance from Nagpur Center (KM)", min_value=1, value=3)
                
            sub_biz = st.form_submit_button("🔥 Register Business & Account")
            if sub_biz:
                if new_ou and new_op and biz_name and biz_loc:
                    users_df = load_users()
                    places_df = load_places()
                    if new_ou in users_df["username"].values:
                        st.error("Username taken!")
                    else:
                        new_u_row = pd.DataFrame([{"username": new_ou, "password": new_op, "role": "Shop Owner", "place_name": biz_name}])
                        pd.concat([users_df, new_u_row], ignore_index=True).to_csv("users.csv", index=False)
                        
                        mood_str = ", ".join(biz_moods)
                        new_p_row = pd.DataFrame([{
                            "name": biz_name, "location": biz_loc, "category": biz_cat,
                            "budget": biz_budget, "rating": 4.5, "special": biz_special,
                            "image": biz_img, "distance": biz_dist, "lat": 21.1458, "lon": 79.0882,
                            "moods": mood_str
                        }])
                        pd.concat([places_df, new_p_row], ignore_index=True).to_csv("places.csv", index=False)
                        st.cache_data.clear()
                        st.success(f"🎉 **{biz_name}** successfully registered! You can now log in using your credentials.")
                else:
                    st.error("Please fill in all required fields marked with *.")

# ==============================================================================
# SCREEN 3A: CUSTOMER DASHBOARD (MAIN APP)
# ==============================================================================
elif st.session_state.page in ["customer_app", "landing"] and (st.session_state.authenticated or st.session_state.page == "landing"):
    df_places = load_places()
    
    tab_explore, tab_events, tab_my_bookings = st.tabs(["🔎 Explore Nearby & Moods", "🎟️ Live Events & Flash Sales", "🎫 My Bookings"])
    
    with tab_explore:
        st.sidebar.markdown("<h4>🔎 Search & Mood Engine</h4>", unsafe_allow_html=True)
        
        search = st.sidebar.text_input("Search Place Name")
        
        mood = st.sidebar.selectbox("🎯 Your Current Hangout Mood", [
            "Any Mood",
            "Unexpected Friend Meetup",
            "Chill with Coffee & Conversations",
            "Delicious Budget Eats",
            "Shopping & Bargains",
            "Peaceful Nature & Lake View"
        ])
        
        locations = ["All Locations"] + sorted(df_places["location"].astype(str).unique().tolist()) if not df_places.empty else ["All Locations"]
        location = st.sidebar.selectbox("📍 Select Region", locations)
        
        categories = ["All Categories"] + sorted(df_places["category"].astype(str).unique().tolist()) if not df_places.empty else ["All Categories"]
        category = st.sidebar.selectbox("🏷️ Select Category", categories)
        
        budget = st.sidebar.slider("💰 Max Budget (₹)", 100, 3000, 1200)
        distance = st.sidebar.slider("📍 Max Distance (KM)", 1, 20, 10)
        
        filtered_df = df_places.copy() if not df_places.empty else pd.DataFrame()
        
        if not filtered_df.empty:
            if location != "All Locations":
                filtered_df = filtered_df[filtered_df["location"] == location]
                
            if category != "All Categories":
                filtered_df = filtered_df[filtered_df["category"] == category]
                
            filtered_df = filtered_df[
                (filtered_df["budget"] <= budget) &
                (filtered_df["distance"] <= distance)
            ]
            
            if mood != "Any Mood":
                filtered_df = filtered_df[filtered_df["moods"].str.contains(mood, case=False, na=False) | filtered_df["category"].isin(["Cafe", "Restaurant"])]

            if search:
                filtered_df = filtered_df[filtered_df["name"].str.contains(search, case=False)]
            
        st.success(f"🎯 Found **{len(filtered_df)} places** matching your mood and budget in Nagpur!")
        
        # 2-COLUMN COMPACT GRID FOR PLACES
        if not filtered_df.empty:
            rows = list(filtered_df.iterrows())
            for i in range(0, len(rows), 2):
                col1, col2 = st.columns(2)
                
                with col1:
                    row = rows[i][1]
                    card_html = f"""
                    <div class="compact-card">
                        <img src="{row['image']}">
                        <h3 style="margin:0; font-size:20px;">{row['name']}</h3>
                        <p style="margin-top:4px; color:#a1a1aa; font-size:13px;">📍 {row['location']} | 🎯 {row['category']}</p>
                        <p style="color:#e4e4e7; font-size:13px;">💰 <b>₹{row['budget']}</b> | ⭐ <b>{row['rating']}</b> | 📍 <b>{row['distance']} KM</b></p>
                        <div class="badge">🔥 {row['special']}</div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                if i + 1 < len(rows):
                    with col2:
                        row2 = rows[i+1][1]
                        card_html2 = f"""
                        <div class="compact-card">
                            <img src="{row2['image']}">
                            <h3 style="margin:0; font-size:20px;">{row2['name']}</h3>
                            <p style="margin-top:4px; color:#a1a1aa; font-size:13px;">📍 {row2['location']} | 🎯 {row2['category']}</p>
                            <p style="color:#e4e4e7; font-size:13px;">💰 <b>₹{row2['budget']}</b> | ⭐ <b>{row2['rating']}</b> | 📍 <b>{row2['distance']} KM</b></p>
                            <div class="badge">🔥 {row2['special']}</div>
                        </div>
                        """
                        st.markdown(card_html2, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.warning("No places found for selected filters.")

        st.markdown("---")
        st.subheader("🗺️ Interactive Nagpur Map View")
        nagpur_lat, nagpur_lon = 21.1458, 79.0882
        m = folium.Map(location=[nagpur_lat, nagpur_lon], zoom_start=12)
        folium.Marker([nagpur_lat, nagpur_lon], popup="📍 You are here (Nagpur)", icon=folium.Icon(color="blue", icon="user")).add_to(m)
        
        if not filtered_df.empty:
            for _, row in filtered_df.iterrows():
                if pd.notna(row["lat"]) and pd.notna(row["lon"]) and row["lat"] != "" and row["lon"] != "":
                    try:
                        folium.Marker(
                            [float(row["lat"]), float(row["lon"])],
                            popup=f"<b>{row['name']}</b><br>Rating: {row['rating']}<br>Budget: ₹{row['budget']}",
                            tooltip=row["name"],
                            icon=folium.Icon(color="red")
                        ).add_to(m)
                    except Exception:
                        pass
        st_folium(m, width=900, height=450)

    with tab_events:
        st.subheader("🎟️ Live Events & Exclusive Owner Flash Sales")
        events_df = load_events()
        if not events_df.empty:
            for idx, evt in events_df.iterrows():
                st.markdown(f"""
                <div class="event-card">
                    <span style="background:#8b5cf6; padding:4px 10px; border-radius:8px; font-weight:bold; font-size:12px;">{evt['event_type']}</span>
                    <h3 style="margin-top:8px; margin-bottom:4px;">{evt['title']} @ {evt['place_name']}</h3>
                    <p style="color:#cbd5e1; margin-bottom:8px;">📅 Date: <b>{evt['date']}</b> at <b>{evt['time']}</b> | 💸 Offer/Price: <b>{evt['price_or_discount']}</b></p>
                    <p>{evt['description']}</p>
                    <p style="color:#a7f3d0; font-weight:bold;">🎟️ Seats Left: {evt['tickets_left']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🎟️ Book Ticket / Lock Offer for '{evt['title']}'", key=f"book_btn_{evt['id']}"):
                    if not st.session_state.authenticated:
                        st.warning("Please log in as a Customer to book tickets!")
                    else:
                        bookings_df = load_bookings()
                        new_b = pd.DataFrame([{
                            "booking_id": f"BK{100+len(bookings_df)+1}",
                            "username": st.session_state.username,
                            "place_name": evt['place_name'],
                            "event_title": evt['title'],
                            "tickets_count": 1,
                            "total_price": evt['price_or_discount'],
                            "status": "Confirmed"
                        }])
                        pd.concat([bookings_df, new_b], ignore_index=True).to_csv("bookings.csv", index=False)
                        st.balloons()
                        st.success(f"🎉 Reserved 1 seat for '{evt['title']}'! View in 'My Bookings'.")
                st.divider()
        else:
            st.info("No active events currently posted.")

    with tab_my_bookings:
        st.subheader("🎫 Your Reserved Tickets & RSVPs")
        if st.session_state.authenticated:
            bookings_df = load_bookings()
            if not bookings_df.empty:
                user_b = bookings_df[bookings_df["username"] == st.session_state.username]
                if not user_b.empty:
                    st.dataframe(user_b, use_container_width=True)
                else:
                    st.info("You haven't booked any tickets yet.")
            else:
                st.info("No bookings registered in system.")
        else:
            st.warning("Please log in to view your bookings.")

# ==============================================================================
# SCREEN 3B: SHOP OWNER DASHBOARD
# ==============================================================================
elif st.session_state.page == "owner_app" and st.session_state.authenticated and st.session_state.role == "Shop Owner":
    st.header(f"🏪 Shop Owner Portal — Welcome, {st.session_state.username}!")
    st.caption(f"Managing Business: **{st.session_state.owner_place}**")
    
    owner_tab1, owner_tab2 = st.tabs(["📢 Post Event or Flash Sale", "📋 Customer Bookings"])
    
    with owner_tab1:
        st.subheader("Post a Standup Show, Live Music, or Limited-Time Flash Sale")
        with st.form("add_event_form_owner"):
            place_name = st.text_input("Place Name", value=st.session_state.owner_place)
            title = st.text_input("Event / Sale Title (e.g. Comedy Night, Buy 1 Get 1 Coffee)")
            event_type = st.selectbox("Type", ["Event (Show/Concert)", "Flash Sale (Food/Shopping)", "Special Offer"])
            price_discount = st.text_input("Price or Discount (e.g. ₹299 or 30% OFF)")
            event_date = st.date_input("Date")
            event_time = st.time_input("Time")
            desc = st.text_area("Description")
            tickets_qty = st.number_input("Available Seats / Passes", min_value=1, value=30)
            
            submit_evt = st.form_submit_button("🔥 Publish to App Customers")
            if submit_evt:
                if title:
                    events_df = load_events()
                    new_evt = pd.DataFrame([{
                        "id": len(events_df) + 1,
                        "place_name": place_name,
                        "title": title,
                        "event_type": event_type,
                        "price_or_discount": price_discount,
                        "date": str(event_date),
                        "time": event_time.strftime("%I:%M %p"),
                        "description": desc,
                        "tickets_left": tickets_qty
                    }])
                    pd.concat([events_df, new_evt], ignore_index=True).to_csv("events.csv", index=False)
                    st.success("🎉 Event published live! Customers browsing the app can now book passes.")
                else:
                    st.error("Please enter an Event Title.")
                    
    with owner_tab2:
        st.subheader("📥 Live Ticket Bookings for Your Place")
        bookings_df = load_bookings()
        if not bookings_df.empty:
            filtered_b = bookings_df[bookings_df["place_name"] == st.session_state.owner_place]
            if not filtered_b.empty:
                st.dataframe(filtered_b, use_container_width=True)
            else:
                st.info(f"No bookings for {st.session_state.owner_place} yet.")
        else:
            st.info("No bookings registered yet.")
