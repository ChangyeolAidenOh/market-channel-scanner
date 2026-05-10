"""
Tab 3: SKU x Channel Fit
Product-channel matrix for U.S. market.
Shows which products fit which channels based on price, format, and positioning.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

GREEN_VALUES = {
    'Active', 'Hero', 'Listed', 'High volume', 'Only at Ulta',
    'Price fit', '233K sold', '183K sold',
    '3K sold', '1.7K sold',
}
YELLOW_VALUES = {
    'Expand', 'Entry tier', 'Grow', 'In-store demo', 'Beauty Studio',
}
RED_VALUES = {
    'Price risk',
}


def load_apr():
    with open(os.path.join(DATA_DIR, 'reference', 'apr_products.json'), 'r') as f:
        return json.load(f)


def render():
    apr = load_apr()

    st.markdown(
        "Which APR products fit which U.S. channels? "
        "This matrix maps product-channel fit based on price positioning, "
        "format compatibility, and observed presence."
    )

    # Product-Channel Fit Matrix
    st.subheader("Product x Channel Fit Matrix")

    fit_data = [
        {'Brand': 'Medicube', 'Product': 'Zero Pore Pad 2.0', 'Price': '$15-21',
         'Amazon': 'Hero', 'Ulta': 'Only at Ulta', 'Target': 'Listed', 'TikTok': 'High volume',
         'Fit Note': 'Universal hero SKU. Anchor product across all channels.'},
        {'Brand': 'Medicube', 'Product': 'PDRN Pink Peptide Serum', 'Price': '$19-28',
         'Amazon': 'Active', 'Ulta': 'Active', 'Target': 'Expand', 'TikTok': 'High volume',
         'Fit Note': 'Premium skincare. Good Ulta/Amazon fit. Target price ceiling risk.'},
        {'Brand': 'Medicube', 'Product': 'Collagen Night Wrapping Mask', 'Price': '$24-29',
         'Amazon': 'Active', 'Ulta': 'Expand', 'Target': 'Expand', 'TikTok': '233K sold',
         'Fit Note': 'TikTok bestseller. Potential to expand to retail channels.'},
        {'Brand': 'Medicube', 'Product': 'PDRN Cream', 'Price': '$28-32',
         'Amazon': 'Active', 'Ulta': 'Expand', 'Target': 'Price risk', 'TikTok': 'Active',
         'Fit Note': 'Premium tier. Target mass pricing may not support.'},
        {'Brand': 'Medicube', 'Product': 'AGE-R Booster Pro', 'Price': '$200-250',
         'Amazon': 'Listed', 'Ulta': 'In-store demo', 'Target': 'Beauty Studio', 'TikTok': '183K sold',
         'Fit Note': 'Device. Best suited for Ulta in-store + TikTok bundles.'},
        {'Brand': 'Medicube', 'Product': 'Collagen Jelly Cream', 'Price': '$15-26',
         'Amazon': 'Active', 'Ulta': 'Expand', 'Target': 'Listed', 'TikTok': 'Active',
         'Fit Note': 'Mid-price. Good mass retail fit.'},
        {'Brand': 'Aprilskin', 'Product': 'TXA Niacinamide Deep Cleanser', 'Price': '$8-11',
         'Amazon': 'Active', 'Ulta': 'Entry tier', 'Target': 'Price fit', 'TikTok': '3K sold',
         'Fit Note': 'Entry tier. Best Target/mass fit. TikTok growth opportunity.'},
        {'Brand': 'Aprilskin', 'Product': 'Calendula Peel Off Mask', 'Price': '$8-13',
         'Amazon': 'Active', 'Ulta': 'Entry tier', 'Target': 'Price fit', 'TikTok': 'Grow',
         'Fit Note': 'Viral potential. Mass retail price point.'},
        {'Brand': 'Aprilskin', 'Product': 'Carrotene IPMP Cleansing Balm', 'Price': '$11-25',
         'Amazon': 'Active', 'Ulta': 'Expand', 'Target': 'Price fit', 'TikTok': '1.7K sold',
         'Fit Note': 'Mid-price Aprilskin hero. Cross-channel potential.'},
    ]

    df = pd.DataFrame(fit_data)

    def color_fit(val):
        val = str(val)
        if val in GREEN_VALUES:
            return 'background-color: #DCFCE7'
        elif val in YELLOW_VALUES:
            return 'background-color: #FEF9C3'
        elif val in RED_VALUES:
            return 'background-color: #FEE2E2'
        return ''

    styled = df.style.map(
        color_fit, subset=['Amazon', 'Ulta', 'Target', 'TikTok']
    )
    st.dataframe(styled, use_container_width=True, hide_index=True, height=400)

    st.caption(
        "Green = Active or strong fit | Yellow = Expansion opportunity | Red = Price/format risk"
    )
    st.caption(
        "Fit labels combine public retailer evidence and strategic "
        "channel-fit judgment; they are not internal APR sales data."
    )

    st.markdown("---")

    # Channel Strategy Summary
    st.subheader("Channel Strategy Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Amazon: SKU Depth + Search Defense**")
        st.markdown(
            "Amazon is the demand-validation channel. "
            "Hero SKU (Zero Pore Pad, 121K reviews) must be protected. "
            "Expand adjacent PDRN/TXA SKUs for cross-sell. "
            "Subscribe & Save, if available, could serve as a retention lever."
        )

        st.markdown("**Target: Mass Retail + Beauty Studio Transition**")
        st.markdown(
            "Target's Korean Beauty category (558 products, 47 brands) "
            "is the mass retail opportunity. Aprilskin's $8-16 price point "
            "fits Target better than Medicube's premium tier. "
            "Post-Ulta Beauty Studio launch (fall 2026) creates a "
            "partnership window."
        )

    with col2:
        st.markdown("**Ulta: Premium Experience + Device**")
        st.markdown(
            "Ulta is the premium retail channel. Featured Brand placement "
            "and Only at Ulta exclusivity differentiate from Amazon. "
            "AGE-R in-store demo is a high-value expansion opportunity. "
            "Staff training and display support are prerequisites."
        )

        st.markdown("**TikTok Shop: Volume + Content Commerce**")
        st.markdown(
            "TikTok Shop shows the highest publicly reported unit volume (5.7M+ sold). "
            "Bundle strategy dominates. Aprilskin growth (53.5K to scale) "
            "is a significant internal opportunity. "
            "Cross-channel pricing governance is critical."
        )

    st.markdown("---")

    # Price Positioning Map
    st.subheader("Price Positioning by Channel")

    price_chart = go.Figure()

    products = [
        ('Aprilskin TXA Cleanser', 8, 11, 'Aprilskin'),
        ('Aprilskin Calendula Mask', 8, 13, 'Aprilskin'),
        ('Aprilskin Carrotene Balm', 11, 25, 'Aprilskin'),
        ('Zero Pore Pad 2.0', 15, 21, 'Medicube'),
        ('Collagen Jelly Cream', 15, 26, 'Medicube'),
        ('PDRN Peptide Serum', 19, 28, 'Medicube'),
        ('Collagen Night Mask', 24, 29, 'Medicube'),
        ('PDRN Cream', 28, 32, 'Medicube'),
        ('AGE-R Booster Pro', 93, 250, 'Medicube'),
    ]

    colors = {'Medicube': '#E11D48', 'Aprilskin': '#F59E0B'}

    for name, low, high, brand in products:
        price_chart.add_trace(go.Bar(
            name=brand,
            x=[high - low],
            y=[name],
            base=[low],
            orientation='h',
            marker_color=colors[brand],
            showlegend=False,
            text=f'${low}-${high}',
            textposition='inside',
        ))

    price_chart.add_vrect(x0=0, x1=16, fillcolor='#FEF3C7',
                          opacity=0.15, line_width=0,
                          annotation_text='Target core', annotation_position='top left')
    price_chart.add_vrect(x0=15, x1=35, fillcolor='#DBEAFE',
                          opacity=0.15, line_width=0,
                          annotation_text='Ulta/Amazon', annotation_position='top left')

    price_chart.update_layout(
        title='APR Product Price Range vs Channel Sweet Spots',
        xaxis_title='Price (USD)',
        height=400,
        margin=dict(l=10, r=10, t=40, b=10),
        barmode='stack',
    )
    st.plotly_chart(price_chart, use_container_width=True)

    st.caption(
        "Yellow zone: Target mass retail sweet spot ($3-$16). "
        "Blue zone: Ulta/Amazon specialty sweet spot ($15-$35). "
        "AGE-R device ($93-$250) excluded from zone overlay for readability. "
        "Prices are approximate and based on public storefront observations."
    )

    st.markdown("---")

    # Cross-market reference
    st.subheader("Cross-Market Reference Points")
    st.markdown(
        "European retailer research provides reference data for U.S. buyer negotiations:"
    )
    refs = [
        "**Amazon 121K+ ratings/reviews** + **Notino strong top-rated visibility** -- demand validation for any new retailer pitch",
        "**Ulta Featured Brand** + **Douglas 30 SKUs** -- suggests APR can scale with premium retailers",
        "**Rossmann ISANA PB** -- suggests drugstore demand is strong enough for retailer private label investment in K-beauty",
        "**Sephora editorial gap** -- Medicube has product presence but is not yet named in editorial; similar pattern may exist at U.S. retailers",
        "**Primor Not Available** -- reactivation risk lesson; supply stability is non-negotiable for channel expansion",
        "**TikTok 5.7M+ public sold** -- highest publicly reported unit volume; validates social commerce as a major demand driver",
    ]
    for ref in refs:
        st.markdown(f"- {ref}")
