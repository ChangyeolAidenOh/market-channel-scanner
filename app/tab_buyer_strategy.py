"""
Tab 2: Buyer Strategy
Account brief cards, competitor positioning, objection handling.
"""
import streamlit as st
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

COUNTRY_MAP = {
    'US': 'United States', 'GB': 'United Kingdom', 'DE': 'Germany',
    'FR': 'France', 'PL': 'Poland', 'ES': 'Spain',
    'KZ': 'Kazakhstan', 'AE': 'United Arab Emirates', 'BR': 'Brazil',
    'EU': 'EU (Cross-border)',
}


def load_buyers():
    with open(os.path.join(DATA_DIR, 'reference', 'buyers.json'), 'r') as f:
        return json.load(f)['buyers']


def render():
    buyers = load_buyers()

    # Country filter
    countries = sorted(set(b['country'] for b in buyers))
    country_labels = [f"{c} - {COUNTRY_MAP.get(c, c)}" for c in countries]

    selected_country = st.selectbox(
        "Filter by country",
        ['All'] + countries,
        format_func=lambda x: 'All countries' if x == 'All' else f"{x} - {COUNTRY_MAP.get(x, x)}"
    )

    if selected_country == 'All':
        filtered = buyers
    else:
        filtered = [b for b in buyers if b['country'] == selected_country]

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    active = sum(1 for b in filtered if 'Active' in b.get('apr_current_status', ''))
    not_entered = sum(1 for b in filtered if 'Not entered' in b.get('apr_current_status', ''))
    reactivation = sum(1 for b in filtered if 'Not Available' in b.get('apr_current_status', '') or 'inactive' in b.get('apr_current_status', ''))
    col1.metric("Active Accounts", active)
    col2.metric("Not Entered", not_entered)
    col3.metric("Reactivation Needed", reactivation)

    st.markdown("---")

    # Buyer cards
    for buyer in filtered:
        status = buyer.get('apr_current_status', '')
        if 'Active' in status:
            status_color = '🟢'
        elif 'Not entered' in status or 'Planned' in status:
            status_color = '🔴'
        elif 'inactive' in status or 'Not Available' in status:
            status_color = '🟡'
        else:
            status_color = '⚪'

        with st.expander(
            f"{status_color} {buyer['buyer']} ({buyer['country']}) — {buyer['channel_type']}"
        ):
            # Status and context
            st.markdown(f"**Status:** {status}")
            st.markdown(f"**Channel:** {buyer['channel_type']} ({buyer.get('online_offline', '')})")
            st.markdown(f"**Scale:** {buyer.get('scale', '').title()}")

            st.markdown("---")

            # Why Now + Entry Angle
            st.markdown("**Why Now**")
            st.markdown(buyer.get('why_now', ''))

            st.markdown("**Entry Angle**")
            st.markdown(buyer.get('apr_entry_angle', ''))

            st.markdown("---")

            # Commercial Hypothesis
            hypothesis = buyer.get('commercial_hypothesis', '')
            if hypothesis:
                st.markdown("**Commercial Hypothesis**")
                st.info(hypothesis)

            # Recommended Products
            products = buyer.get('first_pitch_products', [])
            if products:
                st.markdown("**Recommended Lineup**")
                for p in products:
                    st.markdown(f"- {p}")

            st.markdown("---")

            # Go-to-Market
            test = buyer.get('test_structure', '')
            if test:
                st.markdown("**Go-to-Market Approach**")
                st.markdown(test)

            kpis = buyer.get('success_kpi', [])
            if kpis:
                st.markdown("**Success KPIs:** " + ", ".join(kpis))

            risk = buyer.get('risk', '')
            if risk:
                st.markdown(f"**Risk:** {risk}")

            st.markdown("---")

            # Objection Handling
            objections = buyer.get('objection_response', {})
            if objections:
                st.markdown("**Key Considerations**")
                for concern, response in objections.items():
                    st.markdown(f"*\"{concern}\"*")
                    st.markdown(f"> {response}")
                    st.markdown("")

            # K-beauty presence
            kbeauty = buyer.get('kbeauty_presence', [])
            if kbeauty:
                with st.expander("K-beauty brands on this channel"):
                    st.markdown(", ".join(kbeauty))
