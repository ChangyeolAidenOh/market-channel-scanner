"""
Market Scoring v2.1
Weighted Composite Index + 4-scenario sensitivity analysis.
Connected to real Comtrade data.
"""
import json
import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
REF_DIR = os.path.join(DATA_DIR, 'reference')
OUT_DIR = os.path.join(DATA_DIR, 'processed')

CORE_COUNTRIES = ['USA', 'DEU', 'GBR', 'FRA', 'POL', 'ESP']
WATCHLIST_COUNTRIES = ['KAZ', 'ARE', 'BRA']
ALL_TARGET = CORE_COUNTRIES + WATCHLIST_COUNTRIES

# ISO3 to ISO2 mapping for merging with reference JSONs
ISO3_TO_ISO2 = {
    'USA': 'US', 'DEU': 'DE', 'GBR': 'GB', 'FRA': 'FR',
    'POL': 'PL', 'ESP': 'ES', 'KAZ': 'KZ', 'ARE': 'AE', 'BRA': 'BR',
}

SCENARIOS = {
    'base': {
        'import_growth': 0.25, 'search_interest': 0.20, 'import_volume': 0.15,
        'competition_inv': 0.15, 'gdp_per_capita': 0.10,
        'regulation_inv': 0.10, 'internet_pct': 0.05,
    },
    'growth_focused': {
        'import_growth': 0.35, 'search_interest': 0.25, 'import_volume': 0.10,
        'competition_inv': 0.10, 'gdp_per_capita': 0.05,
        'regulation_inv': 0.10, 'internet_pct': 0.05,
    },
    'risk_controlled': {
        'import_growth': 0.10, 'search_interest': 0.10, 'import_volume': 0.10,
        'competition_inv': 0.20, 'gdp_per_capita': 0.20,
        'regulation_inv': 0.25, 'internet_pct': 0.05,
    },
    'channel_expansion': {
        'import_growth': 0.15, 'search_interest': 0.10, 'import_volume': 0.25,
        'competition_inv': 0.25, 'gdp_per_capita': 0.10,
        'regulation_inv': 0.10, 'internet_pct': 0.05,
    },
}


def normalize_0_100(series):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series(50.0, index=series.index)
    return ((series - mn) / (mx - mn) * 100).round(1)


def load_qualitative():
    path = os.path.join(REF_DIR, 'country_qualitative.json')
    with open(path, 'r') as f:
        return json.load(f)['countries']


def process_comtrade():
    """
    Extract import_volume and import_growth from Comtrade data.
    Uses HS 3304 (broader) for volume, calculates YoY growth.
    """
    path = os.path.join(RAW_DIR, 'comtrade_hs3304.csv')
    if not os.path.exists(path):
        print("Comtrade data not found.")
        return pd.DataFrame()

    df = pd.read_csv(path)
    print(f"Comtrade raw: {len(df)} rows")

    # Filter to HS 3304 (avoid double counting with 330499)
    df_3304 = df[df['cmdCode'].astype(str) == '3304'].copy()

    # Filter to target countries
    df_target = df_3304[df_3304['partnerISO'].isin(ALL_TARGET)].copy()

    # Yearly export value per partner country
    yearly = df_target.groupby(['partnerISO', 'refYear'])['primaryValue'].sum().reset_index()
    yearly.columns = ['country_iso3', 'year', 'export_value']

    print(f"Target country records: {len(yearly)}")
    print(f"Countries found: {sorted(yearly['country_iso3'].unique())}")
    print(f"Years: {sorted(yearly['year'].unique())}")

    # Latest year volume
    latest_year = yearly['year'].max()
    prev_year = latest_year - 1

    volume = yearly[yearly['year'] == latest_year][['country_iso3', 'export_value']].copy()
    volume.columns = ['country_iso3', 'import_volume']

    # YoY growth
    latest = yearly[yearly['year'] == latest_year].set_index('country_iso3')['export_value']
    previous = yearly[yearly['year'] == prev_year].set_index('country_iso3')['export_value']
    growth = ((latest - previous) / previous * 100).round(1)
    growth_df = growth.reset_index()
    growth_df.columns = ['country_iso3', 'import_growth']

    result = volume.merge(growth_df, on='country_iso3', how='outer')

    print(f"\n--- Comtrade Features ({latest_year} vs {prev_year}) ---")
    print(result.to_string(index=False))

    return result


