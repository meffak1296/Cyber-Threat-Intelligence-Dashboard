import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Cyber Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# CSS
st.markdown("""
<style>

.stApp{
    background:#0B1120;
}


.title{
    text-align:center;
    color:#22C55E;
    font-size:50px;
    font-weight:900;
}


.subtitle{
    text-align:center;
    color:#CBD5E1;
    font-size:22px;
    margin-bottom:30px;
}


.card{
    background:#111827;
    padding:25px;
    border-radius:15px;
    border:2px solid #22C55E;
    text-align:center;
    transition:0.4s;
}

.card:hover{
    transform:translateY(-8px);
    box-shadow:0 0 25px #22C55E;
}



.card h3{
    color:#22C55E;
}


.card p{
    color:white;
    font-size:35px;
    font-weight:bold;
}


/* Dataframe Dark Theme */

[data-testid="stDataFrame"]{
    background:#000000;
    border-radius:15px;
}


[data-testid="stDataFrame"] div{
    color:white !important;
}


</style>
""", unsafe_allow_html=True)



# Header

st.markdown("""
<div class="title">
🛡️ CYBER THREAT INTELLIGENCE DASHBOARD
</div>

<div class="subtitle">
Enterprise Security Operations Center (SOC)
</div>
""", unsafe_allow_html=True)



# Load Dataset

@st.cache_data
def load_data():

    df = pd.read_csv(
        "cicids2017_sample.csv",
        skiprows=lambda x: x > 0 and x % 20 != 0,
        low_memory=True
    )

    return df


df = load_data()



# ==========================================================
# Sidebar Filter
# ==========================================================

st.sidebar.title("🎛️ Dashboard Filters")

selected_attack = st.sidebar.selectbox(
    "Select Attack Type",
    ["All"] + sorted(df["Attack Type"].unique().tolist())
)
rows_to_show = st.sidebar.slider(
    "📄 Rows to Display",
    min_value=5,
    max_value=100,
    value=10,
    step=5
)


if selected_attack == "All":
    filtered_df = df
else:
    filtered_df = df[df["Attack Type"] == selected_attack]

# KPI Values

total_records = len(filtered_df)

attack_types = filtered_df["Attack Type"].nunique()

normal_traffic = (filtered_df["Attack Type"].str.upper()=="BENIGN").sum()





# ==========================================================
# Dynamic Threat Level
# ==========================================================

if total_records > 100000:
    threat_level = "HIGH"
    threat_color = "#EF4444"   # Red

elif total_records > 30000:
    threat_level = "MEDIUM"
    threat_color = "#FACC15"   # Yellow

else:
    threat_level = "LOW"
    threat_color = "#22C55E"   # Green

# ==========================================================
# Quick Statistics (Sidebar)
# ==========================================================

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Quick Statistics")

st.sidebar.write(f"📁 Records: {total_records:,}")
st.sidebar.write(f"🚨 Attack Types: {attack_types}")
st.sidebar.write(f"⚠️ Threat Level: {threat_level}")



# KPI Cards

col1,col2,col3,col4 = st.columns(4)


with col1:
    st.markdown(f"""
    <div class="card">
    <h3>📁 Total Records</h3>
    <p>{total_records:,}</p>
    </div>
    """, unsafe_allow_html=True)


with col2:
    st.markdown(f"""
    <div class="card">
    <h3>🚨 Attack Types</h3>
    <p>{attack_types}</p>
    </div>
    """, unsafe_allow_html=True)


with col3:
    st.markdown(f"""
    <div class="card">
    <h3>🛡️ Normal Traffic</h3>
    <p>{normal_traffic:,}</p>
    </div>
    """, unsafe_allow_html=True)


with col4:
    st.markdown(f"""
    <div class="card">
    <h3>⚠️ Threat Level</h3>
    <p style="color:{threat_color};">{threat_level}</p>
    </div>
    """, unsafe_allow_html=True)   


# Dataset Preview

st.markdown("""
<div class="card">
<h3>📋 Dataset Preview</h3>
</div>
""", unsafe_allow_html=True)


st.dataframe(
    filtered_df.head(rows_to_show),
    use_container_width=True,
    height=350
)



# Attack Data


attack_data = filtered_df["Attack Type"].value_counts().reset_index()
attack_data.columns = [
    "Attack Type",
    "Count"
]



# Attack Type Analysis

st.markdown("""
<div class="card">
<h3>🚨 Attack Type Analysis</h3>
</div>
""", unsafe_allow_html=True)


st.dataframe(
    attack_data,
    use_container_width=True,
    height=300,
    hide_index=True
)













# ==========================================================
# Attack Distribution Analysis (Bar Chart)
# ==========================================================

st.markdown("""
<div class="card">
<h3>📊 Attack Distribution Analysis</h3>
</div>
""", unsafe_allow_html=True)

fig_bar = px.bar(
    attack_data,
    x="Attack Type",
    y="Count",
    text="Count",
    color="Count",
    color_continuous_scale="Greens",
    template="plotly_dark"
)

fig_bar.update_traces(
    textposition="outside"
)

