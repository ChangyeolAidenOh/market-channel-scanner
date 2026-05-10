"""
Sales Brief Generator revision version
Added: Evidence status, Buyer Ask, Go/No-Go criteria.
Fixed: Header/footer (portfolio simulation), currency by country, real market scores.
"""
import json
import os
from datetime import datetime
from fpdf import FPDF

REF_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'reference')

BRAND_MAP = {
    'PDRN Cream': 'Medicube', 'PDRN Serum': 'Medicube',
    'PDRN Serum (expand from online to in-store)': 'Medicube',
    'PDRN Serum (push into bestseller)': 'Medicube',
    'PDRN Serum (editorial push)': 'Medicube',
    'PDRN Serum (reactivate)': 'Medicube',
    'PDRN Pink Radiance Routine set (upsell)': 'Medicube',
    'PDRN line expansion': 'Medicube',
    'Zero Pore Pad 2.0': 'Medicube',
    'Zero Pore Pad 2.0 (in-store placement)': 'Medicube',
    'Zero Pore Pad 2.0 (reactivate)': 'Medicube',
    'Zero Pore Pad 2.0 (high-volume hero)': 'Medicube',
    'Zero Pore Pad 2.0 (already Hot on social)': 'Medicube',
    'Collagen Night Wrapping Mask': 'Medicube',
    'Collagen Night Wrapping Mask (in-store placement)': 'Medicube',
    'Collagen Night Wrapping Mask (reactivate)': 'Medicube',
    'AGE-R Booster Pro': 'Medicube', 'AGE-R Booster Pro Mini': 'Medicube',
    'AGE-R Booster Pro (in-store demo)': 'Medicube',
    'AGE-R Booster Pro (new category)': 'Medicube',
    'AGE-R Booster Pro (expand device presence)': 'Medicube',
    'AGE-R Booster Glow': 'Medicube',
    'AGE-R Booster Pro + PDRN Serum + PDRN Cream bundle': 'Medicube',
    'Medicube Zero Pore Pad 2.0 (expand in-store)': 'Medicube',
    'Medicube PDRN Serum (expand in-store)': 'Medicube',
    'Aprilskin TXA Serum': 'Aprilskin',
    'Aprilskin TXA line (entry tier, capture sub-$15 shopper)': 'Aprilskin',
    'Aprilskin Calendula Peeling Pad (new listing)': 'Aprilskin',
    'Aprilskin Calendula Peeling Pad (new, fits Primor price tier at EUR 12-16)': 'Aprilskin',
    'Aprilskin Calendula Pad (entry tier cross-sell)': 'Aprilskin',
    'Aprilskin Carrot Blemish Serum (new listing)': 'Aprilskin',
    'Calendula Peeling Pad': 'Aprilskin', 'Carrot Blemish Serum': 'Aprilskin',
    'Cotton Bath Perfume': 'Forment',
}

CURRENCY_MAP = {
    'US': ('$', 'USD'), 'GB': ('\u00a3', 'GBP'),
    'DE': ('\u20ac', 'EUR'), 'FR': ('\u20ac', 'EUR'),
    'ES': ('\u20ac', 'EUR'), 'PL': ('PLN ', 'PLN'),
    'KZ': ('\u20b8', 'KZT'), 'AE': ('AED ', 'AED'),
    'BR': ('R$', 'BRL'), 'EU': ('\u20ac', 'EUR'),
}


def s(text):
    for old, new in {
        '\u2014': '-', '\u2013': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u2022': '-',
        '\u00a0': ' ', '\u2192': '->', '\u00b7': '-',
        '\u20ac': 'EUR ',
        '\u00a3': 'GBP ',
        '\u20b8': 'KZT ',
    }.items():
        text = text.replace(old, new)
    return text