def process_world_bank():
    """Extract GDP per capita and internet usage from World Bank data."""
    path = os.path.join(RAW_DIR, 'world_bank_indicators.csv')
    if not os.path.exists(path):
        print("World Bank data not found.")
        return pd.DataFrame()

    df = pd.read_csv(path)
    print(f"\nWorld Bank raw: {len(df)} rows")

    # ISO3 mapping from economy name (World Bank uses country names)
    # Get latest year with data for each indicator
    features = []
    for iso3 in ALL_TARGET:
        row = {'country_iso3': iso3}

        # Try to find this country in WB data
        # WB uses various name formats, so we try matching
        country_df = df[df['economy'].str.contains(
            iso3[:3], case=False, na=False
        )]

        if not country_df.empty:
            latest = country_df.sort_values('year', ascending=False).iloc[0]
            if 'gdp_per_capita_ppp' in latest:
                row['gdp_per_capita'] = latest.get('gdp_per_capita_ppp', np.nan)
            if 'internet_users_pct' in latest:
                row['internet_pct'] = latest.get('internet_users_pct', np.nan)

        features.append(row)

    result = pd.DataFrame(features)
    return result


def process_trends():
    """Extract search interest from Google Trends region CSVs."""
    country_name_to_iso3 = {
        'United States': 'USA', 'Germany': 'DEU', 'United Kingdom': 'GBR',
        'France': 'FRA', 'Poland': 'POL', 'Spain': 'ESP',
        'Kazakhstan': 'KAZ', 'United Arab Emirates': 'ARE', 'Brazil': 'BRA',
    }

    result = pd.DataFrame({'country_iso3': ALL_TARGET})

    # K-beauty Topic
    kb_path = os.path.join(RAW_DIR, 'trends_kbeauty_topic_region.csv')
    if os.path.exists(kb_path):
        kb = pd.read_csv(kb_path, skiprows=1)
        kb.columns = ['country_name', 'kbeauty_raw']
        kb['country_iso3'] = kb['country_name'].map(country_name_to_iso3)
        kb = kb.dropna(subset=['country_iso3'])
        kb['search_interest'] = pd.to_numeric(kb['kbeauty_raw'], errors='coerce').fillna(0)
        result = result.merge(kb[['country_iso3', 'search_interest']], on='country_iso3', how='left')
        print(f"\nK-beauty Topic loaded: {len(kb)} target countries matched")
        print(kb[['country_name', 'search_interest']].to_string(index=False))

    # Medicube Search term
    mc_path = os.path.join(RAW_DIR, 'trends_medicube_region.csv')
    if os.path.exists(mc_path):
        mc = pd.read_csv(mc_path, skiprows=1)
        mc.columns = ['country_name', 'medicube_raw']
        mc['country_iso3'] = mc['country_name'].map(country_name_to_iso3)
        mc = mc.dropna(subset=['country_iso3'])
        mc['medicube_interest'] = pd.to_numeric(mc['medicube_raw'], errors='coerce').fillna(0)
        result = result.merge(mc[['country_iso3', 'medicube_interest']], on='country_iso3', how='left')
        print(f"\nMedicube loaded: {len(mc)} target countries matched")
        print(mc[['country_name', 'medicube_interest']].to_string(index=False))

    # Fill missing
    result['search_interest'] = result.get('search_interest', pd.Series(0)).fillna(0)
    result['medicube_interest'] = result.get('medicube_interest', pd.Series(0)).fillna(0)

    # Difference interpretation
    kb_median = result['search_interest'].median()
    mc_median = result['medicube_interest'].median()

    def classify_signal(row):
        kb_high = row['search_interest'] >= kb_median
        mc_high = row['medicube_interest'] >= mc_median
        # Both values within similar range → balanced
        if abs(row['search_interest'] - row['medicube_interest']) <= 2:
            if kb_high or mc_high:
                return 'balanced'
            else:
                return 'low-signal'
        if kb_high and mc_high:
            return 'dual-signal'
        elif kb_high and not mc_high:
            return 'category-led'
        elif not kb_high and mc_high:
            return 'brand-led'
        else:
            return 'low-signal'

    result['signal_pattern'] = result.apply(classify_signal, axis=1)

    return result

