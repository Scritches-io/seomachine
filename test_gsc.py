"""Query GSC for top 50 keywords on the pet sitting business page."""

import sys
sys.path.insert(0, '/Users/lucasstefanski/scritches/seomachine')

from data_sources.modules.google_search_console import GoogleSearchConsole

gsc = GoogleSearchConsole(
    site_url='sc-domain:scritches.io',
    credentials_path='/Users/lucasstefanski/scritches/seomachine/credentials/gsc-credentials.json'
)

page_url = 'https://scritches.io/blog/how-to-start-pet-sitting-business'

# Use the underlying API directly for full control
from datetime import datetime, timedelta

start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

# Get page-level summary
page_request = {
    'startDate': start_date,
    'endDate': end_date,
    'dimensions': ['page'],
    'dimensionFilterGroups': [{
        'filters': [{
            'dimension': 'page',
            'operator': 'equals',
            'expression': page_url
        }]
    }]
}

page_response = gsc.service.searchanalytics().query(
    siteUrl=gsc.site_url,
    body=page_request
).execute()

if page_response.get('rows'):
    row = page_response['rows'][0]
    print(f"Page: {page_url}")
    print(f"Period: {start_date} to {end_date} (90 days)")
    print(f"Total Clicks: {row['clicks']}")
    print(f"Total Impressions: {row['impressions']}")
    print(f"Average CTR: {row['ctr']*100:.2f}%")
    print(f"Average Position: {row['position']:.1f}")
    print()
else:
    print("No page-level data found.")

# Get top 50 queries for this page
keywords_request = {
    'startDate': start_date,
    'endDate': end_date,
    'dimensions': ['query'],
    'dimensionFilterGroups': [{
        'filters': [{
            'dimension': 'page',
            'operator': 'equals',
            'expression': page_url
        }]
    }],
    'rowLimit': 50
}

keywords_response = gsc.service.searchanalytics().query(
    siteUrl=gsc.site_url,
    body=keywords_request
).execute()

rows = keywords_response.get('rows', [])
rows.sort(key=lambda x: x['impressions'], reverse=True)

print(f"{'#':<4} {'Keyword':<55} {'Clicks':>7} {'Impr':>7} {'CTR':>8} {'Pos':>6}")
print("-" * 91)

for i, row in enumerate(rows, 1):
    keyword = row['keys'][0]
    if len(keyword) > 52:
        keyword = keyword[:49] + '...'
    clicks = row['clicks']
    impressions = row['impressions']
    ctr = row['ctr'] * 100
    position = row['position']
    print(f"{i:<4} {keyword:<55} {clicks:>7} {impressions:>7} {ctr:>7.2f}% {position:>5.1f}")

print(f"\nTotal keywords found: {len(rows)}")