fig_bar.update_layout(
    paper_bgcolor="#0B1120",
    plot_bgcolor="#000000",
    font=dict(color="white", size=14),
    xaxis_title="Attack Type",
    yaxis_title="Number of Attacks",
    coloraxis_showscale=False
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)






# ==========================================================
# Pie Chart
# ==========================================================

st.markdown("""
<div class="card">
<h3>🥧 Attack Distribution Pie Chart</h3>
</div>
""", unsafe_allow_html=True)

fig_pie = px.pie(
    attack_data,
    names="Attack Type",
    values="Count",
    template="plotly_dark",
    hole=0.45,
    color_discrete_sequence=px.colors.sequential.Greens
)

fig_pie.update_layout(
    paper_bgcolor="#0B1120",
    plot_bgcolor="#000000",
    font=dict(color="white"),
    title="Attack Distribution (%)",
    title_x=0.5
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)


# ==========================================================
# Threat Summary
# ==========================================================



most_attack = attack_data.iloc[0]["Attack Type"]
most_count = attack_data.iloc[0]["Count"]

st.markdown(f"""
<div style="
background:#111827;
padding:25px;
border-radius:15px;
border:2px solid #22C55E;
margin-top:20px;
box-shadow:0 0 15px rgba(34,197,94,0.25);
">

<h2 style="
color:#22C55E;
text-align:center;">
🚨 Threat Summary
</h2>

<hr style="border:1px solid #22C55E;">

<p style="color:white;font-size:18px;">
🚨 <b>Most Frequent Attack:</b> {most_attack}
</p>

<p style="color:white;font-size:18px;">
📊 <b>Attack Count:</b> {most_count:,}
</p>

<p style="color:white;font-size:18px;">
🛡️ <b>Total Attack Categories:</b> {attack_types}
</p>

<p style="color:white;font-size:18px;">
📁 <b>Total Records:</b> {total_records:,}
</p>

<p style="color:{threat_color};font-size:20px;font-weight:bold;">
⚠️ Current Threat Level : {threat_level}
</p>

</div>
""", unsafe_allow_html=True)



# ==========================================================
# Top 5 Most Frequent Attacks
# ==========================================================

st.markdown("""
<div class="card">
<h3>🏆 Top 5 Most Frequent Attacks</h3>
</div>
""", unsafe_allow_html=True)

top5 = attack_data.head(5)

fig_top5 = px.bar(
    top5,
    x="Count",
    y="Attack Type",
    orientation="h",
    text="Count",
    color="Count",
    color_continuous_scale="Greens",
    template="plotly_dark"
)

fig_top5.update_traces(
    textposition="outside"
)

fig_top5.update_layout(
    paper_bgcolor="#0B1120",
    plot_bgcolor="#000000",
    font=dict(color="white", size=14),
    xaxis_title="Number of Attacks",
    yaxis_title="Attack Type",
    coloraxis_showscale=False,
    yaxis=dict(autorange="reversed")
)

st.plotly_chart(
    fig_top5,
    use_container_width=True
)




# ==========================================================
# Attack Statistics
# ==========================================================

st.markdown("""
<div class="card">
<h3>📊 Attack Statistics</h3>
</div>
""", unsafe_allow_html=True)

highest_attack = attack_data.loc[attack_data["Count"].idxmax()]
lowest_attack = attack_data.loc[attack_data["Count"].idxmin()]
average_attack = int(attack_data["Count"].mean())
total_attacks = int(attack_data["Count"].sum())

col1, col2 = st.columns(2)

col1, col2 = st.columns(2)


with col1:
    st.markdown(f"""
    <div class="card">

    <h3>✅ Total Attacks</h3>
    <p>{total_attacks:,}</p>

    <hr style="border:1px solid #22C55E;">

    <h3>🚨 Highest Attack</h3>
    <p>{highest_attack['Attack Type']}</p>
    <p>{highest_attack['Count']:,}</p>

    </div>
    """, unsafe_allow_html=True)



with col2:
    st.markdown(f"""
    <div class="card">

    <h3>📉 Lowest Attack</h3>
    <p>{lowest_attack['Attack Type']}</p>
    <p>{lowest_attack['Count']:,}</p>

    <hr style="border:1px solid #22C55E;">

    <h3>📊 Average Attacks</h3>
    <p>{average_attack:,}</p>

    </div>
    """, unsafe_allow_html=True)

    # ==========================================================
# Footer
# ==========================================================

st.markdown("""
<br>
<div style="
background:#111827;
padding:20px;
border-radius:15px;
border:2px solid #22C55E;
text-align:center;
margin-top:40px;
">

<h3 style="color:#22C55E;">
🛡️ Cyber Threat Intelligence Dashboard
</h3>

<p style="color:white;font-size:16px;">
Developed by: Maham Farooq
</p>

<p style="color:#CBD5E1;">
AI & Data Science | SOC Analytics
</p>

<p style="color:#94A3B8;">
© 2026 | Enterprise Security Operations Center
</p>

</div>
""", unsafe_allow_html=True)


# ==========================================================
# Download Filtered Dataset
# ==========================================================

st.sidebar.markdown("---")

st.sidebar.download_button(
    label="⬇️ Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_attack_data.csv",
    mime="text/csv"
)
