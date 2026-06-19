import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

st.set_page_config(
    page_title="Food Wastage Management",
    page_icon="🍽️",
    layout="wide"
)

engine = create_engine("mysql+mysqlconnector://root:2004@localhost/food_wastage_db")

if "active_page" not in st.session_state:
    st.session_state.active_page = "🏠 Home"

st.markdown("""
<style>
    /* Dark theme base */
    .stApp {
        background: linear-gradient(180deg, #1f2330 0%, #262b3a 100%);
    }
    section[data-testid="stSidebar"] {
        background-color: #2a2f3f !important;
        border-right: 1px solid #454c63;
    }
    section[data-testid="stSidebar"] * { color: #d4d6dd !important; }

    header[data-testid="stHeader"] { background: transparent; }

    /* Sidebar radio styled as nav pills */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: transparent;
        border-radius: 10px;
        padding: 10px 14px;
        margin-bottom: 4px;
        transition: background 0.15s ease;
        width: 100%;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: #3a4055;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
        border-color: #4f5468 !important;
    }

    /* Metric cards */
    .metric-card {
        background: #2e3344;
        border-radius: 16px;
        padding: 24px 18px;
        text-align: center;
        border: 1px solid #454c63;
        margin-bottom: 14px;
        transition: all 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: #3a3f54;
    }
    .metric-card .number { font-size: 36px; font-weight: 700; margin: 4px 0 4px; letter-spacing: -0.5px; }
    .metric-card .label { font-size: 12px; color: #aeb2c2; letter-spacing: 0.8px; font-weight: 500; }

    /* Insight cards */
    .insight-card {
        background: #2e3344;
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        border: 1px solid #454c63;
        margin-bottom: 14px;
    }
    .insight-card h4 { color: #aeb2c2 !important; font-size: 12px; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .insight-card h3 { font-size: 19px; margin: 4px 0; font-weight: 600; }
    .insight-card p { color: #9aa0b5 !important; font-size: 13px; margin: 0; }

    /* Section title */
    .section-title {
        font-size: 17px;
        font-weight: 600;
        color: #d4d6dd !important;
        margin: 32px 0 16px;
        padding-bottom: 10px;
        border-bottom: 1px solid #454c63;
        letter-spacing: 0.2px;
    }

    /* About box */
    .about-box {
        background: #2e3344;
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #454c63;
        margin-top: 10px;
    }
    .about-box h3 { color: #d4d6dd !important; margin-bottom: 14px; }
    .about-box p { color: #c5c9d4 !important; font-size: 15px; line-height: 1.9; }

    /* Dataframe */
    .stDataFrame { border-radius: 12px; overflow: hidden; border: 1px solid #454c63; }

    /* Buttons */
    .stButton > button {
        background: #4f46e5;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 22px;
        font-size: 14px;
        font-weight: 600;
        width: 100%;
        transition: background 0.15s ease;
    }
    .stButton > button:hover { background: #4338ca; color: white; }
    .stButton > button:disabled { background: #4a5169; color: #8a90a5 !important; }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox > div > div, .stDateInput input {
        background: #2e3344 !important;
        color: #d4d6dd !important;
        border: 1px solid #4a5169 !important;
        border-radius: 10px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #4f46e5 !important;
        box-shadow: 0 0 0 1px #4f46e5 !important;
    }

    /* Success/Error */
    .stSuccess { background: #0f2419 !important; border: 1px solid #1f7a4d !important; border-radius: 10px !important; }
    .stError { background: #271215 !important; border: 1px solid #b3423f !important; border-radius: 10px !important; }
    .stInfo { background: #14202b !important; border: 1px solid #2b5a78 !important; border-radius: 10px !important; }
    .stWarning { background: #2b2310 !important; border: 1px solid #8a6d1f !important; border-radius: 10px !important; }

    /* General text */
    h1, h2, h3, h4, h5 { color: #e4e6eb !important; font-weight: 600; }
    p, label { color: #c5c9d4 !important; }
    .stMarkdown p { color: #c5c9d4 !important; }

    /* Tighter hr */
    hr { margin: 14px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 24px 0 16px;'>
            <div style='font-size:38px; line-height:1;'>🍽️</div>
            <h2 style='color:#e4e6eb; font-size:16px; margin:10px 0 2px; font-weight:600;'>Food Wastage</h2>
            <p style='color:#9aa0b5; font-size:12px; margin:0;'>Management System</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#454c63;'>", unsafe_allow_html=True)
    pages = ["🏠 Home", "📊 SQL Queries", "🔍 Filters", "➕ CRUD Operations", "📈 EDA Charts"]
    page = st.radio("", pages, index=pages.index(st.session_state.active_page))
    st.session_state.active_page = page
    st.markdown("<hr style='border-color:#454c63;'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8a90a5; font-size:11px; text-align:center;'>Built with Python & Streamlit</p>", unsafe_allow_html=True)

# ============ HOME ============
if page == "🏠 Home":

    total_providers = pd.read_sql("SELECT COUNT(*) AS total FROM providers", engine).iloc[0,0]
    total_receivers = pd.read_sql("SELECT COUNT(*) AS total FROM receivers", engine).iloc[0,0]
    total_food = pd.read_sql("SELECT COUNT(*) AS total FROM food_listings", engine).iloc[0,0]
    total_claims = pd.read_sql("SELECT COUNT(*) AS total FROM claims", engine).iloc[0,0]
    total_quantity = pd.read_sql("SELECT SUM(Quantity) AS total FROM food_listings", engine).iloc[0,0]
    completed = pd.read_sql("SELECT COUNT(*) AS total FROM claims WHERE Status='Completed'", engine).iloc[0,0]

    # Hero Banner
    st.markdown("""
        <div style='background: radial-gradient(circle at top left, #343a4d 0%, #12141d 60%);
                    border: 1px solid #454c63;
                    padding: 38px 34px; border-radius: 18px; margin-bottom: 30px;
                    position: relative; overflow: hidden;'>
            <div style='position:absolute; top:-40px; right:-40px; width:160px; height:160px;
                        background: radial-gradient(circle, #4f46e533, transparent 70%); border-radius:50%;'></div>
            <h1 style='color:#e4e6eb; font-size:30px; margin:0 0 10px; font-weight:700; position:relative;'>
                🍽️ Local Food Wastage Management System
            </h1>
            <p style='color:#c5c9d4; font-size:15px; margin:0; position:relative;'>
                Connecting food providers with those in need — reducing waste, feeding lives.
            </p>
            <div style='margin-top:18px; display:flex; gap:8px; position:relative;'>
                <span style='background:#343a4d; color:#a5b4fc; padding:5px 14px; border-radius:20px; font-size:12px; border:1px solid #525a72; font-weight:500;'>Python</span>
                <span style='background:#343a4d; color:#a5b4fc; padding:5px 14px; border-radius:20px; font-size:12px; border:1px solid #525a72; font-weight:500;'>MySQL</span>
                <span style='background:#343a4d; color:#a5b4fc; padding:5px 14px; border-radius:20px; font-size:12px; border:1px solid #525a72; font-weight:500;'>Streamlit</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Metrics — single cohesive accent (indigo) with subtle variation via opacity
    st.markdown("<p class='section-title'>📊 Live Dashboard</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'><div class='number' style='color:#818cf8;'>{total_providers}</div><div class='label'>🏪 TOTAL PROVIDERS</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div class='number' style='color:#34d399;'>{total_receivers}</div><div class='label'>🤝 TOTAL RECEIVERS</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><div class='number' style='color:#fbbf24;'>{total_food}</div><div class='label'>🍱 FOOD LISTINGS</div></div>", unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)
    c4.markdown(f"<div class='metric-card'><div class='number' style='color:#f87171;'>{total_claims}</div><div class='label'>📋 TOTAL CLAIMS</div></div>", unsafe_allow_html=True)
    c5.markdown(f"<div class='metric-card'><div class='number' style='color:#34d399;'>{completed}</div><div class='label'>✅ COMPLETED CLAIMS</div></div>", unsafe_allow_html=True)
    c6.markdown(f"<div class='metric-card'><div class='number' style='color:#60a5fa;'>{int(total_quantity)}</div><div class='label'>🥘 TOTAL FOOD UNITS</div></div>", unsafe_allow_html=True)

    # Quick Insights
    st.markdown("<p class='section-title'>🔍 Quick Insights</p>", unsafe_allow_html=True)
    top_city = pd.read_sql("SELECT Location, COUNT(*) as total FROM food_listings GROUP BY Location ORDER BY total DESC LIMIT 1", engine)
    top_provider = pd.read_sql("SELECT Type, COUNT(*) as total FROM providers GROUP BY Type ORDER BY total DESC LIMIT 1", engine)
    top_food = pd.read_sql("SELECT Food_Name, COUNT(*) as total FROM food_listings GROUP BY Food_Name ORDER BY total DESC LIMIT 1", engine)

    i1, i2, i3 = st.columns(3)
    i1.markdown(f"<div class='insight-card' style='border-top:2px solid #818cf8;'><h4>Top City</h4><h3 style='color:#818cf8;'>{top_city.iloc[0,0]}</h3><p>{top_city.iloc[0,1]} listings</p></div>", unsafe_allow_html=True)
    i2.markdown(f"<div class='insight-card' style='border-top:2px solid #34d399;'><h4>Top Provider Type</h4><h3 style='color:#34d399;'>{top_provider.iloc[0,0]}</h3><p>{top_provider.iloc[0,1]} providers</p></div>", unsafe_allow_html=True)
    i3.markdown(f"<div class='insight-card' style='border-top:2px solid #fbbf24;'><h4>Top Food Item</h4><h3 style='color:#fbbf24;'>{top_food.iloc[0,0]}</h3><p>{top_food.iloc[0,1]} listings</p></div>", unsafe_allow_html=True)

    # Quick Navigation
    st.markdown("<p class='section-title'>🚀 Jump To</p>", unsafe_allow_html=True)
    n1, n2, n3, n4 = st.columns(4)
    with n1:
        if st.button("📊 View Queries", key="nav_sql"):
            st.session_state.active_page = "📊 SQL Queries"
            st.rerun()
    with n2:
        if st.button("🔍 Filter Food", key="nav_filter"):
            st.session_state.active_page = "🔍 Filters"
            st.rerun()
    with n3:
        if st.button("➕ Manage Data", key="nav_crud"):
            st.session_state.active_page = "➕ CRUD Operations"
            st.rerun()
    with n4:
        if st.button("📈 View Charts", key="nav_eda"):
            st.session_state.active_page = "📈 EDA Charts"
            st.rerun()

    # About
    st.markdown("<p class='section-title'>🌍 About This Project</p>", unsafe_allow_html=True)
    st.markdown("""
        <div class='about-box'>
            <p>
                This system helps <b style='color:#818cf8;'>reduce food wastage</b> by connecting food providers
                (restaurants, supermarkets, catering services) with receivers
                (NGOs, individuals, shelters, community centers).<br><br>
                Built with <b style='color:#34d399;'>Python, MySQL & Streamlit</b> — it manages food listings,
                tracks claims, and provides insights through 15 SQL queries and data visualizations.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ============ SQL QUERIES ============
elif page == "📊 SQL Queries":
    st.markdown("<h1 style='color:#e4e6eb;'>📊 SQL Queries</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2e3148;'>", unsafe_allow_html=True)

    all_query_names = [
        "Q1 - Providers & Receivers by City",
        "Q2 - Provider Type Contribution",
        "Q3 - Provider Contact Info by City",
        "Q4 - Top Receivers by Claims",
        "Q5 - Total Food Available",
        "Q6 - City with Most Listings",
        "Q7 - Most Common Food Types",
        "Q8 - Claims per Food Item",
        "Q9 - Provider with Most Successful Claims",
        "Q10 - Claim Status Breakdown",
        "Q11 - Avg Quantity per Receiver",
        "Q12 - Most Claimed Meal Type",
        "Q13 - Total Donated by Provider",
        "Q14 - Earliest Expiring Items",
        "Q15 - Top 5 Cities by Quantity"
    ]

    keyword = st.text_input("🔎 Search queries by keyword", placeholder="e.g. city, claims, provider...")
    filtered_names = [q for q in all_query_names if keyword.lower() in q.lower()] if keyword else all_query_names

    if not filtered_names:
        st.warning("No queries match that keyword.")
        st.stop()

    query_option = st.selectbox("📋 Select a Query", filtered_names)

    queries = {
        "Q1 - Providers & Receivers by City": "SELECT p.City, COUNT(DISTINCT p.Provider_ID) AS Total_Providers, COUNT(DISTINCT r.Receiver_ID) AS Total_Receivers FROM providers p LEFT JOIN receivers r ON p.City = r.City GROUP BY p.City ORDER BY Total_Providers DESC",
        "Q2 - Provider Type Contribution": "SELECT Type, COUNT(*) AS Total_Providers FROM providers GROUP BY Type ORDER BY Total_Providers DESC",
        "Q4 - Top Receivers by Claims": "SELECT r.Name, r.Type, COUNT(c.Claim_ID) AS Total_Claims FROM receivers r JOIN claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Receiver_ID, r.Name, r.Type ORDER BY Total_Claims DESC LIMIT 10",
        "Q5 - Total Food Available": "SELECT SUM(Quantity) AS Total_Food_Available FROM food_listings",
        "Q6 - City with Most Listings": "SELECT Location, COUNT(*) AS Total_Listings FROM food_listings GROUP BY Location ORDER BY Total_Listings DESC LIMIT 10",
        "Q7 - Most Common Food Types": "SELECT Food_Type, COUNT(*) AS Total_Listings FROM food_listings GROUP BY Food_Type ORDER BY Total_Listings DESC",
        "Q8 - Claims per Food Item": "SELECT f.Food_Name, COUNT(c.Claim_ID) AS Total_Claims FROM food_listings f LEFT JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Food_ID, f.Food_Name ORDER BY Total_Claims DESC LIMIT 10",
        "Q9 - Provider with Most Successful Claims": "SELECT p.Name, p.Type, COUNT(c.Claim_ID) AS Successful_Claims FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID JOIN claims c ON f.Food_ID = c.Food_ID WHERE c.Status = 'Completed' GROUP BY p.Provider_ID, p.Name, p.Type ORDER BY Successful_Claims DESC LIMIT 5",
        "Q10 - Claim Status Breakdown": "SELECT Status, COUNT(*) AS Total, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims), 2) AS Percentage FROM claims GROUP BY Status",
        "Q11 - Avg Quantity per Receiver": "SELECT ROUND(AVG(f.Quantity), 2) AS Avg_Quantity_Per_Receiver FROM claims c JOIN food_listings f ON c.Food_ID = f.Food_ID",
        "Q12 - Most Claimed Meal Type": "SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims FROM food_listings f JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Meal_Type ORDER BY Total_Claims DESC",
        "Q13 - Total Donated by Provider": "SELECT p.Name, p.Type, SUM(f.Quantity) AS Total_Donated FROM providers p JOIN food_listings f ON p.Provider_ID = f.Provider_ID GROUP BY p.Provider_ID, p.Name, p.Type ORDER BY Total_Donated DESC LIMIT 10",
        "Q14 - Earliest Expiring Items": "SELECT Food_Name, Quantity, Expiry_Date, Location FROM food_listings ORDER BY Expiry_Date ASC LIMIT 10",
        "Q15 - Top 5 Cities by Quantity": "SELECT Location, SUM(Quantity) AS Total_Quantity FROM food_listings GROUP BY Location ORDER BY Total_Quantity DESC LIMIT 5"
    }

    if query_option == "Q3 - Provider Contact Info by City":
        city = st.text_input("🏙️ Enter City Name", "New Carol")
        df = pd.read_sql(f"SELECT Name, Type, Address, Contact FROM providers WHERE City = '{city}'", engine)
    else:
        df = pd.read_sql(queries[query_option], engine)

    st.markdown(f"<p style='color:#c5c9d4; font-size:14px;'>📌 {len(df)} records found</p>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Export Result as CSV", csv, f"{query_option[:3]}_result.csv", "text/csv")

    # Mini chart preview if data has a numeric column to visualize
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    text_cols = df.select_dtypes(exclude='number').columns.tolist()
    if numeric_cols and text_cols and len(df) > 1 and len(df) <= 20:
        st.markdown("<p style='color:#c5c9d4; font-size:13px; margin-top:10px;'>📊 Quick Preview</p>", unsafe_allow_html=True)
        fig = px.bar(df, x=text_cols[0], y=numeric_cols[0], template="plotly_dark",
                     color_discrete_sequence=["#818cf8"])
        fig.update_layout(height=300, margin=dict(l=10,r=10,t=10,b=10), plot_bgcolor="#2e3344", paper_bgcolor="#2e3344")
        st.plotly_chart(fig, use_container_width=True)
elif page == "🔍 Filters":
    st.markdown("<h1 style='color:#e4e6eb;'>🔍 Filter Food Listings</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2e3148;'>", unsafe_allow_html=True)

    search_term = st.text_input("⚡ Live Search (type a food name, city, or provider...)", placeholder="e.g. Rice, New Carol...")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cities = ["All"] + list(pd.read_sql("SELECT DISTINCT Location FROM food_listings ORDER BY Location", engine)['Location'])
        city = st.selectbox("🏙️ City", cities)
    with col2:
        food_type = st.selectbox("🥗 Food Type", ["All", "Vegetarian", "Vegan", "Non-Vegetarian"])
    with col3:
        meal_type = st.selectbox("🍽️ Meal Type", ["All", "Breakfast", "Lunch", "Dinner", "Snacks"])
    with col4:
        sort_by = st.selectbox("↕️ Sort By", ["Food_Name", "Quantity", "Expiry_Date", "Location"])

    query = """SELECT f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date, f.Food_Type,
               f.Meal_Type, f.Location, p.Name AS Provider_Name, p.Contact
               FROM food_listings f
               JOIN providers p ON f.Provider_ID = p.Provider_ID WHERE 1=1"""

    if city != "All":
        query += f" AND f.Location = '{city}'"
    if food_type != "All":
        query += f" AND f.Food_Type = '{food_type}'"
    if meal_type != "All":
        query += f" AND f.Meal_Type = '{meal_type}'"

    df = pd.read_sql(query, engine)

    if search_term:
        mask = (df['Food_Name'].str.contains(search_term, case=False, na=False) |
                df['Location'].str.contains(search_term, case=False, na=False) |
                df['Provider_Name'].str.contains(search_term, case=False, na=False))
        df = df[mask]

    df = df.sort_values(by=sort_by)

    st.markdown(f"<p style='color:#c5c9d4; font-size:14px;'>📌 {len(df)} records found</p>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Export as CSV", csv, "filtered_food_listings.csv", "text/csv")

# ============ CRUD ============
elif page == "➕ CRUD Operations":
    st.markdown("<h1 style='color:#e4e6eb;'>➕ CRUD Operations</h1>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2e3148;'>", unsafe_allow_html=True)

    operation = st.selectbox("⚙️ Select Operation", [
        "➕ Add Food Listing",
        "✏️ Update Claim Status",
        "🗑️ Delete Food Listing"
    ])

    if operation == "➕ Add Food Listing":
        st.subheader("Add New Food Listing")
        col1, col2 = st.columns(2)
        with col1:
            food_id = st.number_input("Food ID", min_value=1001, step=1)
            food_name = st.text_input("Food Name")
            quantity = st.number_input("Quantity", min_value=1)
            expiry_date = st.date_input("Expiry Date")
        with col2:
            provider_id = st.number_input("Provider ID", min_value=1)
            food_type = st.selectbox("Food Type", ["Vegetarian", "Vegan", "Non-Vegetarian"])
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
            location = st.text_input("Location")

        st.markdown("<p class='section-title'>👁️ Live Preview</p>", unsafe_allow_html=True)
        preview_name = food_name if food_name else "—"
        preview_location = location if location else "—"
        st.markdown(f"""
            <div class='insight-card' style='text-align:left; border-top:2px solid #818cf8;'>
                <p style='margin:4px 0;'><b style='color:#e4e6eb;'>Food ID:</b> {food_id}</p>
                <p style='margin:4px 0;'><b style='color:#e4e6eb;'>Name:</b> {preview_name}</p>
                <p style='margin:4px 0;'><b style='color:#e4e6eb;'>Quantity:</b> {quantity}</p>
                <p style='margin:4px 0;'><b style='color:#e4e6eb;'>Expiry:</b> {expiry_date}</p>
                <p style='margin:4px 0;'><b style='color:#e4e6eb;'>Type:</b> {food_type} • <b>Meal:</b> {meal_type}</p>
                <p style='margin:4px 0;'><b style='color:#e4e6eb;'>Location:</b> {preview_location}</p>
            </div>
        """, unsafe_allow_html=True)

        if st.button("➕ Add Food Listing"):
            try:
                with engine.connect() as conn:
                    conn.execute(text(f"""INSERT INTO food_listings VALUES ({food_id}, '{food_name}', {quantity}, '{expiry_date}', {provider_id}, '{food_type}', '{location}', '{food_type}', '{meal_type}')"""))
                    conn.commit()
                st.success("✅ Food Listing Added Successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    elif operation == "✏️ Update Claim Status":
        st.subheader("Update Claim Status")
        claim_id = st.number_input("Claim ID", min_value=1)
        new_status = st.selectbox("New Status", ["Pending", "Completed", "Cancelled"])
        if st.button("✏️ Update Status"):
            try:
                with engine.connect() as conn:
                    conn.execute(text(f"UPDATE claims SET Status = '{new_status}' WHERE Claim_ID = {claim_id}"))
                    conn.commit()
                st.success("✅ Claim Status Updated Successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    elif operation == "🗑️ Delete Food Listing":
        st.subheader("Delete Food Listing")
        food_id = st.number_input("Food ID to Delete", min_value=1)

        existing = pd.read_sql(f"SELECT * FROM food_listings WHERE Food_ID = {food_id}", engine)
        if not existing.empty:
            st.markdown("<p style='color:#c5c9d4;'>You're about to delete:</p>", unsafe_allow_html=True)
            st.dataframe(existing, use_container_width=True)
        else:
            st.info("No food listing found with that ID.")

        confirm = st.checkbox("⚠️ I confirm I want to permanently delete this listing")

        if st.button("🗑️ Delete", disabled=not confirm):
            try:
                with engine.connect() as conn:
                    conn.execute(text(f"DELETE FROM food_listings WHERE Food_ID = {food_id}"))
                    conn.commit()
                st.success("✅ Food Listing Deleted Successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ============ EDA ============
elif page == "📈 EDA Charts":
    st.markdown("<h1 style='color:#e4e6eb;'>📈 EDA - Data Visualizations</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#c5c9d4; font-size:13px;'>Hover over any chart for details. Use the toggle to switch chart type.</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#2e3148;'>", unsafe_allow_html=True)

    plotly_colors = ['#818cf8', '#34d399', '#fbbf24', '#f87171', '#60a5fa']

    def render_chart(df, names_col, values_col, title, key):
        chart_type = st.radio(f"Chart type — {title}", ["Bar", "Pie"], horizontal=True, key=key)
        if chart_type == "Bar":
            fig = px.bar(df, x=names_col, y=values_col, template="plotly_dark",
                         color=names_col, color_discrete_sequence=plotly_colors, text=values_col)
            fig.update_traces(textposition="outside")
        else:
            fig = px.pie(df, names=names_col, values=values_col, template="plotly_dark",
                         color_discrete_sequence=plotly_colors, hole=0.35)
            fig.update_traces(textinfo="label+percent")
        fig.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="#2e3344", paper_bgcolor="#2e3344",
            font_color="#e4e6eb", showlegend=(chart_type == "Pie")
        )
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏪 Provider Type Contribution")
        q2 = pd.read_sql("SELECT Type, COUNT(*) AS Total FROM providers GROUP BY Type ORDER BY Total DESC", engine)
        render_chart(q2, "Type", "Total", "Provider Type", "chart_provider")

    with col2:
        st.subheader("📋 Claim Status Breakdown")
        q10 = pd.read_sql("SELECT Status, COUNT(*) AS Total FROM claims GROUP BY Status", engine)
        render_chart(q10, "Status", "Total", "Claim Status", "chart_claims")

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🍽️ Most Claimed Meal Types")
        q12 = pd.read_sql("SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total FROM food_listings f JOIN claims c ON f.Food_ID = c.Food_ID GROUP BY f.Meal_Type ORDER BY Total DESC", engine)
        render_chart(q12, "Meal_Type", "Total", "Meal Type", "chart_meal")

    with col4:
        st.subheader("🥗 Food Type Distribution")
        q7 = pd.read_sql("SELECT Food_Type, COUNT(*) AS Total FROM food_listings GROUP BY Food_Type", engine)
        render_chart(q7, "Food_Type", "Total", "Food Type", "chart_food")

    st.markdown("---")
    st.subheader("🏙️ Top 10 Cities by Food Listings")
    q6 = pd.read_sql("SELECT Location, COUNT(*) AS Total FROM food_listings GROUP BY Location ORDER BY Total DESC LIMIT 10", engine)
    fig = px.bar(q6, x="Total", y="Location", orientation="h", template="plotly_dark",
                 color_discrete_sequence=["#818cf8"], text="Total")
    fig.update_traces(textposition="outside")
    fig.update_layout(
        height=420, margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="#2e3344", paper_bgcolor="#2e3344", font_color="#e4e6eb",
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📅 Expiry Date Range")
    date_range = pd.read_sql("SELECT MIN(Expiry_Date) as min_d, MAX(Expiry_Date) as max_d FROM food_listings", engine)
    min_d, max_d = date_range.iloc[0,0], date_range.iloc[0,1]
    selected_range = st.slider("Filter listings by expiry date", min_value=min_d, max_value=max_d, value=(min_d, max_d))
    range_df = pd.read_sql(f"SELECT Food_Name, COUNT(*) as Total FROM food_listings WHERE Expiry_Date BETWEEN '{selected_range[0]}' AND '{selected_range[1]}' GROUP BY Food_Name ORDER BY Total DESC", engine)
    st.markdown(f"<p style='color:#c5c9d4; font-size:13px;'>{range_df['Total'].sum()} listings expiring in this range</p>", unsafe_allow_html=True)
    fig2 = px.bar(range_df, x="Food_Name", y="Total", template="plotly_dark", color_discrete_sequence=["#34d399"])
    fig2.update_layout(height=350, margin=dict(l=10,r=10,t=10,b=10), plot_bgcolor="#2e3344", paper_bgcolor="#2e3344", font_color="#e4e6eb")
    st.plotly_chart(fig2, use_container_width=True)