class Brief(FPDF):

    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 6, 'APR Global Sales Portfolio Simulation  |  Account Brief', align='L')
        self.cell(0, 6, s(datetime.now().strftime('%Y.%m.%d')), align='R',
                  new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(180, 180, 180)
        self.line(10, self.get_y() + 1, 200, self.get_y() + 1)
        self.ln(5)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 6)
        self.set_text_color(160, 160, 160)
        self.cell(0, 4,
                  'Candidate Portfolio Simulation  |  Public-source based  |  '
                  + datetime.now().strftime('%B %Y'),
                  align='C')

    def label(self, text):
        self.set_font('Helvetica', 'B', 8.5)
        self.set_text_color(60, 60, 60)
        self.cell(0, 7, s(text), new_x='LMARGIN', new_y='NEXT')

    def text_block(self, text):
        self.set_font('Helvetica', '', 8)
        self.set_text_color(70, 70, 70)
        self.multi_cell(w=0, h=4.5, text=s(text),
                        new_x='LMARGIN', new_y='NEXT')
        self.ln(1.5)

    def field(self, key, value):
        self.set_font('Helvetica', '', 7.5)
        self.set_text_color(130, 130, 130)
        self.cell(38, 4.5, s(key))
        self.set_font('Helvetica', '', 8)
        self.set_text_color(50, 50, 50)
        self.multi_cell(w=0, h=4.5, text=s(value),
                        new_x='LMARGIN', new_y='NEXT')

    def divider(self):
        self.ln(2)
        self.set_draw_color(210, 210, 210)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def check_page_break(self, h=30):
        if self.get_y() + h > self.h - 20:
            self.add_page()


def load_buyer(buyer_id):
    with open(os.path.join(REF_DIR, 'buyers.json'), 'r') as f:
        return next((b for b in json.load(f)['buyers'] if b['id'] == buyer_id), None)


def load_country(iso2):
    with open(os.path.join(REF_DIR, 'country_qualitative.json'), 'r') as f:
        return json.load(f).get('countries', {}).get(iso2, {})


def load_apr():
    with open(os.path.join(REF_DIR, 'apr_products.json'), 'r') as f:
        return json.load(f)


def get_brand(product_name):
    if product_name in BRAND_MAP:
        return BRAND_MAP[product_name]
    if product_name.lower().startswith('aprilskin'):
        return 'Aprilskin'
    return 'Medicube'


def get_currency(iso2):
    return CURRENCY_MAP.get(iso2, ('$', 'USD'))


