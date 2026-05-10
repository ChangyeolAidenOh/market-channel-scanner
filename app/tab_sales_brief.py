"""
Tab 4: Sales Brief Generator
Generate account briefs for U.S. and European buyer meetings.
"""
import streamlit as st
import json
import os
import sys
import importlib.util

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')


def load_buyers():
    with open(os.path.join(DATA_DIR, 'reference', 'buyers.json'), 'r') as f:
        return json.load(f)['buyers']


def load_scores():
    import pandas as pd
    scores = pd.read_csv(os.path.join(DATA_DIR, 'processed', 'market_scores.csv'))
    return scores


def load_generator():
    spec = importlib.util.spec_from_file_location(
        "sales_brief_generator",
        os.path.join(OUTPUTS_DIR, "sales_brief_generator.py")
    )
    sbg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sbg)
    return sbg.generate_brief


def render():
    buyers = load_buyers()
    scores = load_scores()

    st.markdown(
        "Generate a PDF account brief for any buyer. "
        "Select a buyer below and click Generate."
    )

    # Buyer selector
    buyer_options = {b['id']: f"{b['buyer']} ({b['country']})" for b in buyers}
    selected_id = st.selectbox(
        "Select buyer",
        list(buyer_options.keys()),
        format_func=lambda x: buyer_options[x]
    )

    selected_buyer = next(b for b in buyers if b['id'] == selected_id)

    # Preview
    st.markdown("---")
    st.subheader(f"Preview: {selected_buyer['buyer']}")

    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Country:** {selected_buyer['country']}")
    col2.markdown(f"**Channel:** {selected_buyer['channel_type']}")
    col3.markdown(f"**Status:** {selected_buyer.get('apr_current_status', 'N/A')[:60]}")

    # Evidence status
    ev = selected_buyer.get('evidence_status', '')
    if ev:
        st.markdown(f"**Evidence Status:** {ev}")

    # Buyer Ask
    buyer_ask = selected_buyer.get('buyer_ask', '')
    if buyer_ask:
        st.markdown(f"**Primary Buyer Ask:** {buyer_ask}")

    # Commercial Hypothesis
    hypothesis = selected_buyer.get('commercial_hypothesis', '')
    if hypothesis:
        st.markdown("**Commercial Hypothesis**")
        st.info(hypothesis)

    # Recommended products
    products = selected_buyer.get('first_pitch_products', [])
    if products:
        st.markdown("**Recommended Lineup:** " + " | ".join(products))

    # Go/No-Go
    go_nogo = selected_buyer.get('go_nogo', '')
    if go_nogo:
        st.markdown(f"**Go/No-Go:** {go_nogo}")

    # Market context from scores
    iso2 = selected_buyer['country'].split('/')[0].split(' ')[0]
    iso3_map = {
        'US': 'USA', 'GB': 'GBR', 'DE': 'DEU', 'FR': 'FRA',
        'PL': 'POL', 'ES': 'ESP', 'KZ': 'KAZ', 'AE': 'ARE', 'BR': 'BRA',
        'EU': None
    }
    iso3 = iso3_map.get(iso2)
    if iso3:
        country_score = scores[scores['country_iso3'] == iso3]
        if not country_score.empty:
            row = country_score.iloc[0]
            st.markdown("**Market Context**")
            mcol1, mcol2, mcol3 = st.columns(3)
            mcol1.metric("Base Rank", f"#{int(row['base_rank'])}")
            mcol2.metric("Stability", row['stability'])
            mcol3.metric("Market Role", row['market_role'][:30] + "...")

    # Key considerations
    objections = selected_buyer.get('objection_response', {})
    if objections:
        st.markdown("**Key Considerations**")
        for concern, response in objections.items():
            st.markdown(f"- *{concern}* -- {response[:100]}...")

    # PDF generation
    st.markdown("---")
    if st.button("Generate PDF Brief", type="primary"):
        try:
            generate_brief = load_generator()

            market_score = None
            if iso3:
                country_score = scores[scores['country_iso3'] == iso3]
                if not country_score.empty:
                    market_score = round(country_score.iloc[0]['base'], 1)

            output_path = os.path.join(OUTPUTS_DIR, f'brief_{selected_id}.pdf')
            generate_brief(selected_id, market_score=market_score, output_path=output_path)

            with open(output_path, 'rb') as f:
                pdf_bytes = f.read()

            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"brief_{selected_id}.pdf",
                mime="application/pdf"
            )
            st.success(f"Brief generated for {selected_buyer['buyer']}")
        except Exception as e:
            st.error(f"PDF generation failed: {e}")
