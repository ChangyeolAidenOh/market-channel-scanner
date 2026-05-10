"""
Collector: UN Comtrade
Korea cosmetics exports to Core 6 + Watchlist 3.
"""
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

REPORTER_KOREA = '410'
PARTNER_CODES = {
    '842': 'US', '276': 'DE', '826': 'GB', '250': 'FR',
    '616': 'PL', '724': 'ES',      # Core
    '398': 'KZ', '784': 'AE', '076': 'BR',  # Watchlist
}
HS_CODES = ['3304', '330499']
YEARS = ['2019', '2020', '2021', '2022', '2023']


def collect_with_api(api_key):
    import comtradeapicall
    all_data = []
    partner_str = ','.join(PARTNER_CODES.keys())

    for year in YEARS:
        for hs in HS_CODES:
            try:
                df = comtradeapicall.getFinalData(
                    api_key,
                    typeCode='C', freqCode='A', clCode='HS',
                    period=year, reporterCode=REPORTER_KOREA,
                    cmdCode=hs, flowCode='X',
                    partnerCode=partner_str,
                    partner2Code=None, customsCode=None, motCode=None,
                    maxRecords=500, format_output='JSON',
                    aggregateBy=None, breakdownMode='classic',
                    countOnly=None, includeDesc=True
                )
                if df is not None and len(df) > 0:
                    all_data.append(df)
                    print(f"HS {hs}, {year}: {len(df)} records")
                else:
                    print(f"No data: HS {hs}, {year}")
            except Exception as e:
                print(f"Error HS {hs}, {year}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


def collect_preview():
    import comtradeapicall
    all_data = []

    for year in YEARS:
        for hs in HS_CODES:
            try:
                df = comtradeapicall.previewFinalData(
                    typeCode='C', freqCode='A', clCode='HS',
                    period=year, reporterCode=REPORTER_KOREA,
                    cmdCode=hs, flowCode='X',
                    partnerCode=None, partner2Code=None,
                    customsCode=None, motCode=None,
                    maxRecords=500, format_output='JSON',
                    aggregateBy=None, breakdownMode='classic',
                    countOnly=None, includeDesc=True
                )
                if df is not None and len(df) > 0:
                    all_data.append(df)
                    print(f"Preview HS {hs}, {year}: {len(df)} records")
            except Exception as e:
                print(f"Preview error HS {hs}, {year}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


def collect():
    def collect():
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        api_key = os.environ.get('COMTRADE_API_KEY', '')

    if api_key:
        print("Using API key.")
        result = collect_with_api(api_key)
    else:
        print("No API key. Using preview mode.")
        result = collect_preview()

    if result.empty:
        print("\nNo data. Manual download from https://comtradeplus.un.org/TradeFlow")
        return

    output_path = os.path.join(OUTPUT_DIR, 'comtrade_hs3304.csv')
    result.to_csv(output_path, index=False)
    print(f"\nSaved: {output_path} ({len(result)} rows)")


if __name__ == '__main__':
    collect()
