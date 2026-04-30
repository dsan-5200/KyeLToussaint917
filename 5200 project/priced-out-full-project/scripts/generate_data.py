"""
Generate realistic synthetic displacement data for D.C. ZIP codes.
Based on real patterns from Census ACS, Zillow, and Eviction Lab data.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

# Real DC ZIP codes with neighborhood names
dc_zips = {
    "20001": "Shaw / NoMa",
    "20002": "Capitol Hill / H Street",
    "20003": "Capitol Hill South",
    "20004": "Downtown / Penn Quarter",
    "20005": "Logan Circle / U Street",
    "20009": "Adams Morgan / Columbia Heights",
    "20010": "Columbia Heights",
    "20011": "Petworth / 16th Street Heights",
    "20015": "Chevy Chase",
    "20016": "Spring Valley / AU Park",
    "20017": "Brookland / Michigan Park",
    "20018": "Woodridge / Fort Lincoln",
    "20019": "Capitol Heights / Deanwood",
    "20020": "Anacostia / Congress Heights",
    "20024": "Southwest Waterfront",
    "20032": "Congress Heights / Bellevue",
    "20036": "Dupont Circle / West End",
    "20037": "Foggy Bottom / Georgetown",
}

years = list(range(2010, 2024))
zips = list(dc_zips.keys())

# --- Gentrification profiles per ZIP ---
# Higher = more gentrification pressure
gentrify_score = {
    "20001": 0.95, "20002": 0.85, "20009": 0.90, "20010": 0.88,
    "20005": 0.92, "20024": 0.80, "20036": 0.60, "20037": 0.55,
    "20003": 0.75, "20004": 0.65, "20011": 0.70, "20017": 0.60,
    "20015": 0.20, "20016": 0.15, "20018": 0.45, "20019": 0.30,
    "20020": 0.35, "20032": 0.28,
}

# Base 2010 median rent ($)
base_rent = {
    "20001": 1350, "20002": 1280, "20009": 1400, "20010": 1100,
    "20005": 1500, "20024": 1200, "20036": 1800, "20037": 2000,
    "20003": 1600, "20004": 1900, "20011": 950, "20017": 980,
    "20015": 1700, "20016": 1750, "20018": 900, "20019": 850,
    "20020": 800, "20032": 820,
}

# Base 2010 Black population share (%)
base_black_pct = {
    "20001": 52, "20002": 45, "20009": 30, "20010": 55,
    "20005": 28, "20024": 35, "20036": 12, "20037": 8,
    "20003": 20, "20004": 15, "20011": 65, "20017": 60,
    "20015": 5,  "20016": 4,  "20018": 70, "20019": 85,
    "20020": 90, "20032": 88,
}

# Base 2010 renter share (%)
base_renter_pct = {
    "20001": 72, "20002": 65, "20009": 78, "20010": 70,
    "20005": 68, "20024": 62, "20036": 60, "20037": 55,
    "20003": 55, "20004": 70, "20011": 60, "20017": 58,
    "20015": 25, "20016": 22, "20018": 62, "20019": 68,
    "20020": 72, "20032": 74,
}

records = []

for z in zips:
    gs = gentrify_score[z]
    rent = base_rent[z]
    black_pct = base_black_pct[z]
    renter_pct = base_renter_pct[z]
    base_income = 45000 + (1 - gs) * 30000 + np.random.normal(0, 3000)

    for yr in years:
        t = yr - 2010

        # Rent grows faster in high-gentrify ZIPs
        rent_growth = 1 + (0.035 + gs * 0.045) + np.random.normal(0, 0.01)
        rent = rent * rent_growth

        # Income grows slower than rent in high-gentrify areas (displacement pressure)
        income_growth = 1 + (0.02 + (1 - gs) * 0.01) + np.random.normal(0, 0.005)
        base_income = base_income * income_growth

        # Black population declines faster in high-gentrify ZIPs
        black_pct = max(2, black_pct - gs * 1.8 * np.random.uniform(0.5, 1.5))

        # Rent burden = % income spent on rent
        annual_rent = rent * 12
        rent_burden = min(65, (annual_rent / base_income) * 100)

        # Eviction rate inversely correlated with income, spikes during shocks
        eviction_base = 2 + gs * 4 + np.random.normal(0, 0.5)
        eviction_spike = 3.5 if yr == 2020 else 0  # COVID eviction surge
        eviction_rate = max(0.1, eviction_base + eviction_spike)

        # Vacancy rate rises after displacement
        vacancy_rate = max(1, 4 - gs * 2 + t * gs * 0.15 + np.random.normal(0, 0.3))

        records.append({
            "zip": z,
            "neighborhood": dc_zips[z],
            "year": yr,
            "median_rent": round(rent, 0),
            "median_income": round(base_income, 0),
            "black_pct": round(black_pct, 1),
            "renter_pct": round(renter_pct + np.random.normal(0, 0.5), 1),
            "rent_burden_pct": round(rent_burden, 1),
            "eviction_rate": round(eviction_rate, 2),
            "vacancy_rate": round(vacancy_rate, 2),
            "gentrify_score": gs,
        })

df = pd.DataFrame(records)
df.to_csv("/home/claude/displacement-project/data/dc_displacement.csv", index=False)
print(f"Generated {len(df)} records across {len(zips)} ZIP codes, {len(years)} years")
print(df.head())
