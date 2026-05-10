"""
Tab 1: Market Scanner
Country-level market attractiveness with sensitivity analysis.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def load_data():
    scores = pd.read_csv(os.path.join(DATA_DIR, 'processed', 'market_scores.csv'))
    features = pd.read_csv(os.path.join(DATA_DIR, 'processed', 'country_features.csv'))
    with open(os.path.join(DATA_DIR, 'reference', 'country_qualitative.json'), 'r') as f:
        qual = json.load(f)
    return scores, features, qual


def render():
    scores, features, qual = load_data()

    # Provisional notice
    st.info(
        "Competition whitespace scores are provisional. "
        "They reflect retailer-level manual research (Stage 3) and will be "
        "updated as additional channels are verified."
    )

    # Scenario selector
    scenario = st.selectbox(
        "Select scoring scenario",
        ['base', 'growth_focused', 'risk_controlled', 'channel_expansion'],
        format_func=lambda x: {
            'base': 'Base (balanced weights)',
            'growth_focused': 'Growth-Focused (import growth + search interest)',
            'risk_controlled': 'Risk-Controlled (GDP + regulation + competition)',
            'channel_expansion': 'Channel Expansion (import volume + competition)',
        }[x]
    )

    rank_col = f'{scenario}_rank'

    # Main ranking chart
    chart_data = scores.sort_values(rank_col)
    fig = px.bar(
        chart_data,
        x=scenario,
        y='name',
        orientation='h',
        color='tier',
        color_discrete_map={'core': '#2563EB', 'watchlist': '#F59E0B'},
        text=chart_data[rank_col].apply(lambda x: f'#{x}'),
        labels={scenario: 'Opportunity Score', 'name': ''},
    )
    fig.update_layout(
        title=f'Market Opportunity Score ({scenario.replace("_", " ").title()})',
        height=420,
        showlegend=True,
        legend_title_text='Tier',
        yaxis={'categoryorder': 'total ascending'},
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig.update_traces(textposition='inside')
    st.plotly_chart(fig, use_container_width=True)

    # Sensitivity comparison table
    st.subheader("Sensitivity Analysis")
    st.markdown(
        "Google Trends values are relative indices, not absolute search volume. "
        "They are used as directional signals to compare category-level interest "
        "across markets."
    )
    display = scores[[
        'name', 'tier', 'base_rank', 'growth_focused_rank',
        'risk_controlled_rank', 'channel_expansion_rank',
        'stability', 'market_role'
    ]].copy()
    display.columns = [
        'Country', 'Tier', 'Base', 'Growth', 'Risk', 'Channel',
        'Stability', 'Market Role'
    ]
    display = display.sort_values('Base')

    def color_stability(val):
        colors = {
            'stable': 'background-color: #DCFCE7',
            'moderate': 'background-color: #FEF9C3',
            'volatile': 'background-color: #FEE2E2',
        }
        return colors.get(val, '')

    st.dataframe(
        display.style.applymap(color_stability, subset=['Stability']),
        use_container_width=True,
        hide_index=True,
    )

    # Feature breakdown per country
    st.subheader("Feature Breakdown")
    selected = st.selectbox("Select country", scores['name'].tolist())
    sel_iso3 = scores[scores['name'] == selected]['country_iso3'].values[0]
    sel_iso2 = scores[scores['name'] == selected]['country_iso2'].values[0]
    sel_features = features[features['country_iso3'] == sel_iso3].iloc[0]
    sel_scores = scores[scores['country_iso3'] == sel_iso3].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Base Rank", f"#{int(sel_scores['base_rank'])}")
    col2.metric("Stability", sel_scores['stability'])
    col3.metric("Signal Pattern", sel_features['signal_pattern'])
    col4.metric("Tier", sel_scores['tier'].title())

    # Feature values
    feat_cols = {
        'import_volume': 'Import Volume ($)',
        'import_growth': 'Import Growth (%)',
        'gdp_per_capita': 'GDP/Capita (PPP)',
        'internet_pct': 'Internet (%)',
        'regulation_inv': 'Regulation Score',
        'competition_inv': 'Competition Whitespace',
        'search_interest': 'K-beauty Search Interest',
        'medicube_interest': 'Medicube Brand Signal',
    }
    feat_data = []
    for col, label in feat_cols.items():
        if col in sel_features.index:
            val = sel_features[col]
            if col == 'import_volume':
                val_str = f"${val:,.0f}"
            elif col == 'import_growth':
                val_str = f"{val:.1f}%"
            elif col == 'gdp_per_capita':
                val_str = f"${val:,.0f}"
            elif col == 'internet_pct':
                val_str = f"{val:.1f}%"
            else:
                val_str = f"{val}"
            feat_data.append({'Feature': label, 'Value': val_str, 'Raw': val})

    feat_df = pd.DataFrame(feat_data)
    st.dataframe(feat_df[['Feature', 'Value']], use_container_width=True, hide_index=True)

    # Market role and interpretation
    st.markdown(f"**Market Role:** {sel_scores['market_role']}")
    if sel_scores.get('interpretation'):
        st.markdown(f"**Interpretation:** {sel_scores['interpretation']}")

    # Competition inv note from qualitative JSON
    countries = qual.get('countries', {})
    country_qual = countries.get(sel_iso2, {})
    note = country_qual.get('competition_inv_note', '')
    if note:
        st.caption(f"Competition note: {note}")

    # Qualitative appendix (Russia/Ukraine)
    appendix = qual.get('qualitative_appendix', {})
    if appendix:
        with st.expander("CIS Qualitative Appendix (Russia / Ukraine)"):
            for code, info in appendix.items():
                st.markdown(f"**{info.get('name', code)}**")
                st.markdown(f"K-beauty signal: {info.get('kbeauty_signal', 'N/A')}")
                st.markdown(f"Medicube status: {info.get('medicube_status', 'N/A')}")
                st.markdown(f"Exclusion reason: {info.get('appendix_reason', 'N/A')}")
                st.markdown("---")
