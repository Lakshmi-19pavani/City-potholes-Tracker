import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt


st.set_page_config(page_title="City Pothole Tracker", layout="wide")

# ---------- GLOBAL STYLING ----------
st.markdown("""
<style>
.main {background: linear-gradient(120deg, #f0f2f6, #e6f0ff);}
h1, h2, h3 {font-family: 'Segoe UI', sans-serif;}
.section-card {
    background: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛣️ City Potholes Tracker")
st.caption("Report and track road maintenance")

# ------------------ DATA ------------------
data = pd.DataFrame({
    "location": [
        "Charminar","Hitech City","Kukatpally","Secunderabad","Banjara Hills",
        "Gachibowli","Madhapur","Ameerpet","LB Nagar","Begumpet",
        "Kukatpally","Kukatpally","Ameerpet","LB Nagar","Hitech City"
    ],
    "lat": [
        17.3616,17.4435,17.4948,17.4399,17.4126,
        17.4401,17.4483,17.4375,17.3457,17.4448,
        17.4948,17.4948,17.4375,17.3457,17.4435
    ],
    "lon": [
        78.4747,78.3772,78.3996,78.4983,78.4482,
        78.3489,78.3915,78.4483,78.5510,78.4623,
        78.3996,78.3996,78.4483,78.5510,78.3772
    ],
    "status": [
        "Needs Repair","Under Repair","Needs Repair","Fixed","Fixed",
        "Under Repair","Needs Repair","Fixed","Needs Repair","Under Repair",
        "Needs Repair","Under Repair","Needs Repair","Fixed","Needs Repair"
    ]
})


def get_color(status):
    if status == "Needs Repair":
        return [255, 75, 75]
    elif status == "Under Repair":
        return [255, 165, 0]
    else:
        return [0, 200, 120]

data["color"] = data["status"].apply(get_color)

# ------------------ SIDEBAR FILTER ------------------
st.sidebar.markdown("""
<h3 style="background:linear-gradient(90deg,#ff4b4b,#ffa500);padding:8px;border-radius:8px;color:white;text-align:center;">
Filters
</h3>
""", unsafe_allow_html=True)

status_filter = st.sidebar.selectbox("Status", ["All","Needs Repair","Under Repair","Fixed"])
filtered_data = data if status_filter=="All" else data[data.status==status_filter]

st.sidebar.subheader("Recent Reports")
for _, row in filtered_data.iterrows():
    st.sidebar.write(f"📍 {row['location']} — {row['status']}")

# ------------------ TOP STATS ------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Reports", len(filtered_data))
col2.metric("Needs Repair", len(filtered_data[filtered_data.status=="Needs Repair"]))
col3.metric("Under Repair", len(filtered_data[filtered_data.status=="Under Repair"]))
col4.metric("Fixed", len(filtered_data[filtered_data.status=="Fixed"]))

st.divider()

# ------------------ STATUS CARDS ------------------
st.markdown("""
<style>
.card-container {display:flex; gap:20px; margin-top:10px;}
.card {
    flex:1; padding:20px; border-radius:15px; color:white; font-weight:bold; text-align:center;
    box-shadow: 0 0 15px rgba(255,255,255,0.3); transition: 0.3s;
}
.card:hover {transform: translateY(-6px); box-shadow:0 0 25px rgba(255,255,255,0.6);}
.red {background: linear-gradient(135deg,#ff4b4b,#b30000);}
.orange {background: linear-gradient(135deg,#ffa500,#cc8400);}
.green {background: linear-gradient(135deg,#28a745,#0f6d2f);}
</style>
""", unsafe_allow_html=True)

needs = len(filtered_data[filtered_data.status=="Needs Repair"])
under = len(filtered_data[filtered_data.status=="Under Repair"])
fixed = len(filtered_data[filtered_data.status=="Fixed"])

st.markdown(f"""
<div class="card-container">
  <div class="card red"><h2>{needs}</h2><p>Needs Repair</p></div>
  <div class="card orange"><h2>{under}</h2><p>Under Repair</p></div>
  <div class="card green"><h2>{fixed}</h2><p>Fixed</p></div>
</div>
""", unsafe_allow_html=True)

# ------------------ HEADING FUNCTION ------------------
def styled_heading(text, c1, c2):
    st.markdown(f"""
    <h2 style="background: linear-gradient(90deg,{c1},{c2});
    padding:10px 15px;border-radius:10px;color:white;
    text-shadow:1px 1px 4px rgba(0,0,0,0.4);">{text}</h2>
    """, unsafe_allow_html=True)

# ------------------ MAP ------------------
styled_heading("📍 Pothole Locations", "#ff6f61", "#ffb88c")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_data,
    get_position='[lon, lat]',
    get_color="color",
    get_radius=400,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=17.3850, longitude=78.4867, zoom=11)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# ------------------ ENHANCED TABLE ------------------
styled_heading("📋 All Reports", "#007bff", "#00c6ff")

st.markdown("""
<style>
.table-card {background:white;padding:20px;border-radius:15px;
box-shadow:0 4px 15px rgba(0,0,0,0.08);overflow-x:auto;}
table {width:100%;border-collapse:collapse;font-family:'Segoe UI',sans-serif;}
th {text-align:left;padding:12px;background:#f1f5f9;}
td {padding:12px;border-bottom:1px solid #eee;}
tr:nth-child(even){background:#fafafa;}
tr:hover{background:#f1f7ff;}
.badge {padding:6px 12px;border-radius:20px;color:white;font-weight:bold;font-size:13px;}
.red{background:#ff4b4b;} .orange{background:#ffa500;} .green{background:#28a745;}
</style>
""", unsafe_allow_html=True)

table_html = "<div class='table-card'><table>"
table_html += "<tr><th>📍 Location</th><th>🚧 Status</th></tr>"

for _, row in filtered_data.iterrows():   # ✅ FIXED HERE
    badge_class = "badge red" if row["status"]=="Needs Repair" else \
                  "badge orange" if row["status"]=="Under Repair" else "badge green"
    table_html += f"<tr><td>{row['location']}</td><td><span class='{badge_class}'>{row['status']}</span></td></tr>"

table_html += "</table></div>"
st.markdown(table_html, unsafe_allow_html=True)

# ------------------ CHART ------------------
styled_heading("📊 Repair Status Overview", "#28a745", "#a8e063")

status_counts = filtered_data["status"].value_counts()

chart_df = pd.DataFrame({
    "Status": status_counts.index,
    "Count": status_counts.values
})

color_map = {
    "Needs Repair": "#ff4b4b",
    "Under Repair": "#ffa500",
    "Fixed": "#28a745"
}

chart_df["Color"] = chart_df["Status"].map(color_map)

st.markdown("### ")

st.altair_chart(
    alt.Chart(chart_df).mark_arc(innerRadius=70).encode(
        theta="Count",
        color=alt.Color("Status", scale=alt.Scale(range=chart_df["Color"].tolist())),
        tooltip=["Status", "Count"]
    ),
    use_container_width=True
)
# ------------------ AREA WISE REPORT COUNT ------------------
st.subheader("📍 Reports by Area")

area_counts = (
    filtered_data.groupby("location")
    .size()
    .reset_index(name="Reports")
    .sort_values(by="Reports", ascending=False)
)

bar_chart = alt.Chart(area_counts).mark_bar().encode(
    x=alt.X("Reports:Q", title="Number of Reports"),
    y=alt.Y("location:N", sort="-x", title="Area"),
    tooltip=["location", "Reports"],
    color=alt.value("#4e79a7")
).properties(height=400)

st.altair_chart(bar_chart, use_container_width=True)


