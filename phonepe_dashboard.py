# ============================================================
# PhonePe Transaction Insights - Complete Streamlit Dashboard
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="PhonePe Transaction Insights",
    page_icon="📱",
    layout="wide"
)

# ============================================================
# Custom CSS for better styling
# ============================================================
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #5f259f; color: white; padding: 10px; border-radius: 10px; }
    h1 { color: #5f259f; }
    h2 { color: #5f259f; }
    h3 { color: #5f259f; }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# Connect to MySQL Database
# ============================================================
@st.cache_resource
def get_connection():
    password = quote_plus('bbd@321university')
    engine = create_engine(f'mysql+pymysql://root:{password}@localhost/phonepe')
    return engine

engine = get_connection()

# ============================================================
# Load Data from MySQL
# ============================================================
@st.cache_data
def load_data():
    agg_trans = pd.read_sql("SELECT * FROM aggregated_transaction", engine)
    agg_user = pd.read_sql("SELECT * FROM aggregated_user", engine)
    agg_insurance = pd.read_sql("SELECT * FROM aggregated_insurance", engine)
    map_trans = pd.read_sql("SELECT * FROM map_transaction", engine)
    map_user = pd.read_sql("SELECT * FROM map_user", engine)
    map_insurance = pd.read_sql("SELECT * FROM map_insurance", engine)
    top_trans = pd.read_sql("SELECT * FROM top_transaction", engine)
    top_user = pd.read_sql("SELECT * FROM top_user", engine)
    return agg_trans, agg_user, agg_insurance, map_trans, map_user, map_insurance, top_trans, top_user

agg_trans, agg_user, agg_insurance, map_trans, map_user, map_insurance, top_trans, top_user = load_data()

# ============================================================
# Dashboard Header
# ============================================================
st.markdown("""
    <h1 style='text-align: center; color: #5f259f;'>
    📱 PhonePe Transaction Insights Dashboard
    </h1>
    <p style='text-align: center; color: gray;'>
    Interactive analysis of PhonePe transactions across India (2018-2024)
    </p>
""", unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# Sidebar Navigation
# ============================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/PhonePe_Logo.png/800px-PhonePe_Logo.png", 
                 width=200)
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "💳 Transaction Analysis",
    "👥 User Analysis", 
    "🛡️ Insurance Analysis",
    "🗺️ District Analysis"
])

st.sidebar.markdown("---")
st.sidebar.title("🔍 Filters")

# Year filter
years = sorted(agg_trans['year'].unique())
selected_year = st.sidebar.selectbox("Select Year", ["All"] + list(years))

# Quarter filter
quarters = {1: "Q1 (Jan-Mar)", 2: "Q2 (Apr-Jun)",
            3: "Q3 (Jul-Sep)", 4: "Q4 (Oct-Dec)"}
selected_quarter = st.sidebar.selectbox("Select Quarter",
                                        ["All"] + list(quarters.values()))

# State filter
states = sorted(agg_trans['state'].unique())
selected_state = st.sidebar.selectbox("Select State", ["All"] + list(states))

# ============================================================
# Filter Data
# ============================================================
filtered_trans = agg_trans.copy()
filtered_user = agg_user.copy()
filtered_insurance = agg_insurance.copy()

if selected_year != "All":
    filtered_trans = filtered_trans[filtered_trans['year'] == selected_year]
    filtered_user = filtered_user[filtered_user['year'] == selected_year]
    filtered_insurance = filtered_insurance[filtered_insurance['year'] == selected_year]

if selected_quarter != "All":
    quarter_num = [k for k, v in quarters.items() if v == selected_quarter][0]
    filtered_trans = filtered_trans[filtered_trans['quarter'] == quarter_num]
    filtered_user = filtered_user[filtered_user['quarter'] == quarter_num]
    filtered_insurance = filtered_insurance[filtered_insurance['quarter'] == quarter_num]

if selected_state != "All":
    filtered_trans = filtered_trans[filtered_trans['state'] == selected_state]
    filtered_user = filtered_user[filtered_user['state'] == selected_state]
    filtered_insurance = filtered_insurance[filtered_insurance['state'] == selected_state]

# ============================================================
# HOME PAGE
# ============================================================
if page == "🏠 Home":
    # Key Metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💳 Total Transactions",
                  f"{filtered_trans['count'].sum()/1e7:.1f} Cr")
    with col2:
        st.metric("💰 Total Amount",
                  f"₹{filtered_trans['amount'].sum()/1e12:.1f} Lakh Cr")
    with col3:
        st.metric("👥 Registered Users",
                  f"{filtered_user['registered_users'].sum()/1e7:.1f} Cr")
    with col4:
        st.metric("📱 App Opens",
                  f"{filtered_user['app_opens'].sum()/1e9:.1f} B")

    st.markdown("---")

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Year wise Transaction Growth")
        year_data = agg_trans.groupby('year')['count'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=year_data, x='year', y='count',
                    marker='o', linewidth=2.5, color='purple', ax=ax)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e7:.0f} Cr'))
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Transactions")
        st.pyplot(fig)

    with col2:
        st.subheader("💰 Year wise Transaction Amount")
        year_amount = agg_trans.groupby('year')['amount'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=year_amount, x='year', y='amount',
                   palette='Blues_d', ax=ax)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e12:.0f} L.Cr'))
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Amount")
        st.pyplot(fig)

    st.markdown("---")

    # Row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🥧 Transaction Type Distribution")
        type_data = filtered_trans.groupby('transaction_type')['count'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.pie(type_data['count'],
               labels=type_data['transaction_type'],
               autopct='%1.1f%%',
               colors=['skyblue', 'lightgreen', 'salmon', 'gold', 'purple'])
        st.pyplot(fig)

    with col2:
        st.subheader("🏆 Top 10 States by Transactions")
        state_data = filtered_trans.groupby('state')['count'].sum().reset_index()
        state_data = state_data.sort_values('count', ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=state_data, x='count', y='state',
                   palette='viridis', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e7:.0f} Cr'))
        ax.set_xlabel("Total Transactions")
        ax.set_ylabel("State")
        st.pyplot(fig)

# ============================================================
# TRANSACTION ANALYSIS PAGE
# ============================================================
elif page == "💳 Transaction Analysis":
    st.subheader("💳 Transaction Analysis")
    st.markdown("---")

    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Transactions", f"{filtered_trans['count'].sum()/1e7:.1f} Cr")
    with col2:
        st.metric("Total Amount", f"₹{filtered_trans['amount'].sum()/1e12:.1f} Lakh Cr")
    with col3:
        st.metric("Avg Transaction Amount",
                  f"₹{filtered_trans['amount'].mean()/1e5:.1f} Lakh")

    st.markdown("---")

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Transaction Type vs Count")
        type_count = filtered_trans.groupby('transaction_type')['count'].sum().reset_index()
        type_count = type_count.sort_values('count', ascending=False)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=type_count, x='count', y='transaction_type',
                   palette='viridis', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e7:.0f} Cr'))
        ax.set_xlabel("Total Count")
        ax.set_ylabel("Transaction Type")
        st.pyplot(fig)

    with col2:
        st.subheader("Transaction Type vs Amount")
        type_amount = filtered_trans.groupby('transaction_type')['amount'].sum().reset_index()
        type_amount = type_amount.sort_values('amount', ascending=False)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=type_amount, x='amount', y='transaction_type',
                   palette='magma', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e12:.1f} L.Cr'))
        ax.set_xlabel("Total Amount")
        ax.set_ylabel("Transaction Type")
        st.pyplot(fig)

    st.markdown("---")

    # Row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 States by Transaction Count")
        state_count = filtered_trans.groupby('state')['count'].sum().reset_index()
        state_count = state_count.sort_values('count', ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=state_count, x='count', y='state',
                   palette='viridis', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e7:.0f} Cr'))
        ax.set_xlabel("Total Count")
        ax.set_ylabel("State")
        st.pyplot(fig)

    with col2:
        st.subheader("Top 10 States by Transaction Amount")
        state_amount = filtered_trans.groupby('state')['amount'].sum().reset_index()
        state_amount = state_amount.sort_values('amount', ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=state_amount, x='amount', y='state',
                   palette='magma', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e12:.1f} L.Cr'))
        ax.set_xlabel("Total Amount")
        ax.set_ylabel("State")
        st.pyplot(fig)

    st.markdown("---")

    # Quarter analysis
    st.subheader("Quarter wise Transaction Distribution")
    quarter_data = agg_trans.groupby('quarter')['count'].sum().reset_index()
    quarter_data['quarter'] = quarter_data['quarter'].map({
        1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'})
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=quarter_data, x='quarter', y='count',
               palette='coolwarm', ax=ax)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e7:.0f} Cr'))
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Transactions")
    st.pyplot(fig)

