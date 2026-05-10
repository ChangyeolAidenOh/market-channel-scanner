"""
APR U.S. Sell-through & Channel Expansion Playbook
Global scan to U.S. account-level growth strategy
4 tabs: Global Scan | U.S. Channel Map | SKU x Channel Fit | Sales Brief
"""
import streamlit as st
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="APR U.S. Channel Expansion Playbook",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("APR U.S. Playbook")
st.sidebar.markdown(
    "Global market scan narrowed to U.S. account-level "
    "sell-through and channel expansion strategy."
)
st.sidebar.markdown("---")
st.sidebar.markdown("**U.S. Channels**")
st.sidebar.markdown("Amazon | Ulta | Target | TikTok Shop")
st.sidebar.markdown("**Brands:** Medicube, Aprilskin")
st.sidebar.markdown("---")
st.sidebar.markdown("**European Benchmark**")
st.sidebar.markdown(
    "14 European/CIS retailers validated as "
    "cross-market reference points."
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Data Sources**")
st.sidebar.markdown(
    "UN Comtrade (HS 3304), World Bank, Google Trends, "
    "18 retailer websites (manual research), "
    "TikTok Shop public store data"
)
st.sidebar.markdown("---")
st.sidebar.caption(
    "Built by [Changyeol Oh](https://github.com/ChangyeolAidenOh)"
)
st.sidebar.caption(
    "Candidate Portfolio Simulation | Public-source based"
)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Global Scan → Why U.S.",
    "U.S. Channel Map",
    "SKU × Channel Fit",
    "Sales Brief"
])

with tab1:
    from tab_market_scanner import render as render_scanner
    render_scanner()

with tab2:
    from tab_us_channel_map import render as render_channel
    render_channel()

with tab3:
    from tab_sku_channel_fit import render as render_sku
    render_sku()

with tab4:
    from tab_sales_brief import render as render_brief
    render_brief()
