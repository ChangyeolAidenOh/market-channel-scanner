"""
Collector: World Bank Indicators
Core 6 + Watchlist 3 countries. NaN-safe year handling.
"""
import os
import wbgapi as wb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TARGET_COUNTRIES = [
    'USA', 'DEU', 'GBR', 'FRA', 'POL', 'ESP',
    'KAZ', 'ARE', 'BRA',
    'KOR', 'JPN',
]

INDICATORS = {
    'NY.GDP.PCAP.PP.CD': 'gdp_per_capita_ppp',
    'SP.POP.TOTL': 'population',
    'IT.NET.USER.ZS': 'internet_users_pct',
}

YEAR_RANGE = range(2018, 2025)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')


def collect():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    frames = []

    for wb_code, col_name in INDICATORS.items():
        try:
            df = wb.data.DataFrame(
                wb_code, TARGET_COUNTRIES,
                time=YEAR_RANGE, labels=True
            )
            df = df.reset_index()
            df_melted = df.melt(
                id_vars=['economy'],
                var_name='year_raw',
                value_name=col_name
            )
            # Extract year number safely
            df_melted['year'] = pd.to_numeric(
                df_melted['year_raw'].str.extract(r'(\d{4})', expand=False),
                errors='coerce'
            )
            df_melted = df_melted.dropna(subset=['year'])
            df_melted['year'] = df_melted['year'].astype(int)
            df_melted = df_melted.drop(columns=['year_raw'])
            frames.append(df_melted)
            print(f"Collected {col_name}: {len(df_melted)} rows")
        except Exception as e:
            print(f"Failed {col_name}: {e}")

    if not frames:
        print("No data collected.")
        return

    result = frames[0]
    for f in frames[1:]:
        result = result.merge(f, on=['economy', 'year'], how='outer')

    output_path = os.path.join(OUTPUT_DIR, 'world_bank_indicators.csv')
    result.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path}")
    print(f"Shape: {result.shape}")
    print(f"Countries: {sorted(result['economy'].unique())}")
    print(f"Years: {sorted(result['year'].unique())}")
    print(f"\nSample (latest year):")
    latest = result[result['year'] == result['year'].max()]
    print(latest.to_string(index=False))


if __name__ == '__main__':
    collect()