def generate_brief(buyer_id, market_score=None, output_path=None):
    buyer = load_buyer(buyer_id)
    if not buyer:
        return None

    iso2 = buyer['country'].split('/')[0].split(' ')[0]
    country = load_country(iso2)
    apr = load_apr()
    currency_sym, currency_code = get_currency(iso2)

    buyer_name = buyer['buyer']
    country_name = country.get('name', buyer['country'])
    channel = buyer.get('channel_type', '')

    pdf = Brief()
    pdf.add_page()

    # Title
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(0, 8, s(buyer_name), new_x='LMARGIN', new_y='NEXT')
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(0, 5, s(f'{country_name}  |  {channel}'),
             new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)

    # Evidence status badge
    ev_status = buyer.get('evidence_status', 'Not specified')
    pdf.set_font('Helvetica', 'B', 7)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, s(f'Evidence status: {ev_status}'),
             new_x='LMARGIN', new_y='NEXT')
    pdf.ln(2)

    # Overview
    pdf.label('Overview')
    pdf.field('Channel', f'{channel} ({buyer.get("online_offline", "")})')
    pdf.field('Scale', buyer.get('scale', '-').capitalize())
    kbeauty = buyer.get('kbeauty_presence', [])
    if kbeauty:
        display_brands = kbeauty[:8]
        suffix = f' + {len(kbeauty) - 8} more' if len(kbeauty) > 8 else ''
        pdf.field('K-beauty presence', ', '.join(display_brands) + suffix)
    pdf.field('APR status', buyer.get('apr_current_status', 'Not entered'))
    if market_score:
        pdf.field('Country opportunity score', f'{market_score} / 100')
    pdf.divider()

    # Primary Buyer Ask
    buyer_ask = buyer.get('buyer_ask', '')
    if buyer_ask:
        pdf.label('Primary Buyer Ask')
        pdf.set_font('Helvetica', 'B', 8)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(w=0, h=5, text=s(buyer_ask),
                       new_x='LMARGIN', new_y='NEXT')
        pdf.divider()

    # Market Context
    pdf.label('Market Context')
    parts = []
    if country.get('strategic_note'):
        parts.append(country['strategic_note'])
    if country.get('regulation_complexity'):
        parts.append(f'Regulation complexity: {country["regulation_complexity"]}.')
    if country.get('key_risk'):
        parts.append(f'Key risk: {country["key_risk"]}')
    # Override for Notino (EU)
    market_context_override = buyer.get('market_context_override', '')
    if market_context_override:
        pdf.text_block(market_context_override)
    elif parts:
        pdf.text_block('  '.join(parts))
    else:
        pdf.text_block('Market context data not available for this region.')
    pdf.divider()

    # Commercial Hypothesis
    hypothesis = buyer.get('commercial_hypothesis', '')
    if hypothesis:
        pdf.check_page_break(25)
        pdf.label('Commercial Hypothesis')
        pdf.set_font('Helvetica', 'I', 8)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(w=0, h=4.5, text=s(hypothesis),
                       new_x='LMARGIN', new_y='NEXT')
        pdf.ln(1)
        pdf.divider()

    # Recommended Lineup
    pdf.check_page_break(30)
    pdf.label('Recommended Lineup')
    products = buyer.get('first_pitch_products', [])
    for prod in products:
        brand = get_brand(prod)
        detail = ''
        for bk, bd in apr.get('brands', {}).items():
            for p in bd.get('key_products', []) + bd.get('device_products', []):
                clean_prod = prod.split(' (')[0]
                if p['name'] == clean_prod:
                    price = p['price_usd']
                    detail = f'{currency_sym}{price}, {p["category"].replace("_", " ")}'
        pdf.set_font('Helvetica', '', 7.5)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(0, 5, s(f'{brand}  |  {prod}  {detail}'),
                 new_x='LMARGIN', new_y='NEXT')
    pdf.ln(1)

    entry_angle = buyer.get('apr_entry_angle', '')
    if entry_angle:
        pdf.set_font('Helvetica', 'I', 7.5)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(w=0, h=4.5, text=s(f'Positioning: {entry_angle}'),
                       new_x='LMARGIN', new_y='NEXT')
    pdf.divider()

    # Go-to-Market
    pdf.check_page_break(25)
    pdf.label('Go-to-Market Approach')
    test = buyer.get('test_structure', '')
    if test:
        pdf.text_block(test)
    kpis = buyer.get('success_kpi', [])
    if kpis:
        pdf.field('Success KPI', ', '.join(kpis[:3]))
    risk = buyer.get('risk', '')
    if risk:
        pdf.field('Key risk', risk)

    # Go / No-Go
    go_nogo = buyer.get('go_nogo', '')
    if go_nogo:
        pdf.ln(1)
        pdf.field('Go / No-Go', go_nogo)
    pdf.divider()

    # Key Considerations
    objections = buyer.get('objection_response', {})
    if objections:
        pdf.check_page_break(20)
        pdf.label('Key Considerations')
        for concern, response in objections.items():
            pdf.check_page_break(15)
            pdf.set_font('Helvetica', 'B', 7.5)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(w=0, h=4.5, text=s(f'"{concern}"'),
                          new_x='LMARGIN', new_y='NEXT')
            pdf.set_font('Helvetica', '', 7.5)
            pdf.set_text_color(90, 90, 90)
            pdf.multi_cell(w=0, h=4.5, text=s(response),
                          new_x='LMARGIN', new_y='NEXT')
            pdf.ln(2)

    # Sign-off
    if pdf.page_no() == pdf.pages_count:
        pdf.ln(3)
        pdf.set_font('Helvetica', '', 7)
        pdf.set_text_color(160, 160, 160)
        pdf.cell(0, 4, s(f'Prepared by Changyeol Aiden Oh  |  {datetime.now().strftime("%B %Y")}'),
                 align='R', new_x='LMARGIN', new_y='NEXT')

    if output_path is None:
        out_dir = os.path.dirname(__file__)
        os.makedirs(out_dir, exist_ok=True)
        output_path = os.path.join(out_dir, f'brief_{buyer_id}.pdf')
    pdf.output(output_path)
    print(f"Generated: {output_path}")
    return output_path


if __name__ == '__main__':
    import pandas as pd
    scores_path = os.path.join(
        os.path.dirname(__file__), '..', 'data', 'processed', 'market_scores.csv'
    )
    scores = pd.read_csv(scores_path)
    score_map = dict(zip(scores['country_iso3'], scores['base']))

    buyer_ids = [
        'amazon_us', 'ulta_us', 'boots_uk',
        'douglas_de', 'dm_de', 'rossmann_de',
        'notino_eu', 'sephora_eu', 'primor_es'
    ]
    country_iso3_map = {
        'amazon_us': 'USA', 'ulta_us': 'USA',
        'boots_uk': 'GBR', 'douglas_de': 'DEU', 'dm_de': 'DEU',
        'rossmann_de': 'DEU', 'notino_eu': None,
        'sephora_eu': 'FRA', 'primor_es': 'ESP',
    }
    for bid in buyer_ids:
        iso3 = country_iso3_map.get(bid)
        ms = round(score_map.get(iso3, 50), 1) if iso3 else None
        generate_brief(bid, market_score=ms)