def build_feature_matrix():
    """Build complete feature matrix from all data sources."""
    qual = load_qualitative()

    # Qualitative features
    reg_scores = {'low': 90, 'medium': 60, 'medium-high': 40, 'high': 20}

    rows = []
    for iso3 in ALL_TARGET:
        iso2 = ISO3_TO_ISO2[iso3]
        q = qual.get(iso2, {})
        rows.append({
            'country_iso3': iso3,
            'country_iso2': iso2,
            'name': q.get('name', iso3),
            'tier': q.get('tier', 'watchlist'),
            'regulation_inv': reg_scores.get(q.get('regulation_complexity', 'medium'), 50),
            # Stage 2 provisional — Stage 3 Should be revised after retailer research
            'competition_inv': {
                'USA': 25, 'DEU': 40, 'GBR': 30, 'FRA': 55,
                'POL': 70, 'ESP': 50, 'KAZ': 55, 'ARE': 70, 'BRA': 75,
            }.get(iso3, 50),
        })

    features = pd.DataFrame(rows)

    # Merge Comtrade features
    comtrade = process_comtrade()
    if not comtrade.empty:
        features = features.merge(comtrade, on='country_iso3', how='left')

    # Merge World Bank features
    wb = process_world_bank()
    if not wb.empty:
        features = features.merge(wb, on='country_iso3', how='left')

    # Merge Trends features
    trends = process_trends()
    if not trends.empty:
        features = features.merge(trends, on='country_iso3', how='left')

    # Fill missing quantitative features with median
    quant_cols = ['import_growth', 'import_volume', 'search_interest',
                  'competition_inv', 'gdp_per_capita', 'internet_pct']
    for col in quant_cols:
        if col not in features.columns:
            features[col] = 50.0
        else:
            features[col] = features[col].fillna(features[col].median())

    print(f"\n--- Feature Matrix ---")
    print(features.to_string(index=False))

    return features


def score_scenario(features, scenario_name):
    weights = SCENARIOS[scenario_name]
    score_cols = [c for c in weights.keys() if c in features.columns]

    normalized = features.copy()
    for col in score_cols:
        normalized[f'{col}_n'] = normalize_0_100(normalized[col])

    total_weight = sum(weights[c] for c in score_cols)
    normalized[scenario_name] = sum(
        normalized[f'{c}_n'] * (weights[c] / total_weight)
        for c in score_cols
    ).round(1)

    return normalized[['country_iso3', scenario_name]]


def sensitivity_analysis(features):
    result = features[['country_iso3', 'country_iso2', 'name', 'tier']].copy()

    for scenario in SCENARIOS:
        scores = score_scenario(features, scenario)
        result = result.merge(scores, on='country_iso3')

    for scenario in SCENARIOS:
        result[f'{scenario}_rank'] = result[scenario].rank(ascending=False).astype(int)

    rank_cols = [f'{s}_rank' for s in SCENARIOS]
    result['rank_std'] = result[rank_cols].std(axis=1).round(2)
    result['stability'] = result['rank_std'].apply(
        lambda x: 'stable' if x < 1.0 else 'moderate' if x < 2.0 else 'volatile'
    )

    return result.sort_values('base', ascending=False)


def add_interpretations(scored, qual):
    interp = {}
    for iso3 in ALL_TARGET:
        iso2 = ISO3_TO_ISO2[iso3]
        q = qual.get(iso2, {})
        interp[iso3] = q.get('strategic_note', '')
    scored['interpretation'] = scored['country_iso3'].map(interp)
    scored['market_role'] = scored['country_iso3'].map(MARKET_ROLE)
    return scored

MARKET_ROLE = {
    'USA': 'Core market - sell-through and channel expansion priority',
    'GBR': 'Core Europe - competitive market, account growth priority',
    'DEU': 'Core Europe - competitive market, differentiation required',
    'POL': 'Secondary Europe - whitespace test market (domestic channels unverified)',
    'ESP': 'Secondary Europe - Medicube reactivation opportunity',
    'FRA': 'Core Europe - premium channel present, editorial visibility gap',
    'KAZ': 'CIS - marketplace-led market, channel control needed',
    'ARE': 'Expansion watchlist - high-signal opportunity',
    'BRA': 'Growth watchlist - volatile/risk-sensitive',
}

def run():
    os.makedirs(OUT_DIR, exist_ok=True)

    features = build_feature_matrix()
    qual = load_qualitative()
    result = sensitivity_analysis(features)
    result = add_interpretations(result, qual)

    output_path = os.path.join(OUT_DIR, 'market_scores.csv')
    result.to_csv(output_path, index=False)

    # Also save feature matrix for debugging
    features_path = os.path.join(OUT_DIR, 'country_features.csv')
    features.to_csv(features_path, index=False)

    print(f"\nSaved: {output_path}")
    print(f"Saved: {features_path}")

    print("\n" + "=" * 70)
    print("SENSITIVITY ANALYSIS RESULTS")
    print("=" * 70)
    display_cols = ['name', 'tier',
                    'base_rank', 'growth_focused_rank',
                    'risk_controlled_rank', 'channel_expansion_rank',
                    'stability', 'market_role']
    print(result[display_cols].to_string(index=False))

    # Feature contribution for top country
    print("\n--- Feature Values (Raw) ---")
    feat_cols = ['name', 'import_volume', 'import_growth',
                 'gdp_per_capita', 'internet_pct',
                 'regulation_inv', 'competition_inv', 'search_interest']
    feat_cols = [c for c in feat_cols if c in features.columns]
    print(features[feat_cols].to_string(index=False))

    return result


if __name__ == '__main__':
    run()