# ============================================================
# USER ANALYSIS PAGE
# ============================================================
elif page == "👥 User Analysis":
    st.subheader("👥 User Analysis")
    st.markdown("---")

    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Registered Users",
                  f"{filtered_user['registered_users'].sum()/1e7:.1f} Cr")
    with col2:
        st.metric("Total App Opens",
                  f"{filtered_user['app_opens'].sum()/1e9:.1f} B")
    with col3:
        engagement = filtered_user['app_opens'].sum() / filtered_user['registered_users'].sum()
        st.metric("Avg Engagement Ratio", f"{engagement:.1f}x")

    st.markdown("---")

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 States by Registered Users")
        state_users = filtered_user.groupby('state')['registered_users'].sum().reset_index()
        state_users = state_users.sort_values('registered_users', ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=state_users, x='registered_users', y='state',
                   palette='rocket', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e7:.0f} Cr'))
        ax.set_xlabel("Registered Users")
        ax.set_ylabel("State")
        st.pyplot(fig)

    with col2:
        st.subheader("Top 10 States by App Opens")
        state_opens = filtered_user.groupby('state')['app_opens'].sum().reset_index()
        state_opens = state_opens.sort_values('app_opens', ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=state_opens, x='app_opens', y='state',
                   palette='Blues_d', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.1f} B'))
        ax.set_xlabel("Total App Opens")
        ax.set_ylabel("State")
        st.pyplot(fig)

    st.markdown("---")

    # User growth
    st.subheader("Year wise User Growth")
    year_users = agg_user.groupby('year')['registered_users'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.lineplot(data=year_users, x='year', y='registered_users',
                marker='o', linewidth=2.5, color='green', ax=ax)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e7:.0f} Cr'))
    ax.set_xlabel("Year")
    ax.set_ylabel("Registered Users")
    st.pyplot(fig)

