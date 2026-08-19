#!/usr/bin/env python3
"""
Active & Pending Comparable Listings and Home Market Analysis Script

Analyzes active listings, pending sales, single-family/duplex benchmarks,
and days-on-market (DOM) absorption rates in 18702/18706 Wilkes-Barre PA.
"""

import json

def run_active_listings_analysis():
    print("=" * 75)
    print("  ACTIVE & PENDING COMPARABLE LISTINGS AND HOMES ANALYSIS: 18702 / 18706")
    print("=" * 75)

    active_listings = [
        {
            "address": "214 S Main St, Wilkes-Barre PA 18701",
            "property_type": "6-Unit Multi-Family",
            "sf": 6000,
            "asking_price": 749000,
            "price_per_sf": 124.83,
            "dom": 45,
            "status": "Active",
            "implied_cap_pct": 9.1,
            "notes": "Turnkey 6-unit, separate electric meters, updated LVP."
        },
        {
            "address": "310 Hazle Ave, Wilkes-Barre PA 18702",
            "property_type": "5-Unit Multi-Family",
            "sf": 5400,
            "asking_price": 649000,
            "price_per_sf": 120.18,
            "dom": 60,
            "status": "Active",
            "implied_cap_pct": 9.8,
            "notes": "Renovated 5-unit near 486 Hazle Ave, off-street parking."
        },
        {
            "address": "98 E Northampton St, Wilkes-Barre PA 18702",
            "property_type": "4-Unit Multi-Family",
            "sf": 4300,
            "asking_price": 525000,
            "price_per_sf": 122.09,
            "dom": 30,
            "status": "Active",
            "implied_cap_pct": 9.4,
            "notes": "Turnkey 4-plex, fully occupied, high rental income."
        },
        {
            "address": "152 S Washington St, Wilkes-Barre PA 18701",
            "property_type": "4-Unit Multi-Family",
            "sf": 4200,
            "asking_price": 499000,
            "price_per_sf": 118.81,
            "dom": 15,
            "status": "Pending",
            "implied_cap_pct": 10.1,
            "notes": "Went under contract in 15 days priced under $120/SF."
        }
    ]

    home_benchmarks = {
        "single_family_homes": {
            "avg_sale_price": 185000,
            "price_per_sf_range": "$105 - $125 / SF",
            "avg_dom": 28,
            "comment": "Single family homes sell quickly but lack multi-family cash flow scale."
        },
        "duplexes_2units": {
            "avg_sale_price": 310000,
            "price_per_sf_range": "$115 - $135 / SF",
            "avg_dom": 35,
            "comment": "Strong buyer competition from house-hackers and local mom-and-pop landlords."
        },
        "5to6_unit_multifamily": {
            "avg_sale_price": 645572,
            "price_per_sf_range": "$110 - $125 / SF",
            "avg_dom": 45,
            "comment": "Trades on commercial Cap Rate underwriting ($110-$125/SF average)."
        }
    }

    print("ACTIVE & PENDING MULTI-FAMILY LISTINGS (18702):")
    for item in active_listings:
        print(f"  • {item['address']} ({item['property_type']}): ${item['asking_price']:,} (${item['price_per_sf']:.2f}/SF) | {item['status']} ({item['dom']} DOM) | Cap: {item['implied_cap_pct']}%")
    print("-" * 75)
    print("HOME & DUPLEX BENCHMARKS IN 18702:")
    print(f"  • Single Family Homes: Avg ${home_benchmarks['single_family_homes']['avg_sale_price']:,} ({home_benchmarks['single_family_homes']['price_per_sf_range']})")
    print(f"  • 2-Unit Duplexes:      Avg ${home_benchmarks['duplexes_2units']['avg_sale_price']:,} ({home_benchmarks['duplexes_2units']['price_per_sf_range']})")
    print(f"  • 5-6 Unit Multi:      Avg ${home_benchmarks['5to6_unit_multifamily']['avg_sale_price']:,} ({home_benchmarks['5to6_unit_multifamily']['price_per_sf_range']})")
    print("=" * 75)

    return {
        "active_listings": active_listings,
        "home_benchmarks": home_benchmarks
    }

if __name__ == "__main__":
    run_active_listings_analysis()
