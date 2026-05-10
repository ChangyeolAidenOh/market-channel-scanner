"""
Tab 2: U.S. Channel Map
US-focused account briefs with channel positioning, priority ladder, and cross-channel analysis.
"""
import streamlit as st
import json
import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

US_BUYER_IDS = ['amazon_us', 'ulta_us', 'target_us', 'tiktokshop_us']


def load_buyers():
    with open(os.path.join(DATA_DIR, 'reference', 'buyers.json'), 'r') as f:
        return json.load(f)['buyers']


def render():
    buyers = load_buyers()
    us_buyers = [b for b in buyers if b['id'] in US_BUYER_IDS]
    eu_buyers = [b for b in buyers if b['id'] not in US_BUYER_IDS]

    # Executive Summary
    st.markdown(
        "This project began with a 9-market global scan and narrowed to the U.S. "
        "as APR's core commercial market. The U.S. is not a new-entry market; "
        "APR already has visible Medicube/APRILSKIN presence across Amazon, Ulta, "
        "and TikTok Shop. Therefore, the playbook focuses on sell-through growth, "
        "SKU productivity, channel expansion, and cross-channel pricing governance."
    )

    # Channel overview metrics (2-line format to avoid truncation)
    st.subheader("U.S. Channel Overview")
    cols = st.columns(4)
    with cols[0]:
        st.metric("Amazon", "487 APR results")
        st.caption("121K+ ratings on Zero Pore Pad")
        st.caption("Marketplace | Public-source validated")
    with cols[1]:
        st.metric("Ulta", "1,338 K-beauty products")
        st.caption("Featured Brand placement observed")
        st.caption("Specialty | Public-source validated")
    with cols[2]:
        st.metric("Target", "558 K-beauty products")
        st.caption("~47 brands incl. Medicube")
        st.caption("Mass Retail | Partially validated")
    with cols[3]:
        st.metric("TikTok Shop", "5.7M+ public sold")
        st.caption("479K followers, 962 videos")
        st.caption("Social Commerce | Public metrics observed")

    st.markdown("---")

    # Priority Ladder
    st.subheader("U.S. Channel Priority Ladder")
    st.caption(
        "Priority is based on near-term U.S. growth leverage, not channel prestige. "
        "Amazon protects existing proof, TikTok Shop accelerates public demand conversion, "
        "Ulta builds specialty retail credibility, Target expands mass accessibility."
    )
    ladder = pd.DataFrame([
        {'Priority': 1, 'Channel': 'Amazon',
         'Role': 'Proof channel',
         'Logic': 'Existing hero SKU traction and review/search base must be protected. Amazon performance is the foundation for pitching other retailers.'},
        {'Priority': 2, 'Channel': 'TikTok Shop',
         'Role': 'Growth acceleration',
         'Logic': 'Strongest public unit-sales signal observed. Aprilskin scaling opportunity. Requires pricing governance to avoid channel conflict.'},
        {'Priority': 3, 'Channel': 'Ulta',
         'Role': 'Brand elevation',
         'Logic': 'Premium specialty retail with Featured Brand placement and Only at Ulta exclusivity. AGE-R in-store device experience opportunity.'},
        {'Priority': 4, 'Channel': 'Target',
         'Role': 'Mass accessibility',
         'Logic': 'Mass retail K-beauty category. Post-Ulta beauty transition may create partnership window. Partially validated.'},
        {'Priority': 5, 'Channel': 'Costco',
         'Role': 'Exploratory',
         'Logic': 'Club/volume bundle hypothesis. 86 Korean skincare results observed, no Medicube. Requires buyer validation.'},
    ])
    st.dataframe(ladder, use_container_width=True, hide_index=True)

    st.markdown("---")

    # Channel positioning comparison
    st.subheader("Channel Positioning")
    pos_data = pd.DataFrame([
        {
            'Channel': 'Amazon',
            'Role': 'Demand validation + SKU expansion',
            'Price Strategy': 'Competitive ($14-$19)',
            'Discovery': 'Search + category browsing',
            'Key Asset': '121K+ ratings on Zero Pore Pad',
        },
        {
            'Channel': 'Ulta',
            'Role': 'Premium retail + in-store experience',
            'Price Strategy': 'Full price ($19-$21)',
            'Discovery': 'K-Beauty category + Featured Brand',
            'Key Asset': 'Only at Ulta exclusivity',
        },
        {
            'Channel': 'Target',
            'Role': 'Mass retail expansion',
            'Price Strategy': 'Value-oriented ($3-$25)',
            'Discovery': 'Korean Beauty category',
            'Key Asset': 'Post-Ulta beauty transition (fall 2026)',
        },
        {
            'Channel': 'TikTok Shop',
            'Role': 'Volume driver + content commerce',
            'Price Strategy': 'Aggressive discounts observed',
            'Discovery': 'Content-driven (no K-beauty category)',
            'Key Asset': '5.7M+ public sold, 962 videos',
        },
    ])
    st.dataframe(pos_data, use_container_width=True, hide_index=True)

    # Cross-channel pricing risk
    st.subheader("Cross-Channel Pricing Risk")
    st.warning(
        "Several observed TikTok Shop listings used aggressive discounting, "
        "often materially below traditional retail price points. "
        "Zero Pore Pad sells at approximately $15 on Amazon, $21 at Ulta, "
        "and as low as $20.90 on TikTok Shop (with deeper discounts in bundles). "
        "Recommendation: differentiate by format -- TikTok-exclusive bundles "
        "that are not available at retail."
    )

    # Target-Ulta transition alert
    st.subheader("Strategic Alert: Target-Ulta Partnership Ending")
    st.info(
        "The Ulta Beauty at Target shop-in-shop partnership (600+ stores since 2021) "
        "ends August 2026. Target has announced plans for its own beauty experience "
        "in stores by fall 2026. "
        "This transition may create opportunities for brands to engage directly "
        "with Target's beauty team as K-beauty partners."
    )

    st.markdown("---")

    # Aprilskin TikTok growth gap
    st.subheader("APR Portfolio Gap: Aprilskin on TikTok Shop")
    gap_cols = st.columns(2)
    with gap_cols[0]:
        st.metric("Medicube TikTok Shop", "5.7M+ sold")
        st.metric("Followers", "479.8K")
        st.metric("Videos", "962")
    with gap_cols[1]:
        st.metric("Aprilskin TikTok Shop", "53.5K sold")
        st.metric("Followers", "37.6K")
        st.metric("Videos", "121")
    st.markdown(
        "Aprilskin shows a large public traction gap versus Medicube on TikTok Shop. "
        "Testing whether Medicube's observed content strategy "
        "(bundle format, high video count) can be adapted to Aprilskin "
        "is a significant internal growth opportunity."
    )
    st.caption("Source: public TikTok Shop pages, observed May 2026")

    st.markdown("---")

    # U.S. Account Briefs
    st.subheader("U.S. Account Briefs")
    for buyer in us_buyers:
        status = buyer.get('apr_current_status', '')
        ev = buyer.get('evidence_status', '')

        if 'Active' in status:
            dot = '(Active)'
        elif 'Partially' in ev:
            dot = '(Partial)'
        else:
            dot = ''

        with st.expander(
            f"{buyer['buyer']} -- {buyer['channel_type']} | {ev} {dot}"
        ):
            st.markdown(f"**Primary Buyer Ask:** {buyer.get('buyer_ask', '')}")
            st.markdown("---")

            hypothesis = buyer.get('commercial_hypothesis', '')
            if hypothesis:
                st.info(hypothesis)

            products = buyer.get('first_pitch_products', [])
            if products:
                st.markdown("**Recommended Lineup:** " + " | ".join(products))

            go_nogo = buyer.get('go_nogo', '')
            if go_nogo:
                st.markdown(f"**Go/No-Go:** {go_nogo}")

            risk = buyer.get('risk', '')
            if risk:
                st.markdown(f"**Risk:** {risk}")

            objections = buyer.get('objection_response', {})
            if objections:
                with st.expander("Key Considerations"):
                    for concern, response in objections.items():
                        st.markdown(f"*\"{concern}\"*")
                        st.markdown(f"> {response}")

    # European Benchmark (collapsed)
    st.markdown("---")
    st.subheader("European and CIS Benchmark (Reference)")
    st.markdown(
        "14 European/CIS channels were validated as cross-market reference points. "
        "These are not active U.S. targets but provide competitive intelligence "
        "for U.S. buyer negotiations."
    )
    with st.expander("View European/CIS Account Briefs"):
        for buyer in eu_buyers:
            status = buyer.get('apr_current_status', '')
            ev = buyer.get('evidence_status', '')
            st.markdown(
                f"**{buyer['buyer']}** ({buyer['country']}) -- "
                f"{buyer['channel_type']} | {ev} | {status[:60]}"
            )