# ============================================================
# INSURANCE ANALYSIS PAGE
# ============================================================
elif page == "🛡️ Insurance Analysis":
    st.subheader("🛡️ Insurance Analysis")
    st.markdown("---")

    # Key metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Insurance Transactions",
                  f"{filtered_insurance['count'].sum():,.0f}")
    with col2:
        st.metric("Total Insurance Amount",
                  f"₹{filtered_insurance['amount'].sum()/1e7:.1f} Cr")

    st.markdown("---")

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Insurance Growth Over Years")
        ins_year = agg_insurance.groupby('year')['count'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.lineplot(data=ins_year, x='year', y='count',
                    marker='o', linewidth=2.5, color='blue', ax=ax)
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Insurance Transactions")
        st.pyplot(fig)

    with col2:
        st.subheader("Top 10 States by Insurance Amount")
        ins_state = filtered_insurance.groupby('state')['amount'].sum().reset_index()
        ins_state = ins_state.sort_values('amount', ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=ins_state, x='amount', y='state',
                   palette='viridis', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e7:.0f} Cr'))
        ax.set_xlabel("Total Amount")
        ax.set_ylabel("State")
        st.pyplot(fig)

    st.markdown("---")

    # Quarter wise insurance
    st.subheader("Quarter wise Insurance Distribution")
    ins_quarter = agg_insurance.groupby('quarter')['count'].sum().reset_index()
    ins_quarter['quarter'] = ins_quarter['quarter'].map({
        1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'})
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=ins_quarter, x='quarter', y='count',
               palette='magma', ax=ax)
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Insurance Transactions")
    st.pyplot(fig)

# ============================================================
# DISTRICT ANALYSIS PAGE
# ============================================================
elif page == "🗺️ District Analysis":
    st.subheader("🗺️ District Level Analysis")
    st.markdown("---")

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Districts by Transaction Amount")
        district_amount = map_trans.groupby(['district', 'state'])['amount'].sum().reset_index()
        district_amount = district_amount.sort_values('amount', ascending=False).head(10)
        district_amount['label'] = district_amount['district'] + ' (' + district_amount['state'] + ')'
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=district_amount, x='amount', y='label',
                   palette='viridis', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e12:.1f} L.Cr'))
        ax.set_xlabel("Total Amount")
        ax.set_ylabel("District (State)")
        st.pyplot(fig)

    with col2:
        st.subheader("Top 10 Districts by Registered Users")
        district_users = map_user.groupby(['district', 'state'])['registered_users'].sum().reset_index()
        district_users = district_users.sort_values('registered_users', ascending=False).head(10)
        district_users['label'] = district_users['district'] + ' (' + district_users['state'] + ')'
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=district_users, x='registered_users', y='label',
                   palette='magma', ax=ax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e7:.0f} Cr'))
        ax.set_xlabel("Registered Users")
        ax.set_ylabel("District (State)")
        st.pyplot(fig)

    st.markdown("---")

    # District insurance
    st.subheader("Top 10 Districts by Insurance Transactions")
    district_ins = map_insurance.groupby(['district', 'state'])['count'].sum().reset_index()
    district_ins = district_ins.sort_values('count', ascending=False).head(10)
    district_ins['label'] = district_ins['district'] + ' (' + district_ins['state'] + ')'
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=district_ins, x='count', y='label',
               palette='coolwarm', ax=ax)
    ax.set_xlabel("Total Insurance Transactions")
    ax.set_ylabel("District (State)")
    st.pyplot(fig)

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.markdown("""
    <p style='text-align: center; color: gray;'>
    PhonePe Transaction Insights Dashboard | Data from PhonePe Pulse GitHub (2018-2024)
    </p>
""", unsafe_allow_html=True)