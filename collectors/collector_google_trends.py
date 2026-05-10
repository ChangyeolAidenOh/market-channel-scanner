"""
Collector: Google Trends
Core 6 + Watchlist 3. Manual CSV fallback if 429 rate limited.
"""
import os
import time
import pandas as pd

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

KEYWORDS = ['Korean skincare', 'Medicube', 'PDRN skincare', 'K-beauty']

TARGET_GEOS = {
    'US': 'United States', 'DE': 'Germany', 'GB': 'United Kingdom',
    'FR': 'France', 'PL': 'Poland', 'ES': 'Spain',
    'KZ': 'Kazakhstan', 'AE': 'UAE', 'BR': 'Brazil',
}

PAUSE_SECONDS = 30  # v2: increased from 5 to 30 for rate limit
TIMEFRAME = 'today 5-y'


def collect_via_api():
    """Attempt pytrends API collection."""
    from pytrends.request import TrendReq
    pytrends = TrendReq(hl='en-US', tz=360)
    all_data = []

    for kw in KEYWORDS:
        try:
            pytrends.build_payload([kw], timeframe=TIMEFRAME)
            region_df = pytrends.interest_by_region(resolution='COUNTRY')
            region_df = region_df.rename(columns={kw: 'interest'})
            region_df['keyword'] = kw
            region_df = region_df.reset_index().rename(columns={'geoName': 'country'})
            all_data.append(region_df)
            print(f"Collected region interest: '{kw}' ({len(region_df)} countries)")
            time.sleep(PAUSE_SECONDS)
        except Exception as e:
            print(f"Failed '{kw}': {e}")
            if '429' in str(e):
                print("Rate limited. Switch to manual CSV download.")
                print("Go to: https://trends.google.com/trends/")
                return None
            time.sleep(PAUSE_SECONDS)

    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        return result
    return None


def collect():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Check for manually downloaded CSV first
    manual_path = os.path.join(OUTPUT_DIR, 'google_trends_manual.csv')
    if os.path.exists(manual_path):
        print(f"Using manually downloaded trends data: {manual_path}")
        return

    print("Attempting pytrends API collection...")
    print(f"Pause between calls: {PAUSE_SECONDS}s")

    result = collect_via_api()
    if result is not None:
        path = os.path.join(OUTPUT_DIR, 'google_trends_by_region.csv')
        result.to_csv(path, index=False)
        print(f"Saved: {path}")
    else:
        print("\n=== MANUAL DOWNLOAD INSTRUCTIONS ===")
        print("1. Go to https://trends.google.com/trends/")
        print("2. Enter each keyword and download CSV:")
        for kw in KEYWORDS:
            print(f"   - '{kw}'")
        print(f"3. Save combined data as: {manual_path}")
        print("4. Re-run this collector.")


if __name__ == '__main__':
    collect()